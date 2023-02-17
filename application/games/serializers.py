# Built-in
import datetime

# Third-party
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Local
from games.models import Game, League, Season, Team


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = "__all__"


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class ImportGameSerializer(serializers.Serializer):
    league = serializers.IntegerField(
        required=True, write_only=True, help_text="YYYY, YYYY-YYYY"
    )
    season = serializers.CharField(required=True, write_only=True)
    date = serializers.DateField(
        required=False, write_only=True, help_text="2019-11-26"
    )
    team = serializers.IntegerField(required=False, write_only=True)

    @staticmethod
    def validate_date(value):
        return str(value)

    @staticmethod
    def validate_season(value):
        current_year = datetime.datetime.now().year

        if value.isdigit():
            if not (1950 <= int(value) <= current_year):
                raise ValidationError(f"Season must be between 1950 and {current_year}")
        else:
            if "-" not in value:
                raise ValidationError("Incorrect value. Season ex: YYYY, YYYY-YYYY")

            first_year, second_year = value.split("-")
            if not first_year.isdigit() or not second_year.isdigit():
                raise ValidationError("Incorrect value. Season ex: YYYY, YYYY-YYYY")

            if not (1950 <= int(first_year) <= current_year) or not (
                1950 <= int(second_year) <= current_year
            ):
                raise ValidationError(f"Season must be between 1950 and {current_year}")
        return value


class AdminGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "user",
            "country",
            "reference_id",
            "league",
            "season",
            "home_team",
            "away_team",
            "datetime",
            "status",
            "scores",
        ]


class UserGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "user",
            "country",
            "reference_id",
            "league",
            "season",
            "home_team",
            "away_team",
            "datetime",
            "status",
            "scores",
        ]
