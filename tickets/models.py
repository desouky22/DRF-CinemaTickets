from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User

# Guest, Reservation, Movie
class Movie(models.Model):
    hall = models.CharField(max_length=255)
    movie = models.CharField(max_length=255)
    date = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.hall


class Guest(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    guest = models.ForeignKey(
        Guest,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reservations",
    )


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def token_create(sender, instance, created, *args, **kwargs):
    if created:
        Token.objects.create(user=instance)
