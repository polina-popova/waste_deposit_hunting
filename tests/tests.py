import tempfile
from collections import namedtuple
from unittest import mock

from PIL import Image
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase

from reports.helpers import get_desired_width
from reports.models import Report, State, WasteDeposit
from reports.logic import attach_to_waste_deposit
from send_daily_report import send_daily_report
from tests.data_factory import ValidReportFactory

Coordinates = namedtuple('Coordinates', ('lat', 'long'))
VALID_COORDINATES = Coordinates(64.61833411, 40.9587337)  # Coordinates of the point in Arkhangelsk area
INVALID_COORDINATES = Coordinates(61.932308, 37.5152280)  # Coordinates of the point out of Arkhangelsk area
COORDINATES_WITH_ADDRESS = Coordinates(64.58200895, 40.51487245)
IN_FIVE_METERS_COORDINATES = Coordinates(64.582013, 40.514944)  # Coordinates in less then 5 meters from COORDINATES_WITH_ADDRESS
MORE_THEN_IN_FIVE_METERS_COORDINATES = Coordinates(64.582156, 40.516663)  # Coordinates in more then 5 meters from COORDINATES_WITH_ADDRESS

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


class BaseTestCase(APITestCase):

    def tearDown(self) -> None:
        Report.objects.all().delete()


class ReportTestCase(BaseTestCase):
    @mock.patch('reports.serializers.get_location_attrs', return_valid_state)
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

    @mock.patch('reports.serializers.get_location_attrs', return_invalid_state)
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

    @mock.patch('reports.serializers.get_location_attrs', return_valid_state)
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


class ContentComplainTestCase(BaseTestCase):
    @mock.patch('reports.serializers.get_location_attrs', return_valid_state)
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
        self.assertEqual(response.status_code, 201)

    @mock.patch('reports.utils.get_location_attrs', return_valid_state)
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


@mock.patch('send_daily_report.EmailMultiAlternatives')
class SentDailyReportTestCase(BaseTestCase):

    def test_send_email(self, *args, **kwargs):
        for _ in range(3):
            ValidReportFactory()

        send_daily_report()
        unsent_reports = Report.objects.filter(was_sent=False)

        self.assertEqual(args[0].call_count, 2)
        self.assertEqual(len(unsent_reports), 1)

        State.objects.filter(emails='').update(emails='["someemail@mail.ru"]')
        send_daily_report()
        unsent_reports = Report.objects.filter(was_sent=False)

        self.assertEqual(args[0].call_count, 5)
        self.assertFalse(unsent_reports)


class AttachReportTestCase(BaseTestCase):
    PHOTO_PATH = settings.MEDIA_ROOT + '/test.png'

    def setUp(self):
        WasteDeposit.objects.create(
            lat=COORDINATES_WITH_ADDRESS.lat, long=COORDINATES_WITH_ADDRESS.long
        )

        photo = Image.new('RGB', DEFAULT_TEST_SIZE)
        photo.save(format='png', fp=self.PHOTO_PATH)

    def test_attach_report_to_existed_waste_deposit(self):
        report = Report.objects.create(
            photo=self.PHOTO_PATH, lat=IN_FIVE_METERS_COORDINATES.lat,
            long=IN_FIVE_METERS_COORDINATES.long
        )

        attach_to_waste_deposit(report)

        waste_deposits_qs = WasteDeposit.objects.all()
        report.refresh_from_db()

        self.assertEqual(len(waste_deposits_qs), 1)
        self.assertEqual(report.waste_deposit.lat, waste_deposits_qs.first().lat)
        self.assertEqual(report.waste_deposit.long, waste_deposits_qs.first().long)

    def test_create_new_waste_deposit(self):
        report = Report.objects.create(
            photo=self.PHOTO_PATH, lat=MORE_THEN_IN_FIVE_METERS_COORDINATES.lat,
            long=MORE_THEN_IN_FIVE_METERS_COORDINATES.long
        )

        attach_to_waste_deposit(report)

        waste_deposits_qs = WasteDeposit.objects.all()
        report.refresh_from_db()

        self.assertEqual(len(waste_deposits_qs), 2)
        self.assertEqual(report.waste_deposit.lat, report.lat)
        self.assertEqual(report.waste_deposit.long, report.long)
