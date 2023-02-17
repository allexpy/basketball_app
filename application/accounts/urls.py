# Third-party
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

# Local
from accounts import views

app_name = "accounts"

router_admin = routers.DefaultRouter()
router_admin.register("", views.UsersViewSet, basename="users")

urlpatterns = [
    path("sign_up/", views.SignUpView.as_view(), name="sign_up"),
    path("log_in/", views.LogInView.as_view(), name="log_in"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", include(router_admin.urls)),
]
