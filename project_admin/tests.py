from django.test import TestCase
from django.test import Client
import requests
import requests_mock


class ProjectTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.token = 'XitlFDXBqm5TRK8Vuh3Ey2cDFdiTWz7amKpot97H9Xfgak1qpvray0b0arQhvpEP'
        self.url = 'https://www.openhumans.org/api/direct-sharing/project/?access_token={}'.format(
            self.token)

    def test_member_list_view(self):
        with requests_mock.Mocker() as mock:
            response = mock.get(self.url)
            response = requests.get(self.url)
            self.assertEqual(response.status_code, 200)
