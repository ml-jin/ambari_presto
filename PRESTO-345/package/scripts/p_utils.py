# -*- coding: utf-8 -*-

import commands
import re

INVALID_APPLICATION_ID = 'INVALID_APPLICATION_ID'


def get_presto_id(yarn_application_name):
    output = commands.getoutput('pgrep presto')
    return output


def kill_presto_application(yarn_application_name):
    application_id = get_presto_id(yarn_application_name)
    commands.getoutput('kill -9 {0}'.format(application_id))
    return True


def is_presto_application_running(yarn_application_name):
    application_id = get_presto_id(yarn_application_name)
    if application_id == INVALID_APPLICATION_ID:
        return False

    output = get_presto_id(yarn_application_name)

    if len(output) < 1:
        return False
    else:
        return "RUNNING"
