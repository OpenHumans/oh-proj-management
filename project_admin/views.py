import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from datetime import timedelta
from django.utils import timezone
from .forms import TokenForm
from .models import Project, ProjectMember, ProjectGroup
from .filter import MemberFilter
from .tasks import download_zip_files, update_project_members, compile_metadata
from .helpers import token_is_valid, paginate_items


class HomeView(ListView):
    template_name = 'project_admin/home.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'home'
        return context

    def get_queryset(self):
        try:
            return Project.objects.get(user=self.request.user)
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
            print(project_info)
            Project.objects.update_or_create(id=project_info['id'],
                                             defaults=project_info)
            update_project_members.delay(project_info['id'])
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


class MembersView(TemplateView):
    template_name = 'project_admin/members.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        project = Project.objects.get(user=self.request.user)
        if token_is_valid(project.token):
            if project.refreshed_at < timezone.now() - timedelta(hours=2):
                update_project_members.delay(project.id)
            member_list = project.projectmember_set.all()
            member_filter = MemberFilter(request.GET, request=request, queryset=member_list)
            members_paged = paginate_items(
                                member_filter.qs,
                                request.GET.get('page'))
            context.update({'page': 'members',
                            'filter': member_filter,
                            'members': members_paged,
                            'project': project,
                            'groups': list(project.projectgroup_set.all())
                            })
            return self.render_to_response(context)
        else:
            messages.error(
                        self.request,
                        ' Your master access token has expired. Please get'
                        ' a new one from the project management interface.', 'danger')
            logout(self.request)
            return redirect('login')


class GroupsView(TemplateView):
    template_name = 'project_admin/groups.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        project = Project.objects.get(user=self.request.user)
        if token_is_valid(project.token):
            if project.refreshed_at < timezone.now() - timedelta(hours=2):
                update_project_members.delay(project.id)
            context.update({'page': 'groups',
                            'members': project.projectmember_set.all(),
                            'groups': project.projectgroup_set.all()})
            return self.render_to_response(context)
        else:
            messages.error(
                        self.request,
                        ' Your master access token has expired. Please get'
                        ' a new one from the project management interface.', 'danger')
            logout(self.request)
            return redirect('login')


class LogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        logout(self.request)
        messages.info(self.request, 'You have been logged out!')
        return redirect('login')


def create_group(request):
    project = Project.objects.get(user=request.user)
    group = project.projectgroup_set.create(
        name=request.POST.get('new_group_name'),
        description=request.POST.get('new_group_description')
    )
    through_model = ProjectMember.groups.through
    through_model.objects.bulk_create([
        through_model(projectgroup=group, projectmember=member)
        for member in project.projectmember_set.filter(
            id__in=request.POST.getlist('selected_members')
        )
    ])
    return redirect('groups')


def update_group(request, group_pk):
    project = Project.objects.get(user=request.user)
    group = project.projectgroup_set.get(pk=group_pk)
    group.name = request.POST.get('group_{}_name'.format(group_pk))
    group.description = request.POST.get('group_{}_description'
                                         .format(group_pk))
    group.save()
    return redirect('groups')


def delete_group(request, group_pk):
    project = Project.objects.get(user=request.user)
    project.projectgroup_set.get(pk=group_pk).delete()
    return redirect('groups')


def add_to_groups(request):
    project = Project.objects.get(user=request.user)
    member = project.projectmember_set.get(pk=request.POST.get('member_pk'))
    through_model = ProjectMember.groups.through
    through_model.objects.bulk_create([
        through_model(projectgroup=group, projectmember=member)
        for group in project.projectgroup_set.filter(
            id__in=request.POST.getlist('selected_groups')
        )
    ])
    return redirect('members')


def group_modal_body(request, member_id):
    member = ProjectMember.objects.get(pk=member_id)
    return render(request, 'project_admin/group_modal_body.html', {
                'member': member})


def group_modal_add_body(request, member_id):
    member = ProjectMember.objects.get(pk=member_id)
    groups = ProjectGroup.objects.filter(project=member.project)
    return render(request, 'project_admin/group_modal_add_body.html', {
                'member': member, 'groups': groups})


def files_modal_body(request, member_id):
    member = ProjectMember.objects.get(pk=member_id)
    return render(request, 'project_admin/files_modal_body.html', {
                'member': member})


def notes_modal_body(request, member_id):
    member = ProjectMember.objects.get(pk=member_id)
    return render(request, 'project_admin/notes_modal_body.html', {
                'member': member})


def notes_modal_add_body(request, member_id):
    member = ProjectMember.objects.get(pk=member_id)
    return render(request, 'project_admin/notes_modal_add_body.html', {
                'member': member})


def remove_member(request, group_id, member_id):
    project = Project.objects.get(user=request.user)
    group = project.projectgroup_set.get(pk=group_id)
    member = project.projectmember_set.get(id=member_id)
    through_model = ProjectMember.groups.through
    through_model.objects.filter(
        projectgroup=group, projectmember=member
    ).delete()
    return redirect('members')


def create_note(request, member_id):
    project = Project.objects.get(user=request.user)
    projectmember = ProjectMember.objects.get(pk=member_id)
    project.note_set.create(
        title=request.POST.get('new_note_title'),
        description=request.POST.get('new_note_description'),
        member=projectmember)
    return redirect('members')


def update_note(request, note_id):
    project = Project.objects.get(user=request.user)
    note = project.note_set.get(pk=note_id)
    note.title = request.POST.get('note_{}_title'.format(note.id))
    note.description = request.POST.get('note_{}_description'.format(note.id))
    note.save()
    return redirect('members')


def delete_note(request, note_id):
    project = Project.objects.get(user=request.user)
    project.note_set.get(pk=note_id).delete()
    return redirect('members')


def download_zip_file(request):
    task = download_zip_files.delay(request.user.id)
    messages.info(request, 'File download started with task id: ' + str(task.id) +
                  '. You will receive an email shortly.')
    return redirect('members')


def download_metadata(request):
    task = compile_metadata.delay(request.user.id)
    messages.info(request, 'File download started with task id: ' + str(task.id) +
                  '. You will receive an email shortly.')
    return redirect('members')


def download_zip_file_group(request, group_pk):
    group = ProjectGroup.objects.get(pk=group_pk)
    if group.project.user.id == request.user.id:
        task = download_zip_files.delay(request.user.id, group_pk)
        messages.info(
                request,
                'File download started with task id: ' + str(task.id) +
                '. You will receive an email shortly.')
    return redirect('groups')


def batch_processing(request):
    print(request.POST)
    valid_filters = [
                        'file_count', 'id',
                        'sources_shared', 'groups', 'date_joined']
    filter_params = {}
    for f in valid_filters:
        if request.POST.get(f, ''):
            if f == 'date_joined':
                filter_params['date_joined__gte'] = request.POST.get(f)
            else:
                filter_params[f] = request.POST.get(f)
    filtered_members = ProjectMember.objects.filter(**filter_params)
    project = Project.objects.get(user=request.user)
    group = project.projectgroup_set.create(
        name='Bulk created group',
        description='This is a bulk created group, edit to change the name/description'
    )
    through_model = ProjectMember.groups.through
    through_model.objects.bulk_create([
        through_model(projectgroup=group, projectmember=member)
        for member in filtered_members
    ])
    if request.POST.get('download'):
        task = download_zip_files.delay(request.user.id, group.pk)
        messages.info(
                request,
                'File download started with task id: ' + str(task.id) +
                '. You will receive an email shortly.')
    else:
        messages.info(
                request,
                'Created new bulk group. See Groups menu to change its name')
    return redirect('members')
