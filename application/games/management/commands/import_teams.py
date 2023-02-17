# Built-in
import json
import os

# Third-party
import requests
from django.core.management.base import BaseCommand

# Local
from games.services import import_teams


class Command(BaseCommand):
    help = "Import teams into database."

    def handle(self, *args, **options):
        headers = dict()
        headers["X-RapidAPI-Key"] = os.getenv("RAPID_API_KEY")
        headers["X-RapidAPI-Host"] = "api-basketball.p.rapidapi.com"

        # league & season are mandatory
        # season must be mandatory by this form '2019-2020'
        season = 2022
        league = 178  # US
        response = requests.get(
            url="https://api-basketball.p.rapidapi.com/teams",
            headers=headers,
            params={"league": league, "season": season},
        )

        if response.status_code == 200:
            data = json.loads(response.text)
            if not data["results"]:
                self.stdout.write("No results found.")

            import_teams(data=data['response'], season=season, league=league)
            self.stdout.write("Done.")

        elif response.status_code == 400:
            data = json.loads(response.text)
            self.stdout.write(f'{data["errors"]}')
        else:
            self.stdout.write("Service Unavailable.")
