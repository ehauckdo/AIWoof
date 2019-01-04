#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

import aiwolfpy
import aiwolfpy.contentbuilder as cb

#printing of nested dicts
from pprint import pformat
from yapf.yapflib.yapf_api import FormatCode
import json
from tabulate import tabulate

class SampleAgent(object):

	def __init__(self, agent_name):
		self.myname = agent_name

	def getName(self):
		return self.myname

	def initialize(self, base_info, diff_data, game_setting):
		self.base_info = base_info
		self.game_setting = game_setting
		self.printGameSetting(game_setting)

	def update(self, base_info, diff_data, request):
		self.base_info = base_info
		self.printBaseInfo(base_info)
		self.printDiffData(diff_data)

	def dayStart(self):
		return None

	def talk(self):
		return cb.over()

	def whisper(self):
		return cb.over()

	def vote(self):
		return self.base_info['agentIdx']

	def attack(self):
		return self.base_info['agentIdx']
		
	def divine(self):
		return self.base_info['agentIdx']

	def guard(self):
		return self.base_info['agentIdx']
	
	def finish(self):
		return None

	def printBaseInfo(self, base_info):
		print("Base Info:")
		print(json.dumps(base_info, indent=4))

	def printGameSetting(self, game_setting):
		print("Game Setting:")
		print(json.dumps(game_setting, indent=4))
		
	def printDiffData(self, diff_data):
		print("Diff Data:")
		#print(json.dumps(diff_data, indent=4))
		print(tabulate(diff_data, headers='keys', tablefmt='psql'))

if __name__ == '__main__':	
	aiwolfpy.connect_parse(SampleAgent("myagent"))
