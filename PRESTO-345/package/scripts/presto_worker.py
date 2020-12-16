# -*- coding: utf-8 -*-

from resource_management import *
from resource_management.core.exceptions import ClientComponentHasNoStatus
from resource_management.core.logger import Logger
from p_utils import *
from presto_utils import *
import pwd,grp

import uuid
UUID = str(uuid.uuid1())
class PrestoWorker(Script):

    def install(self, env):
        import params
        # clean old folders
        Execute("rm -rfv {0}".format('/home/presto/worker'), user='root')
        
        Logger.info('Creating Presto group')

        try:
            grp.getgrnam(params.presto_group)
        except KeyError:
            Group(params.presto_group)

        Logger.info('Creating Presto user')
        try:
            pwd.getpwnam('presto')
        except KeyError:
            Execute("useradd presto -m -g hadoop", user='root')
        
        Logger.info('Creating presto install directory')
        Directory(['/home/presto/worker'],
                  mode=0755,
                  cd_access='a',
                  owner=params.presto_user,
                  group=params.presto_group,
                  create_parents=True
                  )

        Logger.info('Creating presto data directory')
        Execute("mkdir -p /home/presto/worker/data_345", user=params.presto_user)

        Logger.info('Creating presto required jdk11+ directory')
        Directory(['/home/presto/worker/presto-server-345/jdk11'],
                  mode=0755,
                  cd_access='a',
                  owner=params.presto_user,
                  group=params.presto_group,
                  create_parents=True
                  )

        Logger.info('Creating presto required pid directory')
        Directory([params.presto_worker_pid_dir],
                  mode=0777,
                  cd_access='a',
                  owner=params.presto_user,
                  group=params.presto_group,
                  create_parents=True
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
        Execute("echo \"JAVA_HOME={0}/jdk-11.0.9\" >> ~/.bashrc && echo \"export PATH=$JAVA_HOME/bin:$PATH\" >> ~/.bashrc".format('/home/presto/worker/presto-server-345/jdk11'), user='presto')
        #Execute("echo \"export PATH=$JAVA_HOME/bin:$PATH\" >> ~/.bashrc", user='presto')

        Execute("chmod -R 777 /home/presto", user=params.presto_user)
        # Execute("export JAVA_HOME={0}; export PATH=$JAVA_HOME/bin:$PATH".format(params.presto_jdk11_dest), user=params.presto_user)

        Logger.info('Downloading jdk binaries')
        Execute("cd {0}; wget {1} -O jdk-11.0.9_linux-x64_bin.tar.gz".format('/home/presto/worker', params.presto_jdk11_download_url), user=params.presto_user)

        Logger.info('Extracting jdk binaries')
        Execute("cd {0};  tar -zxvf jdk-11.0.9_linux-x64_bin.tar.gz -C {1}".format('/home/presto/worker', '/home/presto/worker/presto-server-345/jdk11'), user=params.presto_user)

        # download presto 
        Logger.info('Downloading presto binaries')
        Execute("cd {0}; wget {1} -O presto-server-345.tar.gz".format('/home/presto/worker', params.presto_download_url), user=params.presto_user)

        Logger.info('Extracting presto binaries')
        Execute("cd {0}; tar -zxvf presto-server-345.tar.gz".format('/home/presto/worker'), user=params.presto_user)

        # Logger.info('Creating symbolic links')
        # create_symbolic_link()

        # self.configure(env) # temperary not using
        # generate worker uuid, and change configs
        
        import os
        os.system('cd /home/presto/worker/presto-server-345/etc/ && sed -i "s/node.id=ffffffff-ffff-ffff-ffff-ffffffffffff/node.id=$(uuidgen)/g" node.properties ')
        self.configure(env)
        Execute("source /home/presto/.bashrc && /home/presto/worker/presto-server-345/bin/launcher start --config='/home/presto/worker/presto-server-345/etc/config_new.properties' --pid-file='/var/run/presto/worker/worker.id'", user='presto')
        
        Logger.info('presto installation completed')

    def stop(self, env):
        import os
        import params

        os.system('kill -9 $(pgrep presto)')
        os.system('rm -rf /var/run/presto/worker/worker.id')
        Logger.info('Presto coor server stop completed')


    def start(self, env):
        import params

        Logger.info('Updating presto configuration')
        self.configure(env)

        import os 
        if os.system('pgrep presto') != 0:
            Execute("source /home/presto/.bashrc && /home/presto/worker/presto-server-345/bin/launcher start --config='/home/presto/worker/presto-server-345/etc/config_new.properties' --pid-file='/var/run/presto/worker/worker.id' ", user='presto')
        Logger.info('presto start process completed')

    def status(self, env):
        # import status_params
        # env.set_params(status_params)

        # Use built-in method to check status using pidfilcde
        check_process_status("/var/run/presto/worker/worker{0}.id".format('') )

    def configure(self, env):
        import params

        Logger.info('Configuring presto')
        Logger.info('Configure presto worker complete')
        env.set_params(params)

        File("/home/presto/worker/presto-server-345/etc/config_new.properties",
             content=Template("config.worker.properties.j2"),
             owner=params.presto_user,
             group=params.presto_group
             )


if __name__ == '__main__':
    PrestoWorker().execute()
