from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import uuid


class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    expiry_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Choice(models.Model):
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Vote(models.Model):
    choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE, related_name='votes')
    email = models.EmailField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    otp = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(999999),
            MinValueValidator(100000)
        ],
        null=True,
        blank=True
    )
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
