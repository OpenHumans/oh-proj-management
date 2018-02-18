from .views import HomeView, LoginView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/?$', LoginView.as_view(), name='login'),
]