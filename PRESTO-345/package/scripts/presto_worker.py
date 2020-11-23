# -*- coding: utf-8 -*-

from resource_management import *
from resource_management.core.exceptions import ClientComponentHasNoStatus
from resource_management.core.logger import Logger
# from yarn_utils import *
# from presto_utils import *
import pwd,grp


class PrestoMaster(Script):

    def install(self, env):
        import params

        Logger.info('Creating Presto group')

        try:
            grp.getgrnam(params.presto_group)
        except KeyError:
            Group(params.presto_group)

        Logger.info('Creating Presto user')
        try:
            pwd.getpwnam(params.presto_user)
        except KeyError:
            User(params.presto_user,
                 gid=params.presto_group,
                 groups=[params.presto_group],
                 ignore_failures=True
                 )

        Logger.info('Creating presto install directory')
        Directory([params.presto_base_dir],
                  mode=0755,
                  cd_access='a',
                  owner=params.presto_user,
                  group=params.presto_group,
                  create_parents=True
                  )

        Logger.info('Downloading presto binaries')
        Execute("cd {0}; wget {1} -O presto.tar.gz".format(params.presto_base_dir, params.presto_download_url), user=params.presto_user)

        Logger.info('Extracting presto binaries')
        Execute("cd {0}; tar -zxvf presto.tar.gz".format(params.presto_base_dir), user=params.presto_user)

        Logger.info('Creating symbolic links')
        create_symbolic_link()

        self.configure(env)

        Logger.info('presto installation completed')

    def stop(self, env):
        import params

        result = kill_yarn_application(params.presto_yarn_session_name)

        if result:
            Logger.info('presto yarn session: {0} has been killed'.format(params.presto_yarn_session_name))
        else:
            Logger.info('Cannot not kill presto yarn session: {0}. Maybe it is not running'.format(params.presto_yarn_session_name))

    def start(self, env):
        import params

        Logger.info('Updating presto configuration')
        self.configure(env)

        Logger.info('Starting presto yarn session')
        cmd = get_start_yarn_session_cmd(params.presto_base_dir, params.presto_yarn_session_name, params.job_manager_heap_size, params.task_manager_heap_size, params.slot_count)
        Execute(cmd, user=params.presto_user)

        Logger.info('presto yarn session started')

    def status(self, env):
        raise ClientComponentHasNoStatus()

    def configure(self, env):
        import params

        Logger.info('Configuring presto')
        env.set_params(params)

        File("{0}/{1}/conf/presto-conf.yaml".format(params.presto_base_dir, presto_DIR_NAME),
             content=Template("presto-conf.yaml.j2"),
             owner=params.presto_user,
             group=params.presto_group
             )


if __name__ == '__main__':
    prestoMaster().execute()
