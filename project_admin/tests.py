from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project
import vcr
my_vcr = vcr.VCR(path_transformer=vcr.VCR.ensure_suffix('.yaml'), cassette_library_dir='project_admin/cassettes')


@override_settings(AUTHENTICATION_BACKENDS=('django.contrib.auth.backends.ModelBackend',))
class MemberViewTest(TestCase):

    @classmethod
    def setUp(self):
        self.kwargs = {
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
            "token": "XitlFDXBqm5TRK8Vuh3Ey2cDFdiTWz7amKpot97H9Xfgak1qpvray0b0arQhvpEP"
        }

        self.test_user = User.objects.create_user(username="test", password='12')
        self.kwargs['user'] = self.test_user

    @my_vcr.use_cassette()
    def test_member_with_user_project(self):
        self.project = Project.objects.create(**self.kwargs)
        self.client.force_login(self.test_user)
        resp = self.client.get(reverse('members'))
        self.assertTemplateUsed(resp, 'project_admin/members.html')

    @my_vcr.use_cassette()
    def test_member_with_user_without_project(self):
        self.client.force_login(self.test_user)
        self.assertRaises(Project.DoesNotExist, self.client.get, (reverse('members')))

    @my_vcr.use_cassette()
    def test_member_no_user(self):
        self.assertRaises(TypeError, self.client.get, (reverse('members')))
