# Third-party
from rest_framework import serializers

# Local
from core.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
