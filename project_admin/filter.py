import django_filters
from django import forms
from .models import Project, ProjectGroup, ProjectMember, File


def groups_joined(request):
    if request is None:
        return ProjectGroup.objects.none()
    project = Project.objects.get(user=request.user)
    return project.projectgroup_set.all()


def number_files_shared():
    project_members = ProjectMember.objects.all()
    file_numbers = project_members.values_list(
        'file_count', flat=True)
    file_numbers = tuple((value, value) for value in set(file_numbers))
    return list(file_numbers)


class MemberFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact', label='Member ID')
    date_joined = django_filters.DateTimeFilter(name='date_joined', lookup_expr='gt',
                                                widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),)
    groups = django_filters.ModelChoiceFilter(label='Groups Joined', queryset=groups_joined)
    file_count = django_filters.ChoiceFilter(label='Number of Files Shared', choices=number_files_shared())
    sources_shared = django_filters.CharFilter(label='Sources Authorized')

    class Meta:
        model = ProjectMember
        fields = ['id', 'date_joined', 'sources_shared', 'message_permission', 'file_count', 'groups']
