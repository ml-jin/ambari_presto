# -*- coding: utf-8 -*-

from resource_management import *
import os

PRESTO_DIR_NAME = 'presto-server-345'


def create_symbolic_link():
    import params
    Link('/bin/launcher', to=os.path.join(params.presto_base_dir, PRESTO_DIR_NAME, 'bin/launcher'))
