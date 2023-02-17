# Third-party
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse

# Local
from core.models import Country
from core.serializers import CountrySerializer


@pytest.mark.django_db
def test_country_list(create_user, create_authenticated_client, create_country):
    country = create_country()
    url = reverse("core:countries-list")
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0] == CountrySerializer(country).data


@pytest.mark.django_db
def test_country_is_retrieved_by_id(
    create_user, create_authenticated_client, create_country
):
    country = create_country()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:countries-detail", kwargs={"pk": country.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == CountrySerializer(country).data


@pytest.mark.django_db
def test_create_country(create_user, create_authenticated_client):
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:countries-list")
    data = dict()
    data["reference_id"] = 1
    data["code"] = "US"
    data["name"] = "USA"
    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Country.objects.count() == 1
    assert response.data["name"] == "USA"
    assert response.data["code"] == "US"
    assert response.data["reference_id"] == 1


@pytest.mark.django_db
def test_change_country_name(create_user, create_authenticated_client, create_country):
    country = create_country()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:countries-detail", kwargs={"pk": country.id})
    data = dict()
    data["name"] = "TEST"
    data["reference_id"] = country.reference_id
    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "TEST"


@pytest.mark.django_db
def test_change_country_name_with_patch(
    create_user, create_authenticated_client, create_country
):
    country = create_country()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:countries-detail", kwargs={"pk": country.id})
    data = dict()
    data["name"] = "TEST"
    response = client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "TEST"


@pytest.mark.django_db
def test_country_delete(create_user, create_authenticated_client, create_country):
    country = create_country()
    admin_user = create_user(
        user_type=get_user_model().UserTypes.ADMIN, email="admin@example.com"
    )
    client = create_authenticated_client(admin_user)
    url = reverse("core:countries-detail", kwargs={"pk": country.id})
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Country.objects.count() == 0
