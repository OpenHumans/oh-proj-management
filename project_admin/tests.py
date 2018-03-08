from django.test import TestCase
from django.test import Client


# Create your tests here.

class ProjectTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.token = 'XitlFDXBqm5TRK8Vuh3Ey2cDFdiTWz7amKpot97H9Xfgak1qpvray0b0arQhvpEP'

    def test_member_list_view(self):
        url = 'https://www.openhumans.org/api/direct-sharing/project/members/'
        print(url)
        response = self.client.get(
            url, {'access_token': self.token}, format='json')
        self.assertEqual(response.status_code, 200)
