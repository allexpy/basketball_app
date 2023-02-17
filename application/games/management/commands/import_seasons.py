# built-in
import json
import os
from itertools import zip_longest

# third-party
import requests
from django.core.management.base import BaseCommand

# local
from games.services import import_seasons


class Command(BaseCommand):
    help = "Import seasons into database."

    def handle(self, *args, **options):
        headers = dict()
        headers["X-RapidAPI-Key"] = os.getenv("RAPID_API_KEY")
        headers["X-RapidAPI-Host"] = "api-basketball.p.rapidapi.com"
        response = requests.get(
            url="https://api-basketball.p.rapidapi.com/seasons",
            headers=headers,
        )

        if response.status_code == 200:
            data = json.loads(response.text)
            if not data["results"]:
                self.stdout.write("No results found.")
            years = data["response"][0::2]  # 2008
            periods = data["response"][1::2]  # "2008-2009"
            matches = dict(zip_longest(years, periods))
            import_seasons(data=matches)
            self.stdout.write("Done.")

        elif response.status_code == 400:
            data = json.loads(response.text)
            self.stdout.write(f'{data["errors"]}')
        else:
            self.stdout.write("Service Unavailable.")
