from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from project_admin.views import HomeView, MembersView, GroupsView, LoginView, LogoutView, \
    create_group, update_group, delete_group, add_to_groups, remove_member, create_note, update_note, \
    delete_note, download_zip_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(HomeView.as_view(), login_url='login/'),
         name='home'),
    path('members/', MembersView.as_view(), name='members'),
    path('groups/', GroupsView.as_view(), name='groups'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create_group/', create_group, name='create_group'),
    path('update_group/<int:group_pk>', update_group, name='update_group'),
    path('delete_group/<int:group_pk>/', delete_group, name='delete_group'),
    path('add_to_groups/', add_to_groups, name='add_to_groups'),
    path('remove_member/<int:group_id>/<int:member_id>/', remove_member,
         name='remove_member'),
    path('create_note/<int:member_id>', create_note, name='create_note'),
    path('update_note/<int:note_id>', update_note, name='update_note'),
    path('delete_note/<int:note_id>', delete_note, name='delete_note'),
    path('download_zip_file', download_zip_file, name='download_zip_file'),
]
