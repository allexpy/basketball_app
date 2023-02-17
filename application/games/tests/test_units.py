# Built-in
from itertools import zip_longest

# Third-party
import pytest

from core.services import import_countries
# Local
from games.models import Game, Team, Season, League
from games.services import import_games, import_seasons, import_leagues, import_teams


@pytest.mark.django_db
def test_import_games_service(create_data_for_import, create_team):
    home_team = create_team()
    Team.objects.create(
        country=home_team.country,
        season=home_team.season,
        league=home_team.league,
        reference_id=2,
        name="Miami",
    )

    context = create_data_for_import(filename='games')
    data = context["response"]
    assert import_games(data=data) is True
    assert Game.objects.count() == 1


@pytest.mark.django_db
def test_import_seasons_service(create_data_for_import):
    context = create_data_for_import(filename='seasons')
    years = context["response"][0::2]  # 2008
    periods = context["response"][1::2]  # "2008-2009"
    matches = dict(zip_longest(years, periods))
    assert import_seasons(data=matches) is True
    assert Season.objects.count() == 16


@pytest.mark.django_db
def test_import_leagues_service(create_data_for_import):
    # import countries
    countries_data = create_data_for_import(filename='countries')
    import_countries(data=countries_data['response'])

    # import seasons
    seasons_data = create_data_for_import(filename='seasons')
    years = seasons_data["response"][0::2]  # 2008
    periods = seasons_data["response"][1::2]  # "2008-2009"
    matches = dict(zip_longest(years, periods))
    import_seasons(data=matches)

    # import leagues
    context = create_data_for_import(filename='leagues')
    assert import_leagues(data=context['response']) is True
    assert League.objects.count() == 109


@pytest.mark.django_db
def test_import_teams_service(create_data_for_import):
    # import countries
    countries_data = create_data_for_import(filename='countries')
    import_countries(data=countries_data['response'])

    # import seasons
    seasons_data = create_data_for_import(filename='seasons')
    years = seasons_data["response"][0::2]  # 2008
    periods = seasons_data["response"][1::2]  # "2008-2009"
    matches = dict(zip_longest(years, periods))
    import_seasons(data=matches)

    # import leagues
    leagues_data = create_data_for_import(filename='leagues')
    import_leagues(data=leagues_data['response'])

    # import teams
    context = create_data_for_import(filename='teams')
    assert import_teams(data=context['response'], season=2022, league=178) is True
    assert Team.objects.count() == 12
