import requests
import json
import git
from git import RemoteProgress
import os
import urllib.parse
import argparse


class Progress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)


parser = argparse.ArgumentParser(
    description='Get gitlab repos by groups'
)

parser.add_argument(
    '--url',
    default=os.environ.get('GITLAB_URL')
)

parser.add_argument(
    '--token',
    default=os.environ.get('GITLAB_TOKEN')
)

parser.add_argument(
    '--groups',
    default=''
)

parser.add_argument(
    '--base_dir',
    default='Gitlab'
)

args = parser.parse_args()

gitlab_url = args.url
base_dir = args.base_dir
token = args.token
gitlab_groups = args.groups.split(',')

page = 1
gitlab_repos = []
for group in gitlab_groups:
  group_projects = requests.get('https://' + gitlab_url + '/api/v4/groups/' + urllib.parse.quote(group, safe='') + '/projects',
                                params={'simple': 'true', 'per_page': 100, 'include_subgroups': 'true', 'page': page},
                                headers={'PRIVATE-TOKEN': token})
  gitlab_repos += group_projects.json()
  while group_projects.headers['X-Next-Page'] != '':
    group_projects = requests.get('https://' + gitlab_url + '/api/v4/groups/' + urllib.parse.quote(group, safe='') + '/projects',
                                  params={'simple': 'true', 'per_page': 100, 'include_subgroups': 'true', 'page': group_projects.headers['X-Next-Page']},
                                  headers={'PRIVATE-TOKEN': token})
    gitlab_repos += group_projects.json()

for repo in gitlab_repos:
  if not os.path.isdir(base_dir + '/' + repo['path_with_namespace']):
    os.makedirs(base_dir + '/' + repo['path_with_namespace'])
    print('Cloning repo', repo['path_with_namespace'])
    git.Repo.clone_from(repo['ssh_url_to_repo'], base_dir + '/' + repo['path_with_namespace'], progress=Progress())
  else:
    print('Updating repo', repo['path_with_namespace'])
    git_repo = git.Repo(base_dir + '/' + repo['path_with_namespace'])
    git_repo.remotes.origin.pull(progress=Progress())
