import django_filters
from django import forms
from .models import ProjectMember


class MemberFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact')
    date_joined = django_filters.DateTimeFilter(name='date_joined', lookup_expr='gt',
                                                widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),)
    message_permission = django_filters.ChoiceFilter(name='message_permission', choices=((0, 'False'), (1, 'True')))

    class Meta:
        model = ProjectMember
        fields = ['id', 'date_joined', 'sources_shared', 'message_permission', 'groups']
