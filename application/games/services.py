import datetime
import zoneinfo

from core.models import Country
from games.models import Game, League, Season, Team


def import_games(data: list):
    games = []
    db_countries = Country.objects.all()
    db_seasons = Season.objects.all()
    db_leagues = League.objects.all()
    db_teams = Team.objects.all()
    db_games = Game.objects.all()
    for game_data in data:
        if not db_games.filter(reference_id=game_data["id"]).exists():
            games.append(
                Game(
                    country=db_countries.filter(
                        reference_id=game_data["country"]["id"]
                    ).first(),
                    season=db_seasons.filter(
                        year=game_data["league"]["season"]
                    ).first(),
                    league=db_leagues.filter(
                        reference_id=game_data["league"]["id"]
                    ).first(),
                    reference_id=game_data["id"],
                    datetime=datetime.datetime.strptime(
                        f"{game_data['date'].split('T')[0]} {game_data['time']}",
                        "%Y-%m-%d %H:%M",
                    ).replace(tzinfo=zoneinfo.ZoneInfo("UTC")),
                    status=game_data["status"]["long"],
                    home_team=db_teams.filter(
                        reference_id=game_data["teams"]["home"]["id"]
                    ).first(),
                    away_team=db_teams.filter(
                        reference_id=game_data["teams"]["away"]["id"]
                    ).first(),
                    scores=game_data["scores"],
                )
            )

    Game.objects.bulk_create(games, batch_size=100)
    return True


def import_seasons(data: dict):
    db_seasons = Season.objects.all()
    seasons = []
    for k, v in data.items():
        if not db_seasons.filter(year=k).exists():
            seasons.append(Season(year=k, period=v))
            print(f"{k} added")

    Season.objects.bulk_create(seasons)
    return True


def import_leagues(data: list):
    db_countries = Country.objects.all()
    db_seasons = Season.objects.all()
    db_leagues = League.objects.all()

    leagues = []
    idx = 0
    for league_data in data:
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
                print(
                    f"{idx}. "
                    f'{league_data["name"]} - '
                    f'{season_data["season"]} - '
                    f'{league_data["country"]["id"]} added'
                )
    League.objects.bulk_create(leagues)
    return True


def import_teams(data: list, season: int, league: 178):
    # sezonul are nevoie de liga, liga nu are nevoie de sezon
    db_countries = Country.objects.all()
    db_seasons = Season.objects.all()
    db_leagues = League.objects.all()
    db_teams = Team.objects.all()
    teams = []

    for idx, team_data in enumerate(data, start=1):
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
            print(f'{idx}. {team_data["name"]} added')

    Team.objects.bulk_create(teams, batch_size=100)
    return True
