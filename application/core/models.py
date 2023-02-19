# Third-party
from django.db import models


class Country(models.Model):
    reference_id = models.PositiveSmallIntegerField()
    code = models.CharField(max_length=2, blank=True, null=True, default=None)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
