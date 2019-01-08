#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

import aiwolfpy
import aiwolfpy.contentbuilder as cb

#printing of nested dicts and pandas
import json
from tabulate import tabulate

import time
import random

class SampleAgent(object):

	def __init__(self, agent_name):
		self.myname = agent_name
		self.sleeptime = 0.1

	def getName(self):
		return self.myname

	def initialize(self, base_info, diff_data, game_setting):
		self.base_info = base_info
		self.game_setting = game_setting
		self.printGameSetting(game_setting)

	def update(self, base_info, diff_data, request):
		self.base_info = base_info
		print(self.getTimeStamp()+" inside Update")
		self.printBaseInfo(base_info)
		self.printDiffData(diff_data)

	def dayStart(self):
		print(self.getTimeStamp()+" inside dayStart")
		return None

	def talk(self):
		#time.sleep (self.sleeptime)
		print(self.getTimeStamp()+" inside Talk")
		selected = self.randomPlayerId()
		print("Selected ID for talk: "+str(selected))
		return cb.vote(selected)
		#return cb.skip()

	def whisper(self):
		print(self.getTimeStamp()+" inside Whisper")
		selected = self.randomPlayerId()
		print("Selected ID for whisper: "+str(selected))
		return cb.attack(selected)
		#return cb.over()

	def vote(self):
		print(self.getTimeStamp()+" inside Vote")
		selected = self.randomPlayerId()
		print("Selected ID for vote: "+str(selected))
		return selected
		#return self.base_info['agentIdx']

	def attack(self):
		print(self.getTimeStamp()+" inside Attack")
		selected = self.randomPlayerId()
		print("Selected ID for attack: "+str(selected))
		return selected
		#return self.base_info['agentIdx']
		
	def divine(self):
		print(self.getTimeStamp()+" inside Divine")
		selected = self.randomPlayerId()
		print("Selected ID for divine: "+str(selected))
		return selected
		#return self.base_info['agentIdx']

	def guard(self):
		print(self.getTimeStamp()+" inside Guard")
		selected = self.randomPlayerId()
		print("Selected ID for guard: "+str(selected))
		return selected
		#return self.base_info['agentIdx']
	
	def finish(self):
		print(self.getTimeStamp()+" inside Finish")
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

	def getTimeStamp(self):
		return time.strftime('%l:%M:%S%p')

	def randomPlayerId(self):
		ids = self.getAlivePlayerIds()
		return random.choice(ids)

	def getAlivePlayerIds(self):
		ids = []
		for key,value in self.base_info["statusMap"].iteritems():
			if value == "ALIVE" and int(key) != self.base_info["agentIdx"]:
				ids.append(int(key))
		return ids

if __name__ == '__main__':	
	aiwolfpy.connect_parse(SampleAgent("myagent"))
