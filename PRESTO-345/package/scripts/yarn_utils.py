# -*- coding: utf-8 -*-

import commands
import re

INVALID_APPLICATION_ID = 'INVALID_APPLICATION_ID'


def get_yarn_application_id(yarn_application_name):
    output = commands.getoutput('yarn application -list | grep {0}'.format(yarn_application_name))
    line = output.split('\n')[-1]

    if yarn_application_name not in line:
        return INVALID_APPLICATION_ID

    return re.split(r'\s*', line)[0]


def kill_yarn_application(yarn_application_name):
    application_id = get_yarn_application_id(yarn_application_name)
    if application_id == INVALID_APPLICATION_ID:
        return False

    commands.getoutput('yarn application -kill {0}'.format(application_id))
    return True


def is_yarn_application_running(yarn_application_name):
    application_id = get_yarn_application_id(yarn_application_name)
    if application_id == INVALID_APPLICATION_ID:
        return False

    output = commands.getoutput('yarn application -status {0} | grep State'.format(application_id))
    line = output.split('\n')[-2]
    line_split = line.split(':')

    if len(line_split) < 2:
        return False
    else:
        return line_split[-1].strip() == "RUNNING"
