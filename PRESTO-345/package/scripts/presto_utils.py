# -*- coding: utf-8 -*-

from resource_management import *
import os

FLINK_DIR_NAME = 'presto-345'


# def get_start_yarn_session_cmd(flink_base_dir, yarn_session_name, jm_heap_size, tm_heap_size, slot_count):
#     return '{0} -d -nm {1} -jm {2} -tm {3} -s {4}'.format(os.path.join(flink_base_dir, FLINK_DIR_NAME, 'bin/yarn-session.sh'), yarn_session_name, jm_heap_size, tm_heap_size, slot_count)


def create_symbolic_link():
    import params
    # Link('/bin/yarn-session', to=os.path.join(params.flink_base_dir, FLINK_DIR_NAME, 'bin/yarn-session.sh'))
    Link('/bin/flink', to=os.path.join(params.flink_base_dir, FLINK_DIR_NAME, 'bin/flink'))
