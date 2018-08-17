import requests


def get_all_members(token):
    req_url = 'https://www.openhumans.org/api/direct-sharing' \
              '/project/members/?access_token={}'.format(token)
    members = requests.get(req_url).json()['results']
    return members
