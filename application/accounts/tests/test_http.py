# Built-in
import base64
import json

# Third-party
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

# Local
from accounts.serializers import AdminUserSerializer
from conftest import EMAIL, PASSWORD


@pytest.mark.django_db
def test_user_can_sign_up():
    url = reverse("accounts:sign_up")
    data = dict()
    data["email"] = "test@example.com"
    data["first_name"] = "Test"
    data["last_name"] = "User"
    data["password1"] = PASSWORD
    data["password2"] = PASSWORD
    client = APIClient()
    response = client.post(url, data, format="json")
    user = get_user_model().objects.last()
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["id"] == user.id
    assert response.data["email"] == user.email
    assert response.data["first_name"] == user.first_name
    assert response.data["last_name"] == user.last_name


@pytest.mark.django_db
def test_user_tries_to_signup_wrong_email_bad_request():
    url = reverse("accounts:sign_up")

    data = dict()
    data["email"] = "test"
    data["first_name"] = "Test"
    data["last_name"] = "User"
    data["password1"] = PASSWORD
    data["password2"] = PASSWORD
    client = APIClient()
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_tries_to_signup_passwords_do_not_match_bad_request():
    url = reverse("accounts:sign_up")

    data = dict()
    data["email"] = "test@example.com"
    data["first_name"] = "Test"
    data["last_name"] = "User"
    data["password1"] = PASSWORD
    data["password2"] = "123fojgfioe"
    client = APIClient()
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_can_log_in(create_user):
    user = create_user(user_type=get_user_model().UserTypes.NORMAL)
    url = reverse("accounts:log_in")
    data = dict()
    data["email"] = EMAIL
    data["password"] = PASSWORD
    client = APIClient()
    response = client.post(url, data, format="json")

    # Parse payload data from access token.
    access = response.data["access"]
    header, payload, signature = access.split(".")
    decoded_payload = base64.b64decode(f"{payload}==")
    payload_data = json.loads(decoded_payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["refresh"] is not None
    assert payload_data["id"] == user.id
    assert payload_data["email"] == user.email
    assert payload_data["first_name"] == user.first_name
    assert payload_data["last_name"] == user.last_name


@pytest.mark.django_db
def test_normal_users_list(create_user, create_authenticated_client):
    url = reverse("accounts:users-list")
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    normal_user = create_user(
        user_type=get_user_model().UserTypes.NORMAL, email="user@example.com"
    )
    client = create_authenticated_client(admin_user)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0] == AdminUserSerializer(normal_user).data


@pytest.mark.django_db
def test_normal_users_is_retrieved_by_id(create_user, create_authenticated_client):
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    normal_user = create_user(
        user_type=get_user_model().UserTypes.NORMAL, email="user@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("accounts:users-detail", kwargs={"pk": normal_user.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == AdminUserSerializer(normal_user).data


@pytest.mark.django_db
def test_add_normal_user_country_permission(
    create_user, create_authenticated_client, create_country
):
    country = create_country()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    normal_user = create_user(
        user_type=get_user_model().UserTypes.NORMAL, email="user@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("accounts:users-detail", kwargs={"pk": normal_user.id})
    data = dict()
    data["countries"] = [country.id]
    response = client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["countries"][0]["id"] == country.id


@pytest.mark.django_db
def test_remove_normal_user_country_permission(
    create_user, create_authenticated_client, create_country
):
    country = create_country()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    normal_user = create_user(
        user_type=get_user_model().UserTypes.NORMAL, email="user@example.com"
    )
    normal_user.countries.add(country)
    normal_user.save()

    client = create_authenticated_client(admin_user)
    url = reverse("accounts:users-detail", kwargs={"pk": normal_user.id})
    data = dict()
    data["countries"] = []
    response = client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["countries"] == []
