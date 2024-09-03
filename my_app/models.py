from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Poll(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    isPublic = models.BooleanField(default=False)
    allowEditing = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Choice(models.Model):
    text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE) # choices belong to a unique poll

    def __str__(self):
        return self.text
    
class Comment(models.Model):
    text = models.TextField(max_length=250)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text