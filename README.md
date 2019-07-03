Gitlab gt clone repositories by group
===================

Script to get gitlab repositories in groups

Requirements
------------

```bash
pip install gitpython requests
```

Variables
------------

`url` - Gitlab url - default from `GITLAB_URL` environment variable
`token` - Gitlab token to access Gitlab - default from `GITLAB_TOKEN` environment variable
`groups` - Gitlab groups wheere lookup repositories - default empty
`base_dir` - directory to clone repos - default `./Gitlab`

Usage
--------------

```bash
./gitlab.py --url=gitlab.example.com --token=SUPER_SECRET_GITLAB_TOKEN --groups first-group,second_group,third,group --base_dir gitlab_dir
```
