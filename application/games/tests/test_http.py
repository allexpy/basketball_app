# Third-party
import os

import pytest
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse

# Local
from games.models import Game, League, Season, Team
from games.serializers import (
    AdminGameSerializer,
    LeagueSerializer,
    SeasonSerializer,
    TeamSerializer,
)


@pytest.mark.django_db
def test_season_list(create_user, create_authenticated_client, create_season):
    season = create_season()
    url = reverse("core:seasons-list")
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0] == SeasonSerializer(season).data


@pytest.mark.django_db
def test_season_is_retrieved_by_id(
    create_user, create_authenticated_client, create_season
):
    season = create_season()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:seasons-detail", kwargs={"pk": season.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == SeasonSerializer(season).data


@pytest.mark.django_db
def test_create_season(create_user, create_authenticated_client):
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:seasons-list")
    data = dict()
    data["year"] = 2022
    data["period"] = "2022-2023"
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Season.objects.count() == 1
    assert response.data["year"] == 2022
    assert response.data["period"] == "2022-2023"


@pytest.mark.django_db
def test_change_season_year_and_period(
    create_user, create_authenticated_client, create_season
):
    season = create_season()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:seasons-detail", kwargs={"pk": season.id})
    data = dict()
    data["year"] = 2012
    data["period"] = "2012-2013"
    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["year"] == 2012
    assert response.data["period"] == "2012-2013"


@pytest.mark.django_db
def test_change_season_year_and_period_with_patch(
    create_user, create_authenticated_client, create_season
):
    season = create_season()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:seasons-detail", kwargs={"pk": season.id})
    data = dict()
    data["year"] = 2012
    data["period"] = "2012-2013"
    response = client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["year"] == 2012
    assert response.data["period"] == "2012-2013"


@pytest.mark.django_db
def test_season_delete(create_user, create_authenticated_client, create_season):
    season = create_season()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:seasons-detail", kwargs={"pk": season.id})
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Season.objects.count() == 0


@pytest.mark.django_db
def test_league_list(create_user, create_authenticated_client, create_league):
    league = create_league()
    url = reverse("core:leagues-list")
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0] == LeagueSerializer(league).data


@pytest.mark.django_db
def test_league_is_retrieved_by_id(
    create_user, create_authenticated_client, create_league
):
    league = create_league()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:leagues-detail", kwargs={"pk": league.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == LeagueSerializer(league).data


@pytest.mark.django_db
def test_league_season(
    create_user, create_authenticated_client, create_country, create_season
):
    country = create_country()
    season = create_season()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:leagues-list")
    data = dict()
    data["country"] = country.id
    data["season"] = season.id
    data["reference_id"] = 1
    data["name"] = "NBA"
    data["type"] = "National Men's Basketball"

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Season.objects.count() == 1
    assert response.data["country"] == 1
    assert response.data["season"] == 1
    assert response.data["reference_id"] == 1
    assert response.data["name"] == "NBA"
    assert response.data["type"] == "National Men's Basketball"


@pytest.mark.django_db
def test_change_league_name(create_user, create_authenticated_client, create_league):
    league = create_league()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:leagues-detail", kwargs={"pk": league.id})
    data = dict()
    data["country"] = league.country_id
    data["season"] = league.season_id
    data["reference_id"] = league.reference_id
    data["name"] = "TEST"
    data["type"] = league.type
    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["reference_id"] == 1
    assert response.data["name"] == "TEST"


@pytest.mark.django_db
def test_change_league_year_and_period_with_patch(
    create_user, create_authenticated_client, create_league
):
    league = create_league()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:leagues-detail", kwargs={"pk": league.id})
    data = dict()
    data["reference_id"] = 1
    data["name"] = "TEST"
    response = client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["reference_id"] == 1
    assert response.data["name"] == "TEST"


@pytest.mark.django_db
def test_league_delete(create_user, create_authenticated_client, create_league):
    league = create_league()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:leagues-detail", kwargs={"pk": league.id})
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert League.objects.count() == 0


@pytest.mark.django_db
def test_team_list(create_user, create_authenticated_client, create_team):
    team = create_team()
    url = reverse("core:teams-list")
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0] == TeamSerializer(team).data


@pytest.mark.django_db
def test_team_is_retrieved_by_id(create_user, create_authenticated_client, create_team):
    team = create_team()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:teams-detail", kwargs={"pk": team.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == TeamSerializer(team).data


@pytest.mark.django_db
def test_create_team(create_user, create_authenticated_client, create_league):
    league = create_league()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:teams-list")
    data = dict()
    data["country"] = league.country.id
    data["season"] = league.season.id
    data["league"] = league.id
    data["reference_id"] = 1
    data["name"] = "Red Bulls"

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Season.objects.count() == 1
    assert response.data["country"] == 1
    assert response.data["season"] == 1
    assert response.data["league"] == 1
    assert response.data["reference_id"] == 1
    assert response.data["name"] == "Red Bulls"


@pytest.mark.django_db
def test_change_team_name(create_user, create_authenticated_client, create_team):
    team = create_team()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:teams-detail", kwargs={"pk": team.id})
    data = dict()
    data["country"] = team.country_id
    data["season"] = team.season_id
    data["league"] = team.league_id
    data["reference_id"] = team.reference_id
    data["name"] = "TEST"
    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["reference_id"] == 1
    assert response.data["name"] == "TEST"


@pytest.mark.django_db
def test_change_team_name_with_patch(
    create_user, create_authenticated_client, create_team
):
    team = create_team()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:teams-detail", kwargs={"pk": team.id})
    data = dict()
    data["name"] = "TEST"
    response = client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "TEST"


@pytest.mark.django_db
def test_team_delete(create_user, create_authenticated_client, create_team):
    team = create_team()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:teams-detail", kwargs={"pk": team.id})
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Team.objects.count() == 0


@pytest.mark.django_db
def test_admin_game_list(create_user, create_authenticated_client, create_game):
    game = create_game()
    url = reverse("games:admin-games-list")
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0] == AdminGameSerializer(game).data


@pytest.mark.django_db
def test_admin_game_is_retrieved_by_id(
    create_user, create_authenticated_client, create_game
):
    game = create_game()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("games:admin-games-detail", kwargs={"pk": game.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == AdminGameSerializer(game).data


@pytest.mark.django_db
def test_admin_assign_game_user(create_user, create_authenticated_client, create_game):
    game = create_game()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    normal_user = create_user(
        user_type=get_user_model().UserTypes.NORMAL, email="user@example.com"
    )

    client = create_authenticated_client(admin_user)
    url = reverse("games:admin-games-detail", kwargs={"pk": game.id})
    data = dict()
    data["user"] = normal_user.id
    data["country"] = game.country_id
    data["season"] = game.season_id
    data["league"] = game.league_id
    data["home_team"] = game.home_team_id
    data["away_team"] = game.away_team_id
    data["reference_id"] = game.reference_id
    data["datetime"] = game.datetime
    data["status"] = "Finished"
    data["scores"] = {
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
    }

    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"] == normal_user.id


@pytest.mark.django_db
def test_admin_change_game_user_with_patch(
    create_user, create_authenticated_client, create_game
):
    game = create_game()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    normal_user = create_user(
        user_type=get_user_model().UserTypes.NORMAL, email="user@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("games:admin-games-detail", kwargs={"pk": game.id})
    data = dict()
    data["user"] = normal_user.id

    response = client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"] == normal_user.id


@pytest.mark.django_db
def test_admin_game_delete(create_user, create_authenticated_client, create_game):
    game = create_game()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("games:admin-games-detail", kwargs={"pk": game.id})
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Game.objects.count() == 0


@pytest.mark.django_db
def test_normal_user_assigned_game_list(
    create_user, create_authenticated_client, create_game
):
    game = create_game()
    url = reverse("games:user-assigned-games-list")
    normal_user = create_user(
        user_type=get_user_model().UserTypes.NORMAL, email="user@example.com"
    )
    normal_user.countries.add(game.country)
    normal_user.save()

    game.user = normal_user
    game.save()

    client = create_authenticated_client(normal_user)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0] == AdminGameSerializer(game).data
    assert response.data["results"][0]["user"] == normal_user.id
    assert response.data["results"][0]["country"] in normal_user.countries.values_list(
        "id", flat=True
    )


@pytest.mark.django_db
def test_normal_user_assigned_game_is_retrieved_by_id(
    create_user, create_authenticated_client, create_game
):
    game = create_game()
    url = reverse("games:user-assigned-games-detail", kwargs={"pk": game.id})
    normal_user = create_user(
        user_type=get_user_model().UserTypes.NORMAL, email="user@example.com"
    )
    normal_user.countries.add(game.country)
    normal_user.save()

    game.user = normal_user
    game.save()

    client = create_authenticated_client(normal_user)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == AdminGameSerializer(game).data
    assert response.data["user"] == normal_user.id
    assert response.data["country"] in normal_user.countries.values_list(
        "id", flat=True
    )


@pytest.mark.django_db
def test_normal_user_unassigned_game_list(
    create_user, create_authenticated_client, create_game
):
    game = create_game()
    url = reverse("games:user-unassigned-games-list")
    normal_user = create_user(
        user_type=get_user_model().UserTypes.NORMAL, email="user@example.com"
    )
    normal_user.countries.add(game.country)
    normal_user.save()

    client = create_authenticated_client(normal_user)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0] == AdminGameSerializer(game).data
    assert response.data["results"][0]["user"] is None
    assert response.data["results"][0]["country"] in normal_user.countries.values_list(
        "id", flat=True
    )


@pytest.mark.django_db
def test_normal_user_unassigned_game_is_retrieved_by_id(
    create_user, create_authenticated_client, create_game
):
    game = create_game()
    url = reverse("games:user-unassigned-games-detail", kwargs={"pk": game.id})
    normal_user = create_user(
        user_type=get_user_model().UserTypes.NORMAL, email="user@example.com"
    )
    normal_user.countries.add(game.country)
    normal_user.save()

    client = create_authenticated_client(normal_user)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == AdminGameSerializer(game).data
    assert response.data["user"] is None
    assert response.data["country"] in normal_user.countries.values_list(
        "id", flat=True
    )


@pytest.mark.django_db
def test_normal_user_unassigned_game_is_assigning_to_itself(
    create_user, create_authenticated_client, create_game
):
    game = create_game()
    url = reverse("games:user-unassigned-games-assign-game", kwargs={"pk": game.id})
    normal_user = create_user(
        user_type=get_user_model().UserTypes.NORMAL, email="user@example.com"
    )
    normal_user.countries.add(game.country)
    normal_user.save()

    client = create_authenticated_client(normal_user)
    response = client.post(url)

    game.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert game.country_id in normal_user.countries.values_list("id", flat=True)
    assert game.user == normal_user


@pytest.mark.django_db
def test_normal_user_unassigned_game_is_assigning_to_itself_bad_request(
    create_user, create_authenticated_client, create_game
):
    game = create_game()
    url = reverse("games:user-unassigned-games-assign-game", kwargs={"pk": game.id})
    normal_user = create_user(
        user_type=get_user_model().UserTypes.NORMAL, email="user@example.com"
    )

    client = create_authenticated_client(normal_user)
    response = client.post(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


class MockedResponse:
    def __init__(self, status_code_number, text_body):
        self.status_code = status_code_number
        self.text = text_body

    def text(self):
        return self.text

    def status_code(self):
        return self.status_code


def mock_get(*args, **kwargs):
    with open(os.path.join(settings.ROOT_DIR, "examples/games.json")) as file:
        return MockedResponse(status.HTTP_200_OK, file.read())


@pytest.mark.django_db
def test_import_games(
    monkeypatch, create_user, create_authenticated_client, create_team
):
    home_team = create_team()
    Team.objects.create(
        country=home_team.country,
        season=home_team.season,
        league=home_team.league,
        reference_id=2,
        name="Miami",
    )

    url = reverse("games:import-games")
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)

    monkeypatch.setattr(requests, "get", mock_get)

    data = dict()
    data["season"] = 2022
    data["league"] = 178
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["success"] is True
    assert Game.objects.count() == 1


def mock_get_no_results(*args, **kwargs):
    return MockedResponse(status.HTTP_200_OK, '{"results": []}')


@pytest.mark.django_db
def test_import_games_api_no_results_bad_request(
    monkeypatch, create_user, create_authenticated_client
):
    url = reverse("games:import-games")
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    monkeypatch.setattr(requests, "get", mock_get_no_results)

    data = dict()
    data["season"] = 2022
    data["league"] = 178
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data["success"] is False
    assert Game.objects.count() == 0


def mock_get_with_bad_request(*args, **kwargs):
    return MockedResponse(status.HTTP_400_BAD_REQUEST, '{"errors": "Errors message"}')


@pytest.mark.django_db
def test_import_games_api_bad_request(
    monkeypatch, create_user, create_authenticated_client
):
    url = reverse("games:import-games")
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    monkeypatch.setattr(requests, "get", mock_get_with_bad_request)

    data = dict()
    data["season"] = 2022
    data["league"] = 178
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["success"] is False
    assert Game.objects.count() == 0


def mock_get_service_unavailable(*args, **kwargs):
    return MockedResponse(
        status.HTTP_500_INTERNAL_SERVER_ERROR, '{"errors": "Errors message"}'
    )


@pytest.mark.django_db
def test_import_games_api_service_unavailable(
    monkeypatch, create_user, create_authenticated_client
):
    url = reverse("games:import-games")
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    monkeypatch.setattr(requests, "get", mock_get_service_unavailable)

    data = dict()
    data["season"] = 2022
    data["league"] = 178
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.data["success"] is False
    assert Game.objects.count() == 0


@pytest.mark.django_db
def test_import_games_bad_season_data(create_user, create_authenticated_client):
    url = reverse("games:import-games")
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)

    data = dict()
    data["season"] = 1949
    data["league"] = 178
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert type(response.data["season"][0]) == ErrorDetail

    data = dict()
    data["season"] = 2050
    data["league"] = 178
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert type(response.data["season"][0]) == ErrorDetail

    data = dict()
    data["season"] = "1940-2020"
    data["league"] = 178
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert type(response.data["season"][0]) == ErrorDetail

    data = dict()
    data["season"] = "2000-2070"
    data["league"] = 178
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert type(response.data["season"][0]) == ErrorDetail

    data = dict()
    data["season"] = "gsdfgsfdgfdg"
    data["league"] = 178
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert type(response.data["season"][0]) == ErrorDetail

    data = dict()
    data["season"] = "gsdfg-sfdgfdg"
    data["league"] = 178
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert type(response.data["season"][0]) == ErrorDetail
