from django.urls import path
from . import views

urlpatterns = [
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('', views.Home, name='home'),
    path('profiles/<str:username>', views.Profile, name='profile'),
    path('polls/<int:pk>/', views.pollDetail, name='poll-detail'),
    path('polls/<int:pk>/edit-poll', views.editPoll, name='edit-poll'),
    path('polls/<int:pk>/toggle-public', views.togglePublic, name='toggle-public'),
    path('polls/<int:pk>/toggle-editing', views.toggleEditing, name='toggle-editing'),
    path('polls/<int:pk>/choices/create/', views.createChoice, name='create-choice'),
    path('polls/<int:pk>/vote/', views.submitVote, name='submit-vote'),
    path('polls/<int:pk>/delete/', views.deletePoll, name='delete-poll'),
    path('polls/<int:pk>/comments/create', views.createComment, name='create-comment')
]