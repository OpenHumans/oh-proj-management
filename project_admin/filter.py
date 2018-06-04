import django_filters
from django import forms
from .models import Project, ProjectGroup, ProjectMember

def groups_joined(request):
    if request is None:
        return ProjectGroup.objects.none()
    project = Project.objects.get(user=
    request.user)
    return project.projectgroup_set.all()

class MemberFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact', label='Member Id')
    date_joined = django_filters.DateTimeFilter(name='date_joined', lookup_expr='gt',
                                                widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),)
    message_permission = django_filters.ChoiceFilter(name='message_permission', choices=((0, 'False'), (1, 'True')))
    groups= django_filters.ModelChoiceFilter(label='Groups Joined', queryset=groups_joined)


    class Meta:
        model = ProjectMember
        fields = ['id', 'date_joined', 'sources_shared', 'message_permission', 'groups']