from core.models import Country


def import_countries(data: list):
    db_countries = Country.objects.all()
    countries = []
    for idx, country_data in enumerate(data, start=1):
        if not db_countries.filter(reference_id=country_data["id"]).exists():
            countries.append(
                Country(
                    reference_id=country_data["id"],
                    name=country_data["name"],
                    code=country_data["code"],
                )
            )
            print(f'{idx}. {country_data["name"]} added')

    Country.objects.bulk_create(countries)
    return True
