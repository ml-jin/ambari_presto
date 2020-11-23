# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Flink Params configurations
"""

# from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *
# from resource_management.core.logger import Logger
import os
import repoin

config = Script.get_config()

FLINK_TAR_NAME = 'flink-1.8.1-bin-scala_2.11.tgz'

flink_conf = config['configurations']['flink-conf']

flink_user = flink_conf['flink_user']
flink_group = flink_conf['flink_group']

flink_download_url = os.path.join(repoin.baseurl, 'flink', FLINK_TAR_NAME)

flink_base_dir = flink_conf['flink_base_dir']

# Common

jobmanager_rpc_address = flink_conf['jobmanager_rpc_address']
jobmanager_rpc_port = flink_conf['jobmanager_rpc_port']
jobmanager_heap_size = flink_conf['jobmanager_heap_size'] + 'm'
taskmanager_heap_size = flink_conf['taskmanager_heap_size'] + 'm'
taskmanager_numberOfTaskSlots = flink_conf['taskmanager_numberOfTaskSlots']
parallelism_default = flink_conf['parallelism_default']
fs_default_scheme = flink_conf['fs_default_scheme']

# High Availability
high_availability = flink_conf['high_availability']
high_availability_storageDir = flink_conf['high_availability_storageDir']
high_availability_zookeeper_quorum = flink_conf['high_availability_zookeeper_quorum']
high_availability_zookeeper_client_acl = flink_conf['high_availability_zookeeper_client_acl']

# Fault tolerance and checkpointing
state_backend = flink_conf['state_backend']
state_checkpoints_dir = flink_conf['state_checkpoints_dir']
state_savepoints_dir = flink_conf['state_savepoints_dir']
state_backend_incremental = flink_conf['state_backend_incremental']

# Rest & web frontend

rest_port = flink_conf['rest_port']
rest_address = flink_conf['rest_address']
rest_bind_port = flink_conf['rest_bind_port']
rest_bind_address = flink_conf['rest_bind_address']
web_submit_enable = flink_conf['web_submit_enable']
io_tmp_dirs = flink_conf['io_tmp_dirs']
taskmanager_memory_preallocate = flink_conf['taskmanager_memory_preallocate']
classloader_resolve_order = flink_conf['classloader_resolve_order']
taskmanager_network_memory_fraction = flink_conf['taskmanager_network_memory_fraction']
taskmanager_network_memory_min = flink_conf['taskmanager_network_memory_min']
taskmanager_network_memory_max = flink_conf['taskmanager_network_memory_max']

# Flink Cluster Security Configuration
security_kerberos_login_contexts = flink_conf['security_kerberos_login_contexts']
security_kerberos_login_use_ticket_cache = flink_conf['security_kerberos_login_use_ticket_cache']
security_kerberos_login_keytab = flink_conf['security_kerberos_login_keytab']
security_kerberos_login_principal = flink_conf['security_kerberos_login_principal']

# History server

jobmanager_archive_fs_dir = flink_conf['jobmanager_archive_fs_dir']
historyserver_web_address = flink_conf['historyserver_web_address']
historyserver_web_port = flink_conf['historyserver_web_port']
historyserver_archive_fs_dir = flink_conf['historyserver_archive_fs_dir']
historyserver_archive_fs_refresh_interval = flink_conf['historyserver_archive_fs_refresh_interval']

# Custom properties
custom_properties = flink_conf['custom_properties']

"""
Logger.info('###Config:')

Logger.info(str(config))

java64_home = config['hostLevelParams']['java_home']

hostname = config['agentLevelParams']['hostname']


# es env
es_user = config['configurations']['elasticsearch-env']['elasticsearch.user']
es_group = config['configurations']['elasticsearch-env']['elasticsearch.group']

es_master_base_dir = config['configurations']['elasticsearch-env']['elasticsearch.base.dir'] + '/master'
es_slave_base_dir = config['configurations']['elasticsearch-env']['elasticsearch.base.dir'] + '/slave'

es_master_home = es_master_base_dir
es_master_bin = es_master_base_dir + '/bin'
es_slave_home = es_slave_base_dir
es_slave_bin = es_slave_base_dir + '/bin'

es_master_conf_dir = es_master_base_dir + '/config'
es_slave_conf_dir = es_slave_base_dir + '/config'

es_master_pid_dir = config['configurations']['elasticsearch-env']['elasticsearch.pid.dir'] + '/master'
es_slave_pid_dir = config['configurations']['elasticsearch-env']['elasticsearch.pid.dir'] + '/slave'

es_master_pid_file = format("{es_master_pid_dir}/elasticsearch-master.pid")
es_slave_pid_file = format("{es_slave_pid_dir}/elasticsearch-slave.pid")

es_download_url = config['configurations']['elasticsearch-env']['elasticsearch.download.url']

# jvm
heap_size = config['configurations']['elasticsearch-env']['elasticsearch.heap.size'] + 'g'
jvm_opts = config['configurations']['elasticsearch-env']['jvm.opts']

# es config
cluster_name = config['configurations']['elasticsearch-config']['cluster.name']
hostname = config['hostname']
node_attr_rack = config['configurations']['elasticsearch-config']['node.attr.rack']

data_dir = config['configurations']['elasticsearch-config']['path.data']

es_master_log_dir = config['configurations']['elasticsearch-config']['path.logs'] + '/master'
es_slave_log_dir = config['configurations']['elasticsearch-config']['path.logs'] + '/slave'

es_master_install_log = es_master_log_dir + '/elasticsearch-install.log'
es_slave_install_log = es_slave_log_dir + '/elasticsearch-install.log'

# multi data path
master_path_data = ','.join(x + '/master' for x in data_dir.split(','))
slave_path_data = ','.join(x + '/slave' for x in data_dir.split(','))
# single log path
master_path_logs = es_master_log_dir
slave_path_logs = es_slave_log_dir

bootstrap_memory_lock = str(config['configurations']['elasticsearch-config']['bootstrap.memory.lock'])
if bootstrap_memory_lock is True:
    bootstrap_memory_lock = 'true'
else:
    bootstrap_memory_lock = 'false'

network_host = config['configurations']['elasticsearch-config']['network.host']
#http_port = config['configurations']['elasticsearch-config']['http_port']

discovery_zen_ping_unicast_hosts = str(config['configurations']['elasticsearch-config']['discovery.zen.ping.unicast.hosts'])

# Need to parse the comma separated hostnames to create the proper string format within the configuration file
# Expects the format ["host1","host2"]
master_node_list = discovery_zen_ping_unicast_hosts.split(',')
discovery_zen_ping_unicast_hosts = '[' +  ','.join('"' + x + '"' for x in master_node_list) + ']'

discovery_zen_minimum_master_nodes = config['configurations']['elasticsearch-config']['discovery.zen.minimum.master.nodes']

gateway_recover_after_nodes = config['configurations']['elasticsearch-config']['gateway.recover.after.nodes']
node_max_local_storage_nodes = config['configurations']['elasticsearch-config']['node.max.local.storage.nodes']

action_destructive_requires_name = str(config['configurations']['elasticsearch-config']['action.destructive.requires.name'])
if action_destructive_requires_name is True:
    action_destructive_requires_name = 'true'
else:
    action_destructive_requires_name = 'false'




"""