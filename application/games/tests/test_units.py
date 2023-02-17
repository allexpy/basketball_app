# Third-party
import pytest

# Local
from games.models import Game, Team
from games.services import import_games


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

    context = create_data_for_import()
    data = context["response"]
    assert import_games(data=data) is True
    assert Game.objects.count() == 1
