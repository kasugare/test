#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.util_logger import Logger
from resource_manager.resource_info import ResourceInfo
import multiprocessing
import sys

PROCESS_NAME = 'DEFAULT'

class MainProcess:
	def __init__(self):
		self._logger = Logger(PROCESS_NAME).getLogger()

	def doProcess(self):
		resource = ResourceInfo(self._logger)
		resource.doProcess()

if __name__ == '__main__':
	MainProcess().doProcess()
