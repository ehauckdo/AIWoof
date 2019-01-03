#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

import aiwolfpy
import aiwolfpy.contentbuilder as cb

class SampleAgent(object):

	def __init__(self, agent_name):
		self.myname = agent_name

	def getName(self):
		return self.myname

	def initialize(self, base_info, diff_data, game_setting):
		self.base_info = base_info
		self.game_setting = game_setting
		self.printGameSetting(game_setting)
		self.printBaseInfo(base_info)
		self.printDiffData(diff_data)

	def update(self, base_info, diff_data, request):
		self.base_info = base_info

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
		print(base_info)
		#for key in base_info.keys():
		#	print(str(key)+":")
		#	print(base_info[key])

	def printGameSetting(self, game_setting):
		print("Game Setting:")
		print(game_setting)
		#for key in game_setting.keys():
		#	print(str(key)+":")
		#	print(game_setting[key])
		
	def printDiffData(self, diff_data):
		print("Diff Data:")
		print(diff_data)
		#for key in diff_data.keys():
		#	print(str(key)+":")
		#	print(diff_data[key])

if __name__ == '__main__':	
	aiwolfpy.connect_parse(SampleAgent("myagent"))
