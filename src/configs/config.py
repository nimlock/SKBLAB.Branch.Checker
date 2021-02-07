# -*- coding: utf-8 -*-

GITLAB = {
    "base_url": "http://gitlab.testsite.ru",
    "immutable_branches": [
        "master",
        "develop"
    ],
    "desired_pattern": r'^(feature|bugfix)/task-\d+$',
    "max_age_days": 14
}

RENAME_MAIL_TEMPLATE = "Переименуй!"

FORGOTTEN_MAIL_TEMPLATE = "Обнови или удали!"

JSON_FILE_EXCEPTIONS = "exceptions.json"

SMTP_SERVER = "someSMTP.server.ru"
MAIL_FROM = "BranchChecker@testsite.ru"
