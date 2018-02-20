#oh_proj_management URL Configuration

from django.urls import path
from django.contrib import admin
#from django.contrib.auth import views as auth_views

from project_admin.views import HomeView, LoginView, SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
