# Third-party
from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

# Local
from accounts.models import CustomUser
from accounts.serializers import AdminUserSerializer, LogInSerializer, UserSerializer
from core.permissions import AdminsOnlyPermission


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer


class UsersViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, AdminsOnlyPermission)
    model = CustomUser
    serializer_class = AdminUserSerializer
    queryset = CustomUser.objects.filter(type=CustomUser.UserTypes.NORMAL).order_by(
        "id"
    )
    http_method_names = ["get", "patch"]
