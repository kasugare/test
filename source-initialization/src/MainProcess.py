#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.util_logger import Logger
import multiprocessing
import sys

PROCESS_NAME = 'DEFAULT'

class MainProcess:
	def __init__(self):
		self._logger = Logger(PROCESS_NAME).getLogger()

	def doProcess(self):
		self._logger.info("Show logger info format")
		self._logger.debug("Show logger debug format")
		self._logger.warn("Show logger warn format")
		self._logger.critical("Show logger critical format")
		self._logger.exception("Show logger except format")

if __name__ == '__main__':
	MainProcess().doProcess()
