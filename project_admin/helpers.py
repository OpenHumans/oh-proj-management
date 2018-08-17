import requests
from .models import ProjectGroup


def get_all_members(token):
    req_url = 'https://www.openhumans.org/api/direct-sharing' \
              '/project/members/?access_token={}'.format(token)
    members = requests.get(req_url).json()['results']
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
