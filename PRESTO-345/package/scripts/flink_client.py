# -*- coding: utf-8 -*-

from resource_management import *
from resource_management.core.exceptions import ClientComponentHasNoStatus
from resource_management.core.logger import Logger
from yarn_utils import *
from flink_utils import *
import pwd,grp


class FlinkMaster(Script):

    def install(self, env):
        import params

        Logger.info('Creating Flink group')

        try:
            grp.getgrnam(params.flink_group)
        except KeyError:
            Group(params.flink_group)

        Logger.info('Creating Flink user')
        try:
            pwd.getpwnam(params.flink_user)
        except KeyError:
            User(params.flink_user,
                 gid=params.flink_group,
                 groups=[params.flink_group],
                 ignore_failures=True
                 )

        Logger.info('Creating Flink install directory')
        Directory([params.flink_base_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.flink_user,
                  group=params.flink_group,
                  create_parents=True
                  )

        Logger.info('Downloading Flink binaries')
        Execute("cd {0}; wget {1} -O flink.tar.gz".format(params.flink_base_dir, params.flink_download_url), user=params.flink_user)

        Logger.info('Extracting Flink binaries')
        Execute("cd {0}; tar -zxvf flink.tar.gz".format(params.flink_base_dir), user=params.flink_user)

        Logger.info('Creating symbolic links')
        create_symbolic_link()

        self.configure(env)

        Logger.info('Flink installation completed')

    def stop(self, env):
        import params

        result = kill_yarn_application(params.flink_yarn_session_name)

        if result:
            Logger.info('Flink yarn session: {0} has been killed'.format(params.flink_yarn_session_name))
        else:
            Logger.info('Cannot not kill Flink yarn session: {0}. Maybe it is not running'.format(params.flink_yarn_session_name))

    def start(self, env):
        import params

        Logger.info('Updating Flink configuration')
        self.configure(env)

        Logger.info('Starting Flink yarn session')
        cmd = get_start_yarn_session_cmd(params.flink_base_dir, params.flink_yarn_session_name, params.job_manager_heap_size, params.task_manager_heap_size, params.slot_count)
        Execute(cmd, user=params.flink_user)

        Logger.info('Flink yarn session started')

    def status(self, env):
        raise ClientComponentHasNoStatus()

    def configure(self, env):
        import params

        Logger.info('Configuring Flink')
        env.set_params(params)

        File("{0}/{1}/conf/flink-conf.yaml".format(params.flink_base_dir, FLINK_DIR_NAME),
             content=Template("flink-conf.yaml.j2"),
             owner=params.flink_user,
             group=params.flink_group
             )


if __name__ == '__main__':
    FlinkMaster().execute()
