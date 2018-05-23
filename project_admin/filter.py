import django_filters
from .models import ProjectMember


class MemberFilter(django_filters.FilterSet):
    date_joined = django_filters.NumberFilter(name='date_joined', lookup_expr='year')
    message_permission = django_filters.ChoiceFilter(name='message_permission', choices=((0, 'False'), (1, 'True')))

    class Meta:
        model = ProjectMember
        fields = ['id', 'date_joined', 'sources_shared', 'message_permission', 'groups']
