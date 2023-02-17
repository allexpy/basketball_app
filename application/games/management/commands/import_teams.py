# Built-in
import json
import os

# Third-party
import requests
from django.core.management.base import BaseCommand

# Local
from core.models import Country
from games.models import League, Season, Team


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

            # sezonul are nevoie de liga, liga nu are nevoie de sezon
            db_countries = Country.objects.all()
            db_seasons = Season.objects.all()
            db_leagues = League.objects.all()
            db_teams = Team.objects.all()
            teams = []

            for idx, team_data in enumerate(data["response"], start=1):
                if not db_teams.filter(
                    reference_id=team_data["id"],
                    season__year=season,
                    league__reference_id=league,
                ).exists():
                    teams.append(
                        Team(
                            country=db_countries.filter(
                                reference_id=team_data["country"]["id"]
                            ).first(),
                            season=db_seasons.filter(year=season).first(),
                            league=db_leagues.filter(
                                reference_id=league, season__year=season
                            ).first(),
                            reference_id=team_data["id"],
                            name=team_data["name"],
                        )
                    )
                    self.stdout.write(f'{idx}. {team_data["name"]} added')

            Team.objects.bulk_create(teams, batch_size=100)
            self.stdout.write("Done.")

        elif response.status_code == 400:
            data = json.loads(response.text)
            self.stdout.write(f'{data["errors"]}')
        else:
            self.stdout.write("Service Unavailable.")
