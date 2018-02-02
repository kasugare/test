#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto
import boto.s3.connection
import traceback
import os


class S3_FileSystemHandler:
	def __init__(self):
		self._access_key = 'AKIAI7IZ7K4OEDFWOX4A'
		self._secret_key = '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'
		self._s3_host = 's3.amazonaws.com'
		self._s3 = None
		self._init_connection()

	def _init_connection(self):
		if not self._s3:
			self._s3 = boto.connect_s3(aws_access_key_id = self._access_key,
				aws_secret_access_key = self._secret_key,
				host = self._s3_host,
				calling_format = boto.s3.connection.OrdinaryCallingFormat(),)

	def ls(self):
		try:
			for bucket in self._s3.get_all_buckets():
				print "{name}\t{created}".format(name = bucket.name, created = bucket.creation_date,)
				print "- ", dir(bucket)
				print bucket.name
				if bucket.name == 'hcc-alab-pa':
					for key in bucket.list():
						print "-" * 100
						print key
						print "{name}\t{size}\t{modified}".format(
								name = key.name,
								size = key.size,
								modified = key.last_modified,
								)
		except Exception, e:
			print traceback.format_exc(e)



	def write(self, filename, mode):
		pass

	def read(self):
		pass

	def readline(self):
		pass

	def readlines(self):
		pass

	def rm(self, filename):
		pass

	def rmr(self, dir_path):
		pass

	def mkdir(self, dir_path):
		pass

	def close(self):
		pass

class InvalidArgumentError(Exception):
	def __str__(self):
		return "invalid arguments"

class InvalidPathError(Exception):
	def __str__(self):
		return "path not valid"

class IsDirError(Exception):
	def __str__(self):
		return "path is a directory"

class IsFileError(Exception):
	def __str__(self):
		return "path is not directory"

class DirNotEmptyError(Exception):
	def __str__(self):
		return "directory not empty"

class SameFileError(Exception):
	def __str__(self):
		return "original path and target path are same"

class PathExistsError(Exception):
	def __str__(self):
		return "file or path is already exists"

class PathNotExistsError(Exception):
	def __str__(self):
		return "path does not exist"

class HdfsHostError(Exception):
	def __str__(self):
		return "operation category READ is not supported in state standby"

class ConnectionError(Exception):
	def __str__(self):
		return "HDFS connection aborted"


if __name__ == '__main__':
	s3fs = S3_FileSystemHandler()
	s3fs.ls()
