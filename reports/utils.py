import requests

from sentry_sdk import capture_message

GEO_API_PROVIDER_URL = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&' \
                       'lat={latitude}&lon={longitude}'


def get_location_attrs(latitude, longitude):
    """Get geo state for the provided coordinates. """

    response = requests.get(GEO_API_PROVIDER_URL.format(
        latitude=latitude, longitude=longitude),
        headers={'Accept-Language': "ru-Ru"}
    )
    if response.status_code != 200:
        capture_message(
            'Bad response from OpenStreetMap API', level='error'
        )
        return None
    address_json = response.json()['address']
    state = address_json['state']

    address = []
    for address_attr in ('county', 'city', 'road', 'building', 'house_number'):
        if address_attr in address_json:
            address.append(address_json[address_attr])

    verbose_address = ', '.join(address)

    return state, verbose_address
