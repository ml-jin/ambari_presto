# -*- coding: utf-8 -*-

from resource_management import *
from resource_management.core.exceptions import ClientComponentHasNoStatus
from resource_management.core.logger import Logger
from resource_management.libraries.functions import check_process_status
from p_utils import *
from presto_utils import *
import pwd,grp


class PrestoMaster(Script):
    # for restart method only, restart 会调用prepare方法。 解决一个重启相关的bug.
    def prepare(self):
        stop()

    def install(self, env):
        import params
        # clean old folders
        Execute("rm -rfv {0}".format(params.presto_base_dir), user='root')
        
        Logger.info('Creating Presto group')

        try:
            grp.getgrnam(params.presto_group)
        except KeyError:
            Group(params.presto_group)

        Logger.info('Creating Presto user')
        try:
            pwd.getpwnam(params.presto_user)
        except KeyError:
            Execute("useradd presto -m -g presto", user='root')
        
        Logger.info('Creating presto install directory')
        Directory([params.presto_base_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.presto_user,
                  group=params.presto_group,
                  create_parents=True
                  )

        Logger.info('Creating presto data directory')
        Execute("mkdir -p /home/presto/data_345", user='root')

        Logger.info('Creating presto required jdk11+ directory')
        Directory([params.presto_jdk11_dest],
                  mode=0755,
                  cd_access='a',
                  owner=params.presto_user,
                  group=params.presto_group,
                  create_parents=True
                  )

        Logger.info('Creating presto required pid directory')
        Directory([params.presto_coor_pid_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.presto_user,
                  group=params.presto_group,
                  create_parents=True,
                  recursive_ownership=True
                  )

        Logger.info('Creating presto required logs directory')
        Directory([params.presto_log_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.presto_user,
                  group=params.presto_group,
                  create_parents=True
                  )

        # activate java env
        Execute("cd ~ && echo \"JAVA_HOME={0}/jdk-11.0.9\" >> .bashrc".format('/home/presto/worker/presto-server-345/jdk11'), user='presto')
        Execute("cd ~ && echo \"export PATH=$JAVA_HOME/bin:$PATH\" >> .bashrc", user='presto')


        Execute("chmod -R 777 /home/presto", user=params.presto_user)

        Logger.info('Downloading jdk binaries')
        Execute("cd {0}; wget {1} -O jdk-11.0.9_linux-x64_bin.tar.gz".format(params.presto_base_dir, params.presto_jdk11_download_url), user=params.presto_user)

        Logger.info('Extracting jdk binaries')
        Execute("cd {0};  tar -zxvf jdk-11.0.9_linux-x64_bin.tar.gz -C {1}".format(params.presto_base_dir, params.presto_jdk11_dest), user=params.presto_user)

        # download presto 
        Logger.info('Downloading presto binaries')
        Execute("cd {0}; wget {1} -O presto-server-345.tar.gz".format(params.presto_base_dir, params.presto_download_url), user=params.presto_user)

        Logger.info('Extracting presto binaries')
        Execute("cd {0}; tar -zxvf presto-server-345.tar.gz".format(params.presto_base_dir), user=params.presto_user)

        # Logger.info('Creating symbolic links')
        # create_symbolic_link()
        
        self.configure(env)
        Execute("/usr/hdp/3.0.1.0-187/presto/presto-server-345/bin/launcher start --pid-file=/var/run/presto/coor/coor.id  --launcher-log-file={} --server-log-file={} --config='/var/lib/ambari-server/resources/stacks/HDP/3.0/services/PRESTO/configuration/config_new.properties' && echo $(pgrep presto) > /var/run/presto/coor/coor.id".format(params.presto_log_launcher, params.presto_log_server), user='root')

        Logger.info('presto installation completed')

    def stop(self, env):
        import params
        import os
        os.system('kill -9 $(pgrep presto)')
        os.system('rm -rf /var/run/presto/coor/coor.id')
        Logger.info('Presto coor server stop completed')
        

    def start(self, env):
        import params

        Logger.info('Updating presto configuration')
        self.configure(env)

        import os 
        if os.system('pgrep presto') != 0:
          Execute("/usr/hdp/3.0.1.0-187/presto/presto-server-345/bin/launcher start  --pid-file=/var/run/presto/coor/coor.id  --launcher-log-file={} --server-log-file={} --config='/var/lib/ambari-server/resources/stacks/HDP/3.0/services/PRESTO/configuration/config_new.properties'".format(params.presto_log_launcher, params.presto_log_server), user='root')
        Logger.info('start process finished, succssfully start')

    def status(self, env):
        # import status_params
        # env.set_params(status_params)
        check_process_status('/var/run/presto/coor/coor.id')

    def configure(self, env):
        import params

        Logger.info('Configuring presto')
        env.set_params(params)

        File("/var/lib/ambari-server/resources/stacks/HDP/3.0/services/PRESTO/configuration/config_new.properties",
             content=Template("config.master.properties.j2"),
             owner=params.presto_user,
             group=params.presto_group
             )


if __name__ == '__main__':
    PrestoMaster().execute()
