#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import os
import sys

import configparser
from rainbow_logging_handler import RainbowLoggingHandler

# !/usr/bin/env python
# -*- coding: utf-8 -*-

CONF_PATH = "/conf/"
CONF_FILENAME = "logger.ini"

LOGGER_INFO = ('log_name', 'log_level', 'log_format', 'log_dir', 'log_filename')
HANDLER_INFO = ('is_stream', 'is_file')
LOTATE_INFO = ('is_lotate', 'log_maxsize', 'backup_count')


def _getConfig():
    src_path = os.path.dirname(CONF_PATH)
    ini_path = src_path + "/" + CONF_FILENAME
    if not os.path.exists(ini_path):
        print ("# Cannot find logger.ini in conf directory : %s" % src_path)
        sys.exit(1)

    conf = configparser.RawConfigParser()
    conf.read(ini_path)
    return conf


def _cvtFlag(value):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        print ("# Wrong logger values in logger.ini.")
        sys.exit(1)


def _checkInteger(value):
    try:
        return int(value)
    except (Exception, e):
        print ("# Wrong logger values in logger.ini.")
        sys.exit(1)


def _getLoggerConf(configList, elemnts=LOGGER_INFO, confName='TEST_SERVER'):
    conf = _getConfig()
    for elementName in elemnts:
        configList[elementName] = conf.get(confName, elementName)
    return configList


def _getHandlerConf(configList, elemnts=HANDLER_INFO, confName='HANDLER'):
    conf = _getConfig()
    for elementName in elemnts:
        elementValue = conf.get(confName, elementName)
        if elementName == 'is_stream':
            configList[elementName] = _cvtFlag(elementValue)
        elif elementName == 'is_file':
            configList[elementName] = _cvtFlag(elementValue)
        else:
            configList[elementName] = elementValue
    return configList


def _getLotateConf(configList, elemnts=LOTATE_INFO, confName='LOTATE'):
    conf = _getConfig()
    for elementName in elemnts:
        elementValue = conf.get(confName, elementName)
        if elementName == 'is_lotate':
            configList[elementName] = _cvtFlag(elementValue)
        elif elementName == 'log_maxsize':
            configList[elementName] = _checkInteger(elementValue)
        elif elementName == 'backup_count':
            configList[elementName] = _checkInteger(elementValue)
        else:
            configList[elementName] = elementValue
    return configList


def getLoggerInfo():
    configList = { }
    configList = _getLoggerConf(configList, LOGGER_INFO, loggerConfName)
    configList = _getHandlerConf(configList)
    configList = _getLotateConf(configList)
    return configList


class Logger:
    def __init__(self):
        loggerInfo = getLoggerInfo()
        loggerName = loggerInfo['log_name']
        loggerLevel = self._getLevel(loggerInfo['log_level'])
        loggerFormat = loggerInfo['log_format']

        logger = logging.getLogger(loggerName)
        logger.setLevel(loggerLevel)
        formatter = logging.Formatter(loggerFormat)

        isFile = loggerInfo['is_file']
        isLotate = loggerInfo['is_lotate']
        isStream = loggerInfo['is_stream']

        if isFile:
            dirPath = loggerInfo['log_dir']
            fileName = loggerInfo['log_filename']
            maxBytes = loggerInfo['log_maxsize']
            backupCnt = loggerInfo['backup_count']
            handler = self._setFileLoggingHandler(dirPath, fileName, formatter, isLotate, maxBytes, backupCnt)
            logger.addHandler(handler)
        if isStream:
            handler = self._setStreamLoggingHandler(formatter)
            logger.addHandler(handler)
        self.logger = logger

    def _getLevel(self, level="INFO"):
        level = level.upper()
        if level == "DEBUG":
            return logging.DEBUG
        elif level == "ERROR":
            return logging.ERROR
        elif level == "FATAL":
            return logging.FATAL
        elif level == "CRITICAL":
            return logging.CRITICAL
        elif level == "WARN":
            return logging.WARN
        else:
            return logging.INFO

    def _setFileLoggingHandler(self, dirPath, fileName, formatter, isLotate=True, maxBytes=104857600, backupCnt=10):
        filePath = '%s/%s' % (dirPath, fileName)

        if isLotate:
            handler = logging.handlers.RotatingFileHandler(filePath, maxBytes=maxBytes, backupCount=backupCnt)
        else:
            handler = logging.FileHandler(filePath)
        handler.setFormatter(formatter)
        return handler

    def _setStreamLoggingHandler(self, formatter):
        handler = RainbowLoggingHandler(sys.stderr, datefmt='%Y-%m-%d %H:%M:%S', color_name=('white', None, False),
                                        color_levelno=('white', None, False), color_levelname=('white', None, False),
                                        color_pathname=('blue', None, True), color_filename=('blue', None, True), color_module=('blue', None, True),
                                        color_lineno=('cyan', None, True), color_funcName=('blue', None, True), color_created=('white', None, False),
                                        color_asctime=('black', None, True), color_msecs=('white', None, False),
                                        color_relativeCreated=('white', None, False), color_thread=('white', None, False),
                                        color_threadName=('white', None, False), color_process=('black', None, True),
                                        color_message_debug=('cyan', None, False), color_message_info=('white', None, False),
                                        color_message_warning=('yellow', None, True), color_message_error=('red', None, True),
                                        color_message_critical=('white', 'red', True))
        handler.setFormatter(formatter)
        return handler

    def setLevel(self, level="INFO"):
        loggerLevel = self._getLevel(level)
        logger.setLevel(loggerLevel)

    def getLogger(self):
        return self.logger
