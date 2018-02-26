import requests

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login

from .forms import TokenForm
from .models import Project


class HomeView(TemplateView):
    template_name = "project_admin/home.html"

    def get(self, request, *args, **kwargs):
        token = None
        self.member_data = None

        if 'master_access_token' in request.session:
            token = request.session['master_access_token']
            self.member_data = self.token_for_memberlist(token)
            self.token = token
            if not self.member_data:
                del request.session['master_access_token']

        if self.member_data:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_data'] = self.member_data
        context['Project'] = Project.objects.get(token = self.token)
        return context

    def token_for_memberlist(self, token):
        req_url = ('https://www.openhumans.org/api/direct-sharing/project/'
                   'members/?access_token={}'.format(token))
        req = requests.get(req_url)
        if req.status_code == 200:
            return req.json()
        else:
            messages.error(self.request, 'Token not valid. Maybe a fresh one is needed?')
            return None


class LoginView(FormView):
    template_name = 'project_admin/login.html'
    form_class = TokenForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        token = form.cleaned_data['token']
        req_url = ("https://www.openhumans.org/api/direct-sharing/project/?access_token={}".format(token))
        params = {'token': token}
        project_info = requests.get(req_url, params=params).json()
        try:
            if not User.objects.filter(username=project_info['id_label']).exists():
                user = User.objects.create_user(username = project_info['id_label'])
            else:
                user = User.objects.get(username = project_info['id_label'])
            project_info['user'] = user
            Project.objects.update_or_create(id=project_info['id'], defaults=project_info)
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            self.request.session['master_access_token'] = token
        except Exception as e:
            # Handle expired master tokens, or serve error message
            if 'detail' in project_info:
                messages.error(self.request, project_info['detail'] + 'Check your token in the project management interface.')
            else:
                messages.error(self.request, e)
        return redirect('home')
