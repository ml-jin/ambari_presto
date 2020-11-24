# -*- coding: utf-8 -*-

from resource_management import *
from resource_management.core.exceptions import ClientComponentHasNoStatus
from resource_management.core.logger import Logger
from p_utils import *
from presto_utils import *
import pwd,grp


class PrestoMaster(Script):

    def install(self, env):
        import params
        # clean old folders
        Execute("rm -rfv {0}".format(params.presto_base_dir), user=params.presto_root)
        
        Logger.info('Creating Presto group')

        try:
            grp.getgrnam(params.presto_group)
        except KeyError:
            Group(params.presto_group)

        Logger.info('Creating Presto user')
        try:
            pwd.getpwnam(params.presto_user)
        except KeyError:
            # User(params.presto_user,
            #      gid=params.presto_group,
            #      groups=[params.presto_group],
            #      ignore_failures=True
            #      )
            Execute("useradd presto -m -g presto", user=params.root)
        
        Logger.info('Creating presto install directory')
        Directory([params.presto_base_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.presto_user,
                  group=params.presto_group,
                  create_parents=True
                  )

        Logger.info('Creating presto data directory')
        Execute("mkdir -p /home/presto/data_345", user='presto')
        # Directory(['/home/presto/data_345'],
        #           mode=0755,
        #           cd_access='a',
        #           owner='presto',
        #           group=params.presto_group,
        #           create_parents=True
        #           )

        Logger.info('Creating presto required jdk11+ directory')
        Directory([params.presto_jdk11_dest],
                  mode=0755,
                  cd_access='a',
                  owner=params.presto_user,
                  group=params.presto_group,
                  create_parents=True
                  )

        # activate java env
        Execute("echo \"export JAVA_HOME={0}/jdk-11.0.9; export PATH=$JAVA_HOME/bin:$PATH\" >> .bash_profile".format(params.presto_jdk11_dest), user=params.presto_user)

        # Execute("export JAVA_HOME={0}; export PATH=$JAVA_HOME/bin:$PATH".format(params.presto_jdk11_dest), user=params.presto_user)

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
        Execute("/usr/hdp/3.0.1.0-187/presto/presto-server-345/bin/launcher run", user='presto')

        # self.configure(env) # temperary not using

        Logger.info('presto installation completed')

    def stop(self, env):
        import params

        result = kill_yarn_application(params.presto_yarn_session_name)

        if result:
            Logger.info('presto : {0} has been killed'.format(params.presto_yarn_session_name))
        else:
            Logger.info('Cannot not kill presto : {0}. Maybe it is not running'.format(params.presto_yarn_session_name))

    def start(self, env):
        import params

        Logger.info('Updating presto configuration')
        self.configure(env)

        # Logger.info('Starting presto yarn session')
        # cmd = get_start_yarn_session_cmd(params.presto_base_dir, params.presto_yarn_session_name, params.job_manager_heap_size, params.task_manager_heap_size, params.slot_count)
        # Execute(cmd, user=params.presto_user)
        Execute("/usr/hdp/3.0.1.0-187/presto/presto-server-345/bin/launcher run", user='presto')

    def status(self, env):
        raise ClientComponentHasNoStatus()

    def configure(self, env):
        import params

        Logger.info('Configuring presto')
        env.set_params(params)

        # File("{0}/{1}/conf/presto-conf.yaml".format(params.presto_base_dir, presto_DIR_NAME),
        #      content=Template("presto-conf.yaml.j2"),
        #      owner=params.presto_user,
        #      group=params.presto_group
        #      )


if __name__ == '__main__':
    PrestoMaster().execute()
