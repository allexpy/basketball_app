# Third-party
from django.urls import include, path
from rest_framework import routers

# Local
from core import views as core_views
from games import views as games_views

app_name = "core"


router = routers.DefaultRouter()
router.register("countries", core_views.CountryViewSet, basename="countries")
router.register("seasons", games_views.SeasonViewSet, basename="seasons")
router.register("leagues", games_views.LeagueViewSet, basename="leagues")
router.register("teams", games_views.TeamViewSet, basename="teams")

urlpatterns = [
    path("", include(router.urls)),
]
