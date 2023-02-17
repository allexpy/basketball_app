# Third-party
from django.core.management.base import BaseCommand

# Local
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Create a user admin."

    def handle(self, *args, **options):
        CustomUser.objects.create_user(
            email="admin@example.com",
            password="pAssw0rd!",
            type=CustomUser.UserTypes.ADMIN,
        )
        self.stdout.write("Admin user created.")

        # TODO de facut sa creeze inca un user normal dar cu argumente pentru alegere
