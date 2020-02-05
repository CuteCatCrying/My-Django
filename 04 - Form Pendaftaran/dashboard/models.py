from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
    created_by = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confirm_message = models.TextField(blank=True)
    value_confirm_message = models.BooleanField(default=False)

    is_confirm_message = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return '{}. {}'.format(self.id, self.title)


