from django.db import models

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
