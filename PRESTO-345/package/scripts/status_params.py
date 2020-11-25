# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Presto  service params
"""
from resource_management import *

config = Script.get_config()

es_master_pid_dir = config['configurations']['elasticsearch-env']['elasticsearch.pid.dir'] + '/master'
es_master_pid_file = format("{es_master_pid_dir}/elasticsearch-master.pid")

# es_slave_pid_dir = config['configurations']['elasticsearch-env']['elasticsearch.pid.dir'] + '/slave'
# es_slave_pid_file = format("{es_slave_pid_dir}/elasticsearch-slave.pid")
def get_status_slave_pid_file(slave_case):
    es_slave_pid_dir = config['configurations']['elasticsearch-env']['elasticsearch.pid.dir'] + '/' + slave_case
    return format("{es_slave_pid_dir}/elasticsearch-slave.pid")
