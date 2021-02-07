# -*- coding: utf-8 -*-
import smtplib
import src.configs.config as config


def SendEmail(to, subject, message):

    body = "\r\n".join((
        "From: %s" % config.MAIL_FROM,
        "To: %s" % to,
        "Subject: %s" % subject,
        "",
        message
    ))

    server = smtplib.SMTP(config.SMTP_SERVER)
    server.sendmail(config.MAIL_FROM, [to], body)
    server.quit()
