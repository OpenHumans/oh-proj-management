from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import TokenForm


class HomeView(TemplateView):
    template_name = "oh_proj_management/home.html"

    def get(self, request, *args, **kwargs):
        if 'master_access_token' in request.session:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['master_access_token'] = self.request.session[
            'master_access_token']
        return context


class LoginView(FormView):
    template_name = 'oh_proj_management/login.html'
    form_class = TokenForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        token = form.cleaned_data['token']
        self.request.session['master_access_token'] = token
        return redirect('home')
