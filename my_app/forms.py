from django import forms
from .models import Poll, Choice, Comment

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'poll-title',
                'class': 'poll-input',
                'placeholder': 'Start a poll...'
            })
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'choice-input',
                'placeholder': 'Add choice...'
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'comment-input',
                'placeholder': 'Type a comment...'
            })
        }
        labels = {
            'text': ''
        }