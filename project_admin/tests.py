from django.test import TestCase
from .models import Project


class ProjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
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
        Project.objects.create(**kwargs)


    def test_activity(self):
        project = Project.objects.get(id=1)
        activity = project.active
        print(activity)
        self.assertEquals(activity, True)

    def test_approval(self):
        project = Project.objects.get(id=1)
        approval = project.approved
        self.assertEquals(approval, False)

    def test_authorized_members(self):
        project = Project.objects.get(id=1)
        members = project.authorized_members
        self.assertEquals(members, 5)

    def test_contact_email(self):
        project = Project.objects.get(id=1)
        email = project.contact_email
        self.assertEquals(email, "tester@openhumans.com")

    def test_id_label(self):
        project = Project.objects.get(id=1)
        label = project.id_label
        self.assertEquals(label, "Label")
        self.assertLessEqual(len(label), 50)

    def test_info_url(self):
        project = Project.objects.get(id=1)
        url = project.info_url
        self.assertEquals(url, "openhumans.org")
        self.assertLessEqual(len(url), 200)

    def test_is_academic_or_nonprofit(self):
        project = Project.objects.get(id=1)
        type = project.is_academic_or_nonprofit
        self.assertEquals(type, True)

    def test_is_study(self):
        project = Project.objects.get(id=1)
        type = project.is_study
        self.assertEquals(type, True)

    def test_leader(self):
        project = Project.objects.get(id=1)
        leader = project.leader
        self.assertEquals(leader, "Admin")
        self.assertLessEqual(len(leader), 50)

    def test_long_description(self):
        project = Project.objects.get(id=1)
        long_description = project.long_description
        self.assertEquals(long_description, "Just a test object")

    def test_name(self):
        project = Project.objects.get(id=1)
        name = project.name
        self.assertEquals(name, "TestModel")
        self.assertLessEqual(len(name), 50)

    def test_organization(self):
        project = Project.objects.get(id=1)
        organization = project.organization
        self.assertEquals(organization, "Testing")
        self.assertLessEqual(len(organization), 200)

    def test_request_message_permission(self):
        project = Project.objects.get(id=1)
        permission = project.request_message_permission
        self.assertEquals(permission, True)

    def test_request_sources_access(self):
        project = Project.objects.get(id=1)
        access = project.request_sources_access
        self.assertEquals(access, "Sources used in the project")

    def test_request_username_access(self):
        project = Project.objects.get(id=1)
        access = project.request_username_access
        self.assertEquals(access, True)

    def test_returned_data_description(self):
        project = Project.objects.get(id=1)
        description = project.returned_data_description
        self.assertEquals(description, "project data")
        self.assertLessEqual(len(description), 200)

    def test_short_description(self):
        project = Project.objects.get(id=1)
        short_description = project.short_description
        self.assertEquals(short_description, 'test')
        self.assertLessEqual(len(short_description), 200)

    def test_type(self):
        project = Project.objects.get(id=1)
        type = project.type
        self.assertEquals(type, "Testing purpose")
        self.assertLessEqual(len(type), 50)

    def test_token(self):
        project = Project.objects.get(id=1)
        token = project.token
        self.assertEquals(token, "XitlFDXBqm5TRK8Vuh3Ey2cDFdiTWz7amKpot97H9Xfgak1qpvray0b0arQ")
        self.assertLessEqual(len(token), 100)
