# built-in
import json
import os

# third-party
import requests
from django.core.management.base import BaseCommand

# local
from games.services import import_leagues


class Command(BaseCommand):
    help = "Import leagues into database."

    def handle(self, *args, **options):
        headers = dict()
        headers["X-RapidAPI-Key"] = os.getenv("RAPID_API_KEY")
        headers["X-RapidAPI-Host"] = "api-basketball.p.rapidapi.com"
        response = requests.get(
            url="https://api-basketball.p.rapidapi.com/leagues",
            headers=headers,
        )

        if response.status_code == 200:
            data = json.loads(response.text)
            if not data["results"]:
                self.stdout.write("No results found.")

            import_leagues(data=data["response"])
            self.stdout.write("Done.")

        elif response.status_code == 400:
            data = json.loads(response.text)
            self.stdout.write(f'{data["errors"]}')
        else:
            self.stdout.write("Service Unavailable.")
