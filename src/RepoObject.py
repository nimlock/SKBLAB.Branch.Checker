import re
from datetime import timedelta, datetime

class RepoObject:
    """
    Класс описывает репозитории в GitLab
    """

    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.branches = []
        self.uglu_branches = []
        self.forgotten_branches = []

    def find_ugly_branches(self, desired_pattern, exceptions):
        """
        Метод проверяет имена веток на соответствие шаблону и заполняет список несоответствующих.
        """

        for branch in self.branches:
            if not re.match(desired_pattern, branch.name) and branch.name not in exceptions:
                self.uglu_branches.append(branch)

    def find_forgotten_branches(self, max_age_days, exceptions):
        """
        Метод проверяет дату последнего коммита в ветку и заполняет список устаревших.
        """

        for branch in self.branches:
            if branch.name not in exceptions:
                now = datetime.now()
                last_commit_date_str = re.search(r'^(.+)(\+\d{2}:\d{2})', branch.commit['committed_date']).group(1)
                last_commit_date_obj = datetime.strptime(last_commit_date_str, '%Y-%m-%dT%H:%M:%S.%f')
                delta = now - last_commit_date_obj
                if delta.days > max_age_days:
                    self.forgotten_branches.append(branch)
