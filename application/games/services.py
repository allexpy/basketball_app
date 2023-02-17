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
