# Third-party
from django.conf import settings
from django.db import models

# Local
from core.models import Country


class Season(models.Model):
    year = models.PositiveSmallIntegerField(unique=True)
    period = models.CharField(max_length=50, blank=True, null=True, default=None)

    def __str__(self):
        return str(self.year)


class League(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    reference_id = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ["reference_id", "season", "country"]


class Team(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    reference_id = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Game(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    league = models.ForeignKey(League, on_delete=models.PROTECT)
    home_team = models.ForeignKey(
        Team, on_delete=models.PROTECT, related_name="home_teams"
    )
    away_team = models.ForeignKey(
        Team, on_delete=models.PROTECT, related_name="away_teams"
    )

    reference_id = models.IntegerField(help_text="Game ID")
    datetime = models.DateTimeField()
    status = models.CharField(max_length=100)
    scores = models.JSONField(blank=True)

    def __str__(self):
        return str(self.reference_id)
