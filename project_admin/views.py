import requests
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .forms import TokenForm
from .models import Project


class HomeView(ListView):
    template_name = "project_admin/home.html"
    context_object_name = 'project_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'home'
        return context

    def get_queryset(self):
        try:
            self.user = self.request.user
            self.project_list = Project.objects.get(user=self.user)
            return self.project_list
        except Project.DoesNotExist:
            return redirect('login')


class LoginView(FormView):
    template_name = 'project_admin/login.html'
    form_class = TokenForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'login'
        return context

    def form_valid(self, form):
        token = form.cleaned_data['token']
        req_url = 'https://www.openhumans.org/api/' \
                  'direct-sharing/project/?access_token={}'.format(token)
        project_info = requests.get(req_url).json()
        try:
            user = User.objects.get_or_create(
                username=project_info['id_label']
            )[0]
            project_info['user'] = user
            project_info['token'] = token
            Project.objects.update_or_create(id=project_info['id'],
                                             defaults=project_info)
            login(self.request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        except Exception as e:
            # Handle expired master tokens, or serve error message
            if 'detail' in project_info:
                messages.error(self.request, project_info['detail'] +
                               ' Check your token in the'
                               ' project management interface.', 'danger')
            else:
                messages.error(self.request, e, 'danger')
            return redirect('login')


class MembersView(ListView):
    template_name = 'project_admin/members.html'
    context_object_name = 'members'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'members'
        return context

    def get_queryset(self):
        project_list = Project.objects.get(user=self.request.user)
        token = project_list.token
        req_url = 'https://www.openhumans.org/api/direct-sharing' \
                  '/project/members/?access_token={}'.format(token)
        member_info = requests.get(req_url).json()
        try:
            members = member_info['results']
            for member in members:
                member['uid'] = member.get(
                    'username', member['project_member_id'])
            return members
        except Exception as e:
            if 'detail' in member_info:
                messages.error(self.request, member_info['detail'] +
                               ' Check your token in the'
                               ' project management interface.', 'danger')
            else:
                messages.error(self.request, e, 'danger')
            return redirect('login')


class LogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, 'You have been logged out!')
        return redirect('login')
