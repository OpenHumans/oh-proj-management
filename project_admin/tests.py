from django.test import TestCase
import requests
import vcr


class ProjectTest(TestCase):

    def setUp(self):
        self.token = 'XitlFDXBqm5TRK8Vuh3Ey2cDFdiTWz7amKpot97H9Xfgak1qpvray0b0arQhvpEP'
        self.url = 'https://www.openhumans.org/api/direct-sharing/project/members/?access_token={}'.format(
        	self.token)

    @vcr.use_cassette('tests/members.yml')
    def test_members_request(self):
        """memebers list API"""
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)
