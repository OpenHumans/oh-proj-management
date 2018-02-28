from django.urls import path
from django.contrib import admin

from project_admin.views import HomeView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
]
