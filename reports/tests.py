import tempfile
from collections import namedtuple
from unittest import mock

from PIL import Image
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase

from reports.helpers import get_desired_width
from reports.models import Report


Coordinates = namedtuple('Coordinates', ('lat', 'long'))
VALID_COORDINATES = Coordinates(64.61833411, 40.9587337)  # Coordinates of the point in Arkhangelsk area
INVALID_COORDINATES = Coordinates(61.932308, 37.5152280)  # Coordinates of the point out of Arkhangelsk area
COORDINATES_WITH_ADDRESS = Coordinates(64.58200895, 40.51487245)

PhotoSize = namedtuple('PhotoSize', ('width', 'height'))
BIG_SIZE = PhotoSize(9000, 6000)
DEFAULT_TEST_SIZE = PhotoSize(100, 100)

return_valid_state = mock.Mock(return_value=('Архангельская область', 'some address'))
return_invalid_state = mock.Mock(return_value=('Ленинградская область', 'some address'))


def _get_stub_photo(size):
    image = Image.new('RGB', size)
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file)

    return tmp_file


class ReportTestCase(APITestCase):
    @mock.patch('reports.utils.get_state', return_valid_state)
    def test_post_report(self):
        tmp_file = _get_stub_photo(size=BIG_SIZE)

        with open(tmp_file.name, 'rb') as photo:
            data = {
                'lat': VALID_COORDINATES.lat,
                'long': VALID_COORDINATES.long,
                'photo': photo
            }
            response = self.client.post(
                reverse('reports-list'), data=data
            )
            resized_width = get_desired_width(settings.PHOTO_MAX_HEIGHT, BIG_SIZE)

        report = Report.objects.filter(lat=VALID_COORDINATES.lat, long=VALID_COORDINATES.long).first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(report.photo.height, settings.PHOTO_MAX_HEIGHT)
        self.assertEqual(report.photo.width, resized_width)

    @mock.patch('reports.utils.get_state', return_invalid_state)
    def test_report_with_invalid_location(self):
        tmp_file = _get_stub_photo(size=DEFAULT_TEST_SIZE)

        with open(tmp_file.name, 'rb') as photo:
            data = {
                'lat': INVALID_COORDINATES.lat,
                'long': INVALID_COORDINATES.long,
                'photo': photo
            }
            response = self.client.post(
                reverse('reports-list'), data=data
            )

        self.assertEqual(response.status_code, 400)

    def test_report_with_address(self):
        tmp_file = _get_stub_photo(size=DEFAULT_TEST_SIZE)

        with open(tmp_file.name, 'rb') as photo:
            data = {
                'lat': COORDINATES_WITH_ADDRESS.lat,
                'long': COORDINATES_WITH_ADDRESS.long,
                'photo': photo
            }
            response = self.client.post(
                reverse('reports-list'), data=data
            )

        report = Report.objects\
            .filter(lat=COORDINATES_WITH_ADDRESS.lat, long=COORDINATES_WITH_ADDRESS.long)\
            .first()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(report.verbose_address)
        print(report.verbose_address)


class ContentComplainTestCase(APITestCase):
    @mock.patch('reports.utils.get_state', return_valid_state)
    def test_create_content_complain(self):
        tmp_file = _get_stub_photo(size=DEFAULT_TEST_SIZE)

        with open(tmp_file.name, 'rb') as photo:
            data = {
                'lat': VALID_COORDINATES.lat,
                'long': VALID_COORDINATES.long,
                'photo': photo
            }

            response = self.client.post(reverse('reports-list'), data=data)
        self.assertEqual(response.status_code, 201)

        to_be_complained_report_id = \
            Report.objects\
                .filter(lat=VALID_COORDINATES.lat, long=VALID_COORDINATES.long)\
                .first().id

        data = {'body': 'some complain text'}

        response = self.client.post(
            reverse(
                'complains-list',
                kwargs={'report_pk': to_be_complained_report_id}
                ),
            data=data
        )
        print(response.json())
        self.assertEqual(response.status_code, 201)

    @mock.patch('reports.utils.get_state', return_valid_state)
    def test_create_complain_to_unexisting_report(self):
        to_be_complained_unexisting_report_id = 100

        data = {'body': 'some complain text'}

        response = self.client.post(
            reverse(
                'complains-list',
                kwargs={'report_pk': to_be_complained_unexisting_report_id}
            ),
            data=data
        )
        self.assertEqual(response.status_code, 404)
