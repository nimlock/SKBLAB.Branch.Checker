#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import src.RepoHandler as RepoHandler


def main():
    """
    Метод запускает процедуры проверки веток на соответствие требованиям и отправки уведомлений
    Возвращает void
    """

    # список объектов на основе записей в словаре проектов
    summary_list = RepoHandler.seeder()

    # заполнить из GitLab список объектов-веток (кроме исключений) в объектах-репозиториях
    RepoHandler.filler(summary_list)

    # проходим по всем объектам-репозиториям:
    # 1) прочитать исключения из файла
    # 2) заполнить в объектах список веток не соответствующих шаблону, объект добавить в спец.список
    # 3) заполнить в объектах список устаревших веток, объект добавить в спец.список
    # 4) записать исключения в файл
    RepoHandler.handle(summary_list)

    # отправка уведомлений о найденных проблемах
    RepoHandler.sender(summary_list)


main()
