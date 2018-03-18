from django.test import TestCase
import vcr
import requests
from django.urls import reverse

my_vcr = vcr.VCR(path_transformer=vcr.VCR.ensure_suffix('.yaml'), cassette_library_dir='project_admin/cassettes')


class LoginTest(TestCase):

    def setUp(self):
        self.invalid_token = 'INVALID_TOKEN'
        self.master_token = 'XitlFDXBqm5TRK8Vuh3Ey2cDFdiTWz7amKpot97H9Xfgak1qpvray0b0arQhvpEP'

    @my_vcr.use_cassette()
    def test_invalid_token(self):
        project_info_url = ('https://www.openhumans.org/api/direct-sharing/project/?access_token={}'
                            .format(self.invalid_token))
        response = requests.get(project_info_url)
        self.assertEqual(response.status_code, 401)

    @my_vcr.use_cassette()
    def test_valid_token(self):
        project_info_url = ('https://www.openhumans.org/api/direct-sharing/project/?access_token={}'
                            .format(self.master_token))
        response = requests.get(project_info_url)
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(reverse('login'), {'token': self.master_token}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project_admin/home.html', 'project_admin/base.html')
        self.assertRedirects(response, '/')

    def test_login_fail(self):
        response = self.client.post(reverse('login'), {'token': self.invalid_token}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Check your token in the project management interface")
        self.assertTemplateUsed(response, 'project_admin/login.html')
        self.assertRedirects(response, '/login/')
