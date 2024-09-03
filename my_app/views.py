from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import PollForm, ChoiceForm, CommentForm
from .models import Poll, Choice, Comment

# Create your views here.

class Login(LoginView):
    template_name = 'accounts/login.html'

def Home(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.user = request.user
            poll.save()
            return redirect(f'/polls/{poll.id}')
    else:
        poll_form = PollForm()
    
    polls = Poll.objects.all()

    return render(request, 'home.html', {'poll_form': poll_form, 'polls': polls})

def Profile(request, username):
    user = get_object_or_404(User, username=username)
    is_user = False
    if (request.user.username == username):
        is_user = True

    context = {
        'profile_user': user,
        'is_user': is_user
    }
    return render(request, 'profile.html', context)

def submitVote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    if request.method == 'POST':

        previous_choice = None
        cookie_name = f'poll_{pk}'
        # searches user browser cookies in request to see if they voted already
        if cookie_name in request.COOKIES:
            choice_id = request.COOKIES[cookie_name] # assigns choice they chose
            try:
                previous_choice = Choice.objects.get(id=choice_id, poll=poll) # finds the choice object
                previous_choice.votes -= 1
                previous_choice.save()
            except Choice.DoesNotExist:
                previous_choice = None

        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
        selected_choice.votes += 1
        selected_choice.save()

        response = redirect('poll-detail', pk=poll.id)
        response.set_cookie(f'poll_{poll.id}', selected_choice.id, max_age=365*24*60*60) # saves a cookie from browser for a year

        return response

    return redirect('poll-detail', pk=poll.id)

@login_required
def togglePublic(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    if request.method == 'POST':
        poll.isPublic = not poll.isPublic
        poll.save()
        return redirect('poll-detail', pk=poll.id)

    return redirect('poll-detail', pk=poll.id)

@login_required
def toggleEditing(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    if request.method == 'POST':
        poll.allowEditing = not poll.allowEditing
        poll.save()
        return redirect('poll-detail', pk=poll.id)

    return redirect('poll-detail', pk=poll.id)

@login_required
def editPoll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    if request.method == 'POST':
        poll_form = PollForm(request.POST, instance=poll)
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.save()
            return redirect(f'/polls/{poll.id}')
        else:
            return redirect('poll-detail', pk=poll.id)

def createChoice(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    if request.method == 'POST':
        choice_form = ChoiceForm(request.POST)

        if choice_form.is_valid():
            choice = choice_form.save(commit=False)
            choice.user = request.user
            choice.poll = poll
            choice.save()
            return redirect('poll-detail', pk=poll.id)
    else:
        return redirect('poll-detail', pk=poll.id)

@login_required
def deletePoll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    poll.delete()
    return redirect('home')

@login_required
def createComment(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.poll = poll
            comment.save()
            return redirect('poll-detail', pk=poll.id)
    else:
        return redirect('poll-detail', pk=poll.id)

# RENDERS THE POLL DETAIL PAGE
def pollDetail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    poll_form = PollForm(instance=poll)
    choice_form = ChoiceForm()
    comment_form = CommentForm()
    choices = poll.choice_set.all().order_by('created_at')
    is_public = poll.isPublic
    editing_allowed = poll.allowEditing

    total_votes = 0
    for choice in poll.choice_set.all():
        total_votes += choice.votes

    previous_choice = None
    cookie_name = f'poll_{poll.id}'
    # searches user browser cookies in request to see if they voted already
    if cookie_name in request.COOKIES:
        choice_id = request.COOKIES[cookie_name] # assigns choice they chose
        try:
            previous_choice = Choice.objects.get(id=choice_id, poll=poll) # finds the choice object
        except Choice.DoesNotExist:
            previous_choice = None
    
    comments = poll.comment_set.all()

    return render(request, 'polls/detail.html', {
        'previous_choice': previous_choice,
        'poll_form': poll_form,
        'choice_form': choice_form,
        'comment_form': comment_form,
        'poll': poll,
        'choices': choices,
        'comments': comments,
        'total_votes': total_votes,
        'is_public': is_public,
        'editing_allowed': editing_allowed
    })

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'accounts/signup.html', context)