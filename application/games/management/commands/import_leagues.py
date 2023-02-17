# built-in
import json
import os

# third-party
import requests
from django.core.management.base import BaseCommand

# local
from core.models import Country
from games.models import League, Season


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

            db_countries = Country.objects.all()
            db_seasons = Season.objects.all()
            db_leagues = League.objects.all()

            leagues = []
            idx = 0
            for league_data in data["response"]:
                for season_data in league_data["seasons"]:
                    year = season_data["season"]
                    if isinstance(year, str):
                        year = int(year.split("-")[0])

                    if not db_leagues.filter(
                        reference_id=league_data["id"],
                        season__year=year,
                        country__reference_id=league_data["country"]["id"],
                    ).exists():
                        leagues.append(
                            League(
                                country=db_countries.filter(
                                    reference_id=league_data["country"]["id"]
                                ).first(),
                                season=db_seasons.filter(year=year).first(),
                                reference_id=league_data["id"],
                                name=league_data["name"],
                                type=league_data["type"],
                            )
                        )
                        idx += 1
                        self.stdout.write(
                            f"{idx}. "
                            f'{league_data["name"]} - '
                            f'{season_data["season"]} - '
                            f'{league_data["country"]["id"]} added'
                        )

            League.objects.bulk_create(leagues)
            self.stdout.write("Done.")

        elif response.status_code == 400:
            data = json.loads(response.text)
            self.stdout.write(f'{data["errors"]}')
        else:
            self.stdout.write("Service Unavailable.")
