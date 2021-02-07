# -*- coding: utf-8 -*-
import src.configs.dictionary as dictionary
import src.configs.config as config
from src.RepoObject import RepoObject
from src.SendEmail import SendEmail
import gitlab   # pip3 install python-gitlab
import json


def seeder():
    """
    Создание списка объектов на основе записей из DICTIONARY
    """

    summary_list = []
    for item in dictionary.dictionary:
        summary_list.append(RepoObject(item))
    return summary_list


def filler(summary_list):

    gl = gitlab.Gitlab(config.GITLAB["base_url"])

    for repo_object in summary_list:
        project = gl.projects.get(repo_object.repo_name)
        branches = project.branches.list()
        for branch in branches:
            if branch.name not in config.GITLAB["immutable_branches"]:
                repo_object.branches.append(branch)


def handle(summary_list):

    # Пробуем считать ветки-исключения из файла
    try:
        with open(config.JSON_FILE_EXCEPTIONS, 'r') as f:
            exceptions = json.load(f)
    except FileNotFoundError:
        print('[INFO] Existing exceptions not found!')
        exceptions = {
            'names': {},
            'dates': {}
        }

    for repo_object in summary_list:

        exceptions_names = exceptions['names'].pop(repo_object.repo_name, [])
        exceptions_dates = exceptions['dates'].pop(repo_object.repo_name, [])

        repo_object.find_ugly_branches(config.GITLAB["desired_pattern"], exceptions_names)
        repo_object.find_forgotten_branches(config.GITLAB["max_age_days"], exceptions_dates)

        for branch in repo_object.uglu_branches:
            exceptions_names.append(branch.name)
        for branch in repo_object.forgotten_branches:
            exceptions_dates.append(branch.name)

        if exceptions_names:
            exceptions['names'][repo_object.repo_name] = exceptions_names
        if exceptions_dates:
            exceptions['dates'][repo_object.repo_name] = exceptions_dates

    with open(config.JSON_FILE_EXCEPTIONS, 'w') as f:
        json.dump(exceptions, f, indent='  ')


def sender(summary_list):

    for repo_object in summary_list:

        for branch in repo_object.uglu_branches:
            to = branch.commit['committer_email']
            subject = config.RENAME_MAIL_TEMPLATE
            message = 'Dear {}, there is problem with branch {}/{}.'.format(branch.commit['committer_name'],
                                                                            repo_object.repo_name,
                                                                            branch.name)
            SendEmail(to, subject, message)

        for branch in repo_object.forgotten_branches:
            to = branch.commit['committer_email']
            subject = config.FORGOTTEN_MAIL_TEMPLATE
            message = 'Dear {}, there is problem with branch {}/{}.'.format(branch.commit['committer_name'],
                                                                            repo_object.repo_name,
                                                                            branch.name)
            SendEmail(to, subject, message)
