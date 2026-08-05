from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', db_column='sender_id')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', db_column='receiver_id')
    message_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'

    def __str__(self):
        return f"Msg from {self.sender.username} to {self.receiver.username}"
