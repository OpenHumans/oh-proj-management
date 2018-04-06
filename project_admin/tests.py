from django.test import TestCase
import vcr
import requests
from django.urls import reverse
from django.conf import settings

FILTERSET = [('access_token', 'ACCESSTOKEN')]

my_vcr = vcr.VCR(path_transformer=vcr.VCR.ensure_suffix('.yaml'), 
                 cassette_library_dir='project_admin/cassettes',
                 filter_headers=[('Authorization', 'XXXXXXXX')],
                 filter_query_parameters=FILTERSET,
                 filter_post_data_parameters=FILTERSET)

class ProjectTest(TestCase):
    def setUp(self):
        settings.DEBUG = True
        self.token = 'ACCESSTOKEN'
        self.url = 'https://www.openhumans.org/api/direct-sharing/project/members/?access_token={}'.format(
                    self.token)

    @my_vcr.use_cassette()
    def test_members_request(self):
        """memebers list API"""
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)


class LoginTest(TestCase):

    def setUp(self):
        settings.DEBUG = True
        self.invalid_token = 'INVALID_TOKEN'
        self.master_token = 'ACCESSTOKEN'
        self.project_info_url = 'https://www.openhumans.org/api/direct-sharing/project/?access_token={}'

    @my_vcr.use_cassette()
    def test_invalid_token(self):
        request_url = self.project_info_url.format(self.invalid_token)
        response = requests.get(request_url)
        self.assertEqual(response.status_code, 401)

    @my_vcr.use_cassette()
    def test_valid_token(self):
        request_url = self.project_info_url.format(self.master_token)
        response = requests.get(request_url)
        self.assertEqual(response.status_code, 200)

    @my_vcr.use_cassette()
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
