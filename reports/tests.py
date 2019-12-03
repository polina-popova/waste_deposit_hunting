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
                "location": "Point (12.492324113849 41.890307434153)",
                'photo': photo
            }
            response = self.client.post(
                reverse('reports-list'), data=data
            )

        self.assertEqual(response.status_code, 201)
