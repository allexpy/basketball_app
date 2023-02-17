# Third-party
import pytest
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

# Local
from core.models import Country

EMAIL = "test@example.com"
PASSWORD = "pAssw0rd!ASD"


@pytest.fixture(scope="session")
def create_user():
    def _create_user(user_type: int, email=EMAIL, password=PASSWORD):
        user = get_user_model().objects.create_user(
            email=email,
            first_name="Test",
            last_name="User",
            password=password,
            type=user_type,
        )
        return user

    return _create_user


@pytest.fixture(scope="session")
def create_authenticated_client():
    def _create_authenticated_client(user):
        url = reverse("accounts:log_in")
        data = dict()
        data["email"] = user
        data["password"] = PASSWORD

        client = APIClient()
        response = client.post(url, data)

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
        return client

    return _create_authenticated_client


@pytest.fixture(scope="session")
def create_country():
    def _create_country():
        country = Country.objects.create(reference_id=1, code="US", name="USA")
        return country

    return _create_country
