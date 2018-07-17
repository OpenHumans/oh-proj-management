import django_filters
from django import forms
from .models import Project, ProjectGroup, ProjectMember


def groups_joined(request):
    if request is None:
        return ProjectGroup.objects.none()
    project = Project.objects.get(user=request.user)
    return project.projectgroup_set.all()


class MemberFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact', label='Member ID')
    date_joined = django_filters.DateTimeFilter(name='date_joined', lookup_expr='gt',
                                                widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),)
    groups = django_filters.ModelChoiceFilter(label='Groups Joined', queryset=groups_joined)
    file_count = django_filters.CharFilter(label='Number of Files Shared')
    sources_shared = django_filters.CharFilter(label='Sources Authorized')

    class Meta:
        model = ProjectMember
        fields = ['id', 'date_joined', 'sources_shared', 'message_permission', 'file_count', 'groups']
