from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    active = models.BooleanField()
    approved = models.BooleanField()
    authorized_members = models.IntegerField()
    badge_image = models.URLField(max_length=200, blank=True, null=True)
    contact_email = models.EmailField(max_length=200)
    id = models.AutoField(primary_key=True)
    id_label = models.CharField(max_length=50)
    info_url = models.URLField(max_length=200, blank=True)
    is_academic_or_nonprofit = models.BooleanField()
    is_study = models.BooleanField()
    leader = models.CharField(max_length=50)
    long_description = models.TextField()
    name = models.CharField(max_length=50)
    organization = models.CharField(max_length=200, blank=True)
    request_message_permission = models.BooleanField()
    request_sources_access = models.TextField()
    request_username_access = models.BooleanField()
    returned_data_description = models.CharField(max_length=200, blank=True)
    short_description = models.TextField()
    slug = models.SlugField(max_length=50)
    type = models.CharField(max_length=50)
    token = models.CharField(max_length=50)


class ProjectGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class ProjectMember(models.Model):
    id = models.IntegerField(primary_key=True)
    date_joined = models.DateTimeField()
    sources_shared = models.CharField(max_length=1000, null=True)
    message_permission = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    groups = models.ManyToManyField(ProjectGroup)


class File(models.Model):
    id = models.IntegerField(primary_key=True)
    basename = models.CharField(max_length=200)
    created = models.DateTimeField()
    download_url = models.URLField(max_length=200)
    source = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(ProjectMember, on_delete=models.CASCADE)
