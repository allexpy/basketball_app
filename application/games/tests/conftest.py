# Built-in
import datetime

# Third-party
import pytest
from django.utils.timezone import get_current_timezone, make_aware

# Local
from games.models import Game, League, Season, Team


@pytest.fixture(scope="session")
def create_season():
    def _create_season():
        season = Season.objects.create(year=2022, period="2022-2023")
        return season

    return _create_season


@pytest.fixture(scope="session")
def create_league(create_country, create_season):
    def _create_league():
        country = create_country()
        season = create_season()
        league = League.objects.create(
            country=country,
            season=season,
            reference_id=1,
            name="NBA",
            type="National Men's Basketball",
        )
        return league

    return _create_league


@pytest.fixture(scope="session")
def create_team(create_league):
    def _create_team():
        league = create_league()
        team = Team.objects.create(
            country=league.country,
            season=league.season,
            league=league,
            reference_id=1,
            name="Chicago Bulls",
        )
        return team

    return _create_team


@pytest.fixture(scope="session")
def create_game(create_team):
    def _create_game():
        home_team = create_team()
        away_team = Team.objects.create(
            country=home_team.country,
            season=home_team.season,
            league=home_team.league,
            reference_id=2,
            name="Miami",
        )

        game = Game.objects.create(
            user=None,
            country=home_team.country,
            season=home_team.season,
            league=home_team.league,
            home_team=home_team,
            away_team=away_team,
            reference_id=1,
            datetime=make_aware(
                datetime.datetime.now(), timezone=get_current_timezone()
            ),
            status="Finished",
            scores={
                "home": {
                    "quarter_1": None,
                    "quarter_2": 25,
                    "quarter_3": None,
                    "quarter_4": 26,
                    "over_time": None,
                    "total": 51,
                },
                "away": {
                    "quarter_1": None,
                    "quarter_2": 21,
                    "quarter_3": None,
                    "quarter_4": 14,
                    "over_time": None,
                    "total": 35,
                },
            },
        )
        return game

    return _create_game
