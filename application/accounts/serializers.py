# Third-party
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Local
from accounts.custom_signal import user_after_save
from accounts.models import CustomUser
from core.serializers import CountrySerializer


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password1", "password2", "first_name", "last_name")

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        data = {
            key: value
            for key, value in validated_data.items()
            if key not in ("password1", "password2")
        }
        user = self.Meta.model.objects.create(**data)
        user.set_password(validated_data["password1"])
        user.save()
        return user


class LogInSerializer(TokenObtainPairSerializer):
    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != "id":
                token[key] = value
        return token


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "countries"]
        read_only_fields = ["id", "email", "first_name", "last_name"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["countries"] = CountrySerializer(instance.countries.all(), many=True).data
        return data

    def save(self, **kwargs):
        former_countries = set(self.instance.countries.values_list("id", flat=True))
        instance = super().save(**kwargs)
        current_countries = set(self.instance.countries.values_list("id", flat=True))
        removed_countries = former_countries - current_countries
        # remove games with that country from this user
        user_after_save.send(
            CustomUser, instance=instance, country_ids=removed_countries
        )
        return instance
