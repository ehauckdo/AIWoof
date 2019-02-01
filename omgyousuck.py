#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division

# Sample random python-based agent for AIWolf
# Based on https://github.com/k-harada/AIWolfPy
# Developed for aiwolf 0.4.12 (2018/06/16)
# Author: ehauckdo

import aiwolfpy
import aiwolfpy.contentbuilder as cb

import random
import optparse
import sys

from utility import *

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

		printGameSetting(game_setting)
		self.updatePlayerMap(base_info)

	def update(self, base_info, diff_data, request):
		print(getTimeStamp()+" inside Update")
		self.base_info = base_info
		
		printBaseInfo(base_info)
		printDiffData(diff_data)
		
		self.updateGameHistory(diff_data)
		self.updatePlayerMap(base_info)

	def dayStart(self):
		print(getTimeStamp()+" inside dayStart")

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
				selected = randomPlayerId(self.base_info)
				print("Selecting a random target... Selected ID: "+str(selected))
				self.setTarget(selected, False)

		return None

	def talk(self):
		print(getTimeStamp()+" inside Talk")
		
		if self.player_map[self.current_target]["revenge"] is False: 
			print("Voting on random target")
		else:
			print("Voting for revenge!")

		# Talking against a target has 3 steps: first estimate,
		# then state your vote, then start requesting other agents
		# to vote against target
		if self.player_map[self.current_target]["targetStatus"] == 0: 	
			talk = cb.estimate(self.current_target, "WEREWOLF")
		elif self.player_map[self.current_target]["targetStatus"] == 1:
			talk = cb.vote(self.current_target)
		else:
			talk = cb.request(cb.vote(self.current_target))
			
		self.player_map[self.current_target]["targetStatus"] += 1
		return talk

	def whisper(self):
		print(getTimeStamp()+" inside Whisper")
		if self.current_target != None:
			print("Whispering request against current target: ")
			selected = self.current_target
		else:
			selected = randomPlayerId(self.base_info)
			print("Whispering request against random agent: "+str(selected))
		return cb.request(cb.attack(selected))

	def vote(self):
		print(getTimeStamp()+" inside Vote")
		if self.current_target != None:
			print("Voting on current target: ")
			return self.current_target
		else:
			selected = randomPlayerId(self.base_info)
			print("Voting on random agent: "+str(selected))
			return selected

	def attack(self):
		print(getTimeStamp()+" inside Attack")
		if self.current_target != None:
			print("Attacking current target: ")
			return self.current_target
		else:
			selected = randomPlayerId(self.base_info)
			print("Attacking random agent: "+str(selected))
			return selected
		
	def divine(self):
		print(getTimeStamp()+" inside Divine")
		return randomPlayerId(self.base_info)

	def guard(self):
		print(getTimeStamp()+" inside Guard")
		return randomPlayerId(self.base_info)
	
	def finish(self):
		print(getTimeStamp()+" inside Finish")
		return None

	def updatePlayerMap(self, base_info):
		if self.player_map == None:
			self.player_map = {}
		
		for key, value in base_info["statusMap"].items():
			agent_id = int(key)
			if agent_id is not self.id:
				if agent_id not in self.player_map:
					self.player_map[agent_id] = {}
					self.player_map[agent_id]["targetStatus"] = 0
					self.player_map[agent_id]["revenge"] = False
				self.player_map[agent_id]["status"] = value
				self.player_map[agent_id]["whispered"] = False

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
		self.player_map[id]["targetStatus"] = 0

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
