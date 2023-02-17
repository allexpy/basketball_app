# Third-party
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Local
from core.models import Country
from core.permissions import AdminsOnlyPermission
from core.serializers import CountrySerializer


class CountryViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, AdminsOnlyPermission)
    model = Country
    queryset = Country.objects.order_by("-id")
    serializer_class = CountrySerializer
