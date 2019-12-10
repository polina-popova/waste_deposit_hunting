import json

import requests


GEO_API_PROVIDER_URL = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=5&' \
                       'lat={latitude}&lon={longitude}'


def get_state(latitude, longitude):
    """Get geo state for the provided coordinates. """

    response = requests.get(GEO_API_PROVIDER_URL.format(
        latitude=latitude, longitude=longitude)
    )
    if response.status_code != 200:
        return None

    return json.loads(response.content)['address']['state']
