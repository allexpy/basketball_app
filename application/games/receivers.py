from django.dispatch import receiver

from accounts.custom_signal import user_after_save
from accounts.models import CustomUser
from games.models import Game


@receiver(user_after_save, sender=CustomUser, dispatch_uid="user_after_save")
def user_after_save_update_games(sender, instance, *args, **kwargs):
    """
    Remove user from games if a certain country was removed from user.
    """
    Game.objects.filter(
        user=instance, league__country_id__in=kwargs["country_ids"]
    ).update(user=None)
