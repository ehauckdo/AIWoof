#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

# Sample random python-based agent for AIWolf
# Based on https://github.com/k-harada/AIWolfPy
# Developed for aiwolf 0.4.12 (2018/06/16)
# Author: ehauckdo

import aiwolfpy
import aiwolfpy.contentbuilder as cb

#printing of nested dicts and pandas
import json
from tabulate import tabulate

import time
import random
import optparse
import sys

class SampleAgent(object):

	def __init__(self, agent_name):
		self.myname = agent_name
		self.sleeptime = 0.1

	def getName(self):
		return self.myname

	def initialize(self, base_info, diff_data, game_setting):
		self.id = base_info["agentIdx"]
		self.base_info = base_info
		self.game_setting = game_setting

		self.game_history = {}
		self.player_map = {}
		self.target_list = []
		self.current_target = None

		self.printGameSetting(game_setting)
		self.updatePlayerMap(base_info)

	def update(self, base_info, diff_data, request):
		print(self.getTimeStamp()+" inside Update")
		self.base_info = base_info
		
		self.printBaseInfo(base_info)
		self.printDiffData(diff_data)
		
		self.updateGameHistory(diff_data)
		self.updatePlayerMap(base_info)

	def dayStart(self):
		print(self.getTimeStamp()+" inside dayStart")

		# at the start of each day, either assign a new random target
		# or fetch a new target from the target list (agents who previously voted against us)
		if self.current_target is None or self.player_map[self.current_target]["status"] == "DEAD":
			
			while len(self.target_list) > 0:
				selected = self.target_list.pop(0)
				if self.player_map[selected]["status"] != "DEAD":
					print("Selecting new target from target_list... Selected ID: "+str(selected))
					self.setTarget(selected, True)
					break
				else:
					continue
			else:
				selected = self.randomPlayerId()
				print("Selecting a random target... Selected ID: "+str(selected))
				self.setTarget(selected, False)

		return None

	def talk(self):
		#time.sleep (self.sleeptime)
		print(self.getTimeStamp()+" inside Talk")
		
		if self.player_map[self.current_target]["revenge"] is False: 
			print("Voting on random target")
		else:
			print("Voting for revenge!")

		if self.player_map[self.current_target]["estimated"] == False: 
			self.player_map[self.current_target]["estimated"] = True
			return cb.estimate(self.current_target, "WEREWOLF")
		else:
			return cb.vote(self.current_target)

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
		if len(ids) > 0:
			return random.choice(ids)
		else:
			return 0

	def getAlivePlayerIds(self):
		ids = []
		for key,value in self.base_info["statusMap"].items():
			if value == "ALIVE" and int(key) != self.base_info["agentIdx"]:
				ids.append(int(key))
		return ids

	def updatePlayerMap(self, base_info):
		if self.player_map == None:
			self.player_map = {}
		
		for key, value in base_info["statusMap"].items():
			agent_id = int(key)
			if agent_id is not self.id:
				if agent_id not in self.player_map:
					self.player_map[agent_id] = {}
					self.player_map[agent_id]["estimated"] = False
					self.player_map[agent_id]["revenge"] = False
				self.player_map[agent_id]["status"] = value

	def updateGameHistory(self, diff_data):

		for row in diff_data.itertuples():

			current_day = getattr(row, "day")
			if current_day not in self.game_history:
				self.game_history[current_day] = {}

			current_turn = getattr(row, "turn")
			if current_turn not in self.game_history[current_day]:
				self.game_history[current_day][current_turn] = {}

			agent = getattr(row, "agent")
			text = getattr(row, "text")

			# if anyone votes, estimates, or divines on our agent
			# we set this person as a target
			if "{:02d}".format(self.id) in text:
				if "ESTIMATE" in text or "VOTE" in text or ("DIVINED" in text and "WEREWOLF" in text):
					
					# if we are pursuing revenge against someone already, add this 
					# new agent to the target liost
					if self.player_map[self.current_target]["revenge"] == True:
						self.target_list.append(agent)
					# otherwise, set this new agent as the current target
					else:
						self.setTarget(agent, True)
						

	def setTarget(self, id, revenge):
		self.current_target = id

		self.player_map[id]["revenge"] = revenge
		self.player_map[id]["estimated"] = False

def parseArgs(args):
	usage = "usage: %prog [options]"
	parser = optparse.OptionParser(usage=usage) 

	# need this to ensure -h can be used as an option
	parser.set_conflict_handler("resolve")

	parser.add_option('-h', action="store", type="string", dest="hostname",
		help="IP address of the AIWolf server", default=None)
	parser.add_option('-p', action="store", type="int", dest="port", 
		help="Port to connect in the server", default=None)
	parser.add_option('-r', action="store", type="string", dest="port", 
		help="Role request to the server", default=-1)
	
	(opt, args) = parser.parse_args()
	if opt.hostname == None or opt.port == -1:
		parser.print_help()
		sys.exit()

if __name__ == '__main__':	
	parseArgs(sys.argv[1:])
	aiwolfpy.connect_parse(SampleAgent("omgyousuck"))
