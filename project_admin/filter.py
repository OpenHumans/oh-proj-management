import django_filters
from django import forms
from django.db.models import Count
from .models import Project, ProjectGroup, ProjectMember, File


def groups_joined(request):
    if request is None:
        return ProjectGroup.objects.none()
    project = Project.objects.get(user=request.user)
    return project.projectgroup_set.all()


def number_files_shared(request):
    if request is None:
        return File.objects.none()
    project = Project.objects.get(user=request.user)
    projectmember = project.projectmember_set.all()
    return projectmember.annotate(file_count=Count('file')).values_list('file_count', flat=True)


class MemberFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact', label='Member ID')
    date_joined = django_filters.DateTimeFilter(name='date_joined', lookup_expr='gt',
                                                widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),)
    groups = django_filters.ModelChoiceFilter(label='Groups Joined', queryset=groups_joined)
    files = django_filters.ModelChoiceFilter(label='Number of Files Shared', queryset=number_files_shared)
    sources_shared = django_filters.CharFilter(label='Sources Authorized')

    class Meta:
        model = ProjectMember
        fields = ['id', 'date_joined', 'sources_shared', 'message_permission', 'files', 'groups']
