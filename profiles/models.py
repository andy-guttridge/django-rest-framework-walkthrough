from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/',
        default='../default_profile_sopzfa.jpg'
    )

    class Meta:
        # Return results for this model with the most recent entries first
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


# This function will be called every time a user is created.
# The parameters it receives are a requirement of Django signals.
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)

# Use post_save to register to receive a signal every time a new user is created.
# First paremeter is the function we want to run when the signal is received, the
# second parameter is the model we want to request signals from.
post_save.connect(create_profile, sender=User)

