
from django.db import models
from django.db.models.fields import DateTimeField, TextField
from ..loginApp.models import User

class Message(models.Model):
    user = models.ForeignKey(User, related_name="messages_from", on_delete=models.SET_NULL,null=True)
    user_for = models.ForeignKey(User, related_name="messages_for", on_delete=models.SET_NULL,null=True)
    message = TextField()
    #comments
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class Comment(models.Model):
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.SET_NULL,null=True)
    comment = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)