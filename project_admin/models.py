from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


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
    token = models.CharField(max_length=65)
    refreshed_at = models.DateTimeField(auto_now=True)


class ProjectGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default='')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProjectMemberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            file_count=Count('file')
        )


class ProjectMember(models.Model):
    id = models.IntegerField(primary_key=True)
    date_joined = models.DateTimeField()
    sources_shared = models.CharField(max_length=1000, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    groups = models.ManyToManyField(ProjectGroup)
    objects = ProjectMemberManager()
    username = models.CharField(max_length=200, null=True)


class File(models.Model):
    oh_file_id = models.IntegerField()
    basename = models.CharField(max_length=200)
    created = models.DateTimeField()
    download_url = models.URLField(max_length=512)
    source = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(ProjectMember, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('oh_file_id', 'project')


class Note(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(ProjectMember, on_delete=models.CASCADE)


class S3Upload(models.Model):
    key = models.CharField(max_length=260)
    created_at = models.DateTimeField(auto_now_add=True)
