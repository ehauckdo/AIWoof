Notes for Programming Agents
============================

The aiwolf-py originally developed by [Kei Harada](https://github.com/k-harada/) allows the development of Python agents for the AIWolf competition. This document will briefly describe how you can use this library to develop agents using Python.

First and foremost you must `import aiwolfpy` in your script. Once that is done, you can create a class for your agent and can use the aiwolfpy library to connect to a server by running `aiwolfpy.connect_parse(myAgentObject)`. Once this is run, the aiwolfpy library will connect to the server and will be the intermediary between the server and your agent.

## Agent Class

Your agent class is required to implement a number of functions that will be called by the aiwolfpy library.

getName(self): returns the name of the agent (string)

initialize(self, base_info, diff_data, game_setting): this function is called before a game starts. base_info, diff_data and game_setting contains importanto information about the current game. The contents of it are described in the next section. Note that this function is different from the __init__ one.

update(self, base_info, diff_data, request): this function is always called just before the agent is requested to provide some information (e.g. a statement for the current day phase). 

dayStart(self): called at the start of the day. 

talk, whisper: should return a full sentence according to the protocol in the string format (the content builder library can be used to generate valid sentences)

vote, attack, divine, guard: should return an ID (integer) of one of the agents

finish(self): called when the game finishes

## Content builder

The content builder file within the aiwolfpy library allows the generation of valid sentences according to the AIWolf protocol specification.

## Information received from the server

 * base_info: 
 
 * diff_data:
 
 * game_setting:

 
 
