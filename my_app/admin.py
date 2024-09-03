from django.contrib import admin
from .models import Poll, Choice, Comment

# Register your models here.
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Comment)