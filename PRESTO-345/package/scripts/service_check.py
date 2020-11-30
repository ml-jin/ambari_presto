# -*- coding: utf-8 -*-

from resource_management import *
from resource_management.core.exceptions import ClientComponentHasNoStatus
from resource_management.core.logger import Logger
from p_utils import *


class ServiceCheck(Script):
    def service_check(self, env):
        # raise ClientComponentHasNoStatus()
        output = commands.getoutput('pgrep presto')
        if output > 0:
    		return True
    	else:
    		return False


if __name__ == "__main__":
    ServiceCheck().execute()