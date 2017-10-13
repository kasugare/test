#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import yaml

class YamlParser:
	def __init__(self):
		pass

	def doParsing(self):
		yaml_doc = open("framework_context.yaml", 'r')
		context = yaml.load(yaml_doc)		
		# print json.dumps(context, sort_keys=True, indent=4)
		self._doParse(context)

	def _doParse(self, context, count=0):
		context_type = type(context)
		if context_type == dict:
			context_key = context.keys()
			context_key.sort()
			for key in context_key:
				print "\n",  "    " * count,  " - %s: " %key,
				count += 1
				self._doParse(context[key], count)
				count -= 1
		elif context_type == list:
			for subContext in context:
				self._doParse(subContext, count)
		else:
			print "%s" %context,

if __name__ == '__main__':
	parser = YamlParser()
	parser.doParsing()