import requests
from django.core.exceptions import ObjectDoesNotExist
from .models import ProjectGroup, ProjectMember
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import dateutil.parser
from copy import deepcopy


def update_members(members, project):
    # delete members from DB if not authorized any more
    oh_ids_found = [int(member['project_member_id']) for member in members]
    for db_member in project.projectmember_set.all():
        if db_member.id not in oh_ids_found:
            db_member.delete()

    # update existing member or create if needed
    for oh_member in members:
        try:
            db_member = ProjectMember.objects.get(
                            id=int(oh_member['project_member_id']))
        except ObjectDoesNotExist:
            db_member = ProjectMember(
                                project_id=project.id,
                                id=int(oh_member['project_member_id']))
        db_member.date_joined = dateutil.parser.parse(oh_member['created'])
        db_member.sources_shared = oh_member.get('sources_shared')
        db_member.username = oh_member.get('username')
        db_member.save()
        # fetching old file data for this member
        project_member_old_files = project.file_set.filter(member=db_member)

        for file in oh_member['data']:
            # maintaining a list of obsolete files for this member in database
            project_member_old_files = project_member_old_files.exclude(oh_file_id=file['id'])
            project.file_set.update_or_create(oh_file_id=file['id'],
                                              basename=file['basename'],
                                              created=dateutil.parser.parse(file['created']),
                                              source=file['source'],
                                              member=db_member,
                                              defaults={
                                                  'download_url': file['download_url'],
                                              })
        # deleting obsolete files from database for this member
        project.file_set.filter(id__in=project_member_old_files).delete()


def get_all_members(token):
    req_url = 'https://www.openhumans.org/api/direct-sharing' \
              '/project/members/?access_token={}'.format(token)
    members = requests.get(req_url).json()
    if 'results' in members.keys():
        # results = members['results']
        member_urls = [i['exchange_member'] for i in members['results']]
        while members['next']:
            members = requests.get(members['next']).json()
            for i in members['results']:
                member_urls.append(i['exchange_member'])
        results = []
        for member_url in member_urls:
            member = requests.get(member_url)
            output_member = deepcopy(member)
            while member['next']:
                member = requests.get(member['next'])
                output_member['data'] += member['data']
            results += [output_member]
        return output_member
    else:
        return members


def filter_members_group_id(token, group_id):
    members = get_all_members(token)
    project_group = ProjectGroup.objects.get(pk=group_id)
    group_member_ids = [str(p.id) for p in project_group.projectmember_set.all()]
    filtered_members = []
    for member in members:
        if member['project_member_id'] in group_member_ids:
            filtered_members.append(member)
    return filtered_members


def paginate_items(queryset, page):
    paginator = Paginator(queryset, 25)
    try:
        paged_queryset = paginator.page(page)
    except PageNotAnInteger:
        paged_queryset = paginator.page(1)
    except EmptyPage:
        paged_queryset = paginator.page(paginator.num_pages)
    return paged_queryset


def token_is_valid(token):
    req_url = 'https://www.openhumans.org/api/' \
              'direct-sharing/project/?access_token={}'.format(token)
    project_info = requests.get(req_url).json()
    if 'detail' not in project_info.keys():
        return True
    return False
