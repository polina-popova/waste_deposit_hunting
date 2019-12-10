import tempfile

from PIL import Image
from django.urls import reverse
from rest_framework.test import APITestCase


class ReportTestCase(APITestCase):

    def test_post_report(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)

        with open(tmp_file.name, 'rb') as photo:
            data = {
                'lat': '64.61833411',
                'long': '40.9587337',
                'photo': photo
            }
            response = self.client.post(
                reverse('reports-list'), data=data
            )

        self.assertEqual(response.status_code, 201)

    def test_report_with_invalid_location(self):
        invalid_lat = '61.932308'
        invalid_long = '37.5152280'

        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)

        with open(tmp_file.name, 'rb') as photo:
            data = {
                'lat': invalid_lat,
                'long': invalid_long,
                'photo': photo
            }
            response = self.client.post(
                reverse('reports-list'), data=data
            )

        self.assertEqual(response.status_code, 400)
