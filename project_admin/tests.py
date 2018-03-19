from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project


@override_settings(AUTHENTICATION_BACKENDS=('django.contrib.auth.backends.ModelBackend',))
class HomeViewTest(TestCase):

    @classmethod
    def setUp(self):
        kwargs = {
            "active": True,
            "approved": False,
            "authorized_members": 5,
            "contact_email": "tester@openhumans.com",
            "id_label": "Label",
            "info_url": "openhumans.org",
            "is_academic_or_nonprofit": True,
            "is_study": True,
            "leader": "Admin",
            "long_description": "Just a test object",
            "name": "TestModel",
            "organization": "Testing",
            "request_message_permission": True,
            "request_sources_access": "Sources used in the project",
            "request_username_access": True,
            "returned_data_description": "project data",
            "short_description": "test",
            "type": "Testing purpose",
            "token": "XitlFDXBqm5TRK8Vuh3Ey2cDFdiTWz7amKpot97H9Xfgak1qpvray0b0arQ"
        }

        self.test_user = User.objects.create_user(username="test", password='12')
        kwargs['user'] = self.test_user
        self.project = Project.objects.create(**kwargs)

    def test_home_with_login(self):
        self.client.force_login(self.test_user)
        resp = self.client.get(reverse('home'))
        self.assertEquals(resp.context_data['project_list'], self.project)
        self.assertTemplateUsed(resp, 'project_admin/home.html')

    def test_home_with_login_unknown_user(self):
        self.client.login(username="unknown_test_user", password="unknown")
        resp = self.client.get(reverse('home'))
        self.assertRedirects(resp, '/login/?next=/')

    def test_home_without_login(self):
        resp = self.client.get(reverse('home'))
        self.assertRedirects(resp, '/login/?next=/')
