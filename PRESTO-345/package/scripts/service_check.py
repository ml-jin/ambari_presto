# -*- coding: utf-8 -*-

from resource_management import *
from resource_management.core.exceptions import ClientComponentHasNoStatus
from resource_management.core.logger import Logger
from yarn_utils import *


class ServiceCheck(Script):
    def service_check(self, env):
        raise ClientComponentHasNoStatus()


if __name__ == "__main__":
    ServiceCheck().execute()