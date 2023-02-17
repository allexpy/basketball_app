# Third-party
from django.urls import include, path
from rest_framework import routers

# Local
from games import views

app_name = "games"


router_admin = routers.DefaultRouter()
router_admin.register("", views.AdminGameViewSet, basename="admin-games")

router_user = routers.DefaultRouter()
router_user.register(
    "assigned", views.UserAssignedGameViewSet, basename="user-assigned-games"
)
router_user.register(
    "unassigned", views.UserUnassignedGameViewSet, basename="user-unassigned-games"
)

urlpatterns = [
    path("import-games/", views.ImportGameAPIView.as_view(), name="import-games"),
    path("", include(router_admin.urls)),
    path("user/", include(router_user.urls)),
]
