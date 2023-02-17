# Third-party
import pytest

# Local
from core.models import Country
from core.services import import_countries


@pytest.mark.django_db
def test_import_countries_service(create_data_for_import):
    context = create_data_for_import(filename="countries")
    data = context["response"]
    assert import_countries(data=data) is True
    assert Country.objects.count() == 75
