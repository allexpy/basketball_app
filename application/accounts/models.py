# Third-party
from custom_user.models import AbstractEmailUser
from django.db import models

# Local
from core.models import Country


class CustomUser(AbstractEmailUser):
    class UserTypes(models.IntegerChoices):
        ADMIN = 0, "Admin"
        NORMAL = 1, "Normal"

    countries = models.ManyToManyField(Country, blank=True)
    first_name = models.CharField(max_length=200, blank=True, null=True, default=None)
    last_name = models.CharField(max_length=200, blank=True, null=True, default=None)
    type = models.PositiveSmallIntegerField(
        choices=UserTypes.choices, default=UserTypes.NORMAL
    )

    def __str__(self):
        return self.email
