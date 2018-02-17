import requests

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import TokenForm


class HomeView(TemplateView):
    template_name = "oh_proj_management/home.html"

    def get(self, request, *args, **kwargs):
        token = None
        self.member_data = None

        if 'master_access_token' in request.session:
            token = request.session['master_access_token']
            self.member_data = self.token_for_memberlist(token)
            if not self.member_data:
                del request.session['master_access_token']

        if self.member_data:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['member_data'] = self.member_data
        return context

    def token_for_memberlist(self, token):
        req_url = ('https://www.openhumans.org/api/direct-sharing/project/'
                   'members/?access_token={}'.format(token))
        req = requests.get(req_url)
        if req.status_code == 200:
            return req.json()
        else:
            messages.error('Token not valid. Maybe a fresh one is needed?')
            return None


class LoginView(FormView):
    template_name = 'oh_proj_management/login.html'
    form_class = TokenForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        token = form.cleaned_data['token']
        self.request.session['master_access_token'] = token
        return redirect('home')
