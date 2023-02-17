# Built-in
import json
import os

# Third-party
import requests
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

# Local
from core.permissions import AdminsOnlyPermission, UsersOnlyPermission
from games.models import Game, League, Season, Team
from games.serializers import (
    AdminGameSerializer,
    ImportGameSerializer,
    LeagueSerializer,
    SeasonSerializer,
    TeamSerializer,
    UserGameSerializer,
)
from games.services import import_games


class SeasonViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, AdminsOnlyPermission)
    model = Season
    queryset = Season.objects.order_by("-id")
    serializer_class = SeasonSerializer


class LeagueViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, AdminsOnlyPermission)
    model = League
    queryset = League.objects.order_by("-id")
    serializer_class = LeagueSerializer


class TeamViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, AdminsOnlyPermission)
    model = Team
    queryset = Team.objects.order_by("-id")
    serializer_class = TeamSerializer


class AdminGameViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, AdminsOnlyPermission)
    model = Game
    queryset = Game.objects.all()
    serializer_class = AdminGameSerializer


class UserAssignedGameViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, UsersOnlyPermission)
    model = Game
    serializer_class = UserGameSerializer
    queryset = Game.objects.all()

    def get_queryset(self):
        if not getattr(self, "swagger_fake_view", False):
            qs = super().get_queryset()
            return qs.filter(
                country__in=self.request.user.countries.all(), user=self.request.user
            ).order_by("-id")
        return self.model.objects.none()


class UserUnassignedGameViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """see games from their country with games unassigned to them
    assign games to themselves
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, UsersOnlyPermission)  # user
    model = Game
    serializer_class = UserGameSerializer
    http_method_names = ["get", "post"]
    queryset = Game.objects.all()

    def get_queryset(self):
        if not getattr(self, "swagger_fake_view", False):
            qs = super().get_queryset()
            return qs.filter(
                country__in=self.request.user.countries.all(), user__isnull=True
            ).order_by("-id")
        return self.model.objects.none()

    @action(
        detail=True, methods=["POST"], url_path="assign-game", url_name="assign-game"
    )
    def assign_game(self, request, pk):
        instance = self.get_object()
        instance.user = request.user
        instance.save(update_fields=["user"])
        return Response({"success": True}, status=status.HTTP_200_OK)


class ImportGameAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, AdminsOnlyPermission)

    def post(self, request, *args, **kwargs):
        params_serializer = ImportGameSerializer(data=request.data)
        params_serializer.is_valid(raise_exception=True)
        headers = dict()
        headers["X-RapidAPI-Key"] = os.getenv("RAPID_API_KEY")
        headers["X-RapidAPI-Host"] = "api-basketball.p.rapidapi.com"
        response = requests.get(
            url="https://api-basketball.p.rapidapi.com/games",
            headers=headers,
            params=params_serializer.validated_data,
        )

        if response.status_code == 200:
            data = json.loads(response.text)
            if not data["results"]:
                return Response({"success": False, "message": "No results matched."}, status=status.HTTP_204_NO_CONTENT)
            import_games(data=data["response"])

        elif response.status_code == 400:
            data = json.loads(response.text)
            return Response({"success": False, "message": data["errors"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success": False, "message": "Service unavailable."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"success": True}, status=status.HTTP_201_CREATED)
