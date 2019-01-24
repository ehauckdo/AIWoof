# What is AIWolf?

Quoting from [aiwolf.org](http://aiwolf.org/en/introduction):

> a project to create an “Artificial Intelligence Werewolf” (AIWolf) to play as the werewolf in place of a human player. The objective of this comprehensive project is not only to develop a game-playing algorithm, but also to develop virtual agents, real robots, and so on. 

The AI Competition currently has 2 branches, one protocol-based where agents can use a predefined grammar to communicate, and one NLP-based. This repository has information on the protocol-based branch of the competition.

To learn the rules and how to play the Werewolf game, please refer to [this website](https://werewolf.chat/Main_Page)

# Roles in AIWolf

### Villager Team Roles

* Villager: regular villager role, no special abilities
* Seer: has the ability to discover if someone is a werewolf or a human during each night phase
* Medium: has the ability to discover if someone who was voted and exiled from the village was a werewolf or not
* Bodyguard: has the ability to protect someone or himself every day 

### Werewolf Team Roles

* Werewolf: has the ability to predate one villager everyday. All werewolves need to agree on who to attack.
* Possessed: a regular villager, but alligned with the werewolf team

# Executing a Python-based agent

The AIWolf framework is developed in Java and therefore, the primary way of developing an agent for the competition is by using the [java files offered on the official website](http://aiwolf.org/en/server). Basic instructions in English on which classes to inherit from are provided.

However, the AIWolf competition is run on a server, and each agent connects to this server via sockets. Therefore, as long as you can develop a program which can connect to a server via sockets and receive/submit strings, any programming language should be usable in this platform. However, the organizers need to be able to execute the code during competitions, therefore, only a few languages are officially supported. Python is one of them.

The first Python implementation for AIWolf can be found at [Kei Harada's repository](https://github.com/k-harada/AIWolfPy). The current repository has the same code with minor changes.

### Setting up a server

Before running your agent, you need to set up a server. 

First download the latest [server files](http://aiwolf.org/en/server) from the website (aiwolf-ver0.4.*). 

#### GUI mode

The first and simplest way to execute the server is using the GUI mode. Simply navigate to the unzipped folder and run

```
./StartServer.sh
```

From there, you selected the number of players in the GUI interface, press Connect, and the server is ready for you python-based agent to connect. Additionaly, you can run the StartGUIClient.sh and connect java-base agents to server as well (including the sample ones provided by the competition).

#### Terminal mode

Using the GUI mode you can not automatically run a certain number of games, which can be a problem for testing.

The second option is using the terminal mode. For that you have to open the AutoStarter.ini and configure the parameters properly

```
lib=./	
log=./log/			#folder to save logs
port=10000			#port to connect
game=10				#number of games to run
view=false			#show the game GUI
setting=./SampleSetting.cfg	#game related settings
agent=5 			#number of agents to play
Sample1,org.aiwolf.sample.player.SampleRoleAssignPlayer #list of java agents to connect
Sample2,org.aiwolf.sample.player.SampleRoleAssignPlayer #jar files must be on the same folder
Sample3,org.aiwolf.sample.player.SampleRoleAssignPlayer 
Sample4,org.aiwolf.sample.player.SampleRoleAssignPlayer
```
If you want to connect a python-based agent, simply leave less java-based clients in the agent list than the total number of agents specified (alternatively, leave the agent list empty and connect only python-based clients). The server is going to wait for connections until the specified number of agents is met. After configuring the AutoStarter.ini file, you can execute the server in terminal mode by running

```
./AutoStarter.sh
```

### Connecting the Python-based agent

Once the server is set up, you can connect the sample python agent in the current repository by executing

```
./aiwoof.py -h localhost -p 10000
```

You can also request a role to the server by passing -r [ROLE] as an argument (roles can be VILLAGER, SEER, MEDIUM, BODYGUARD, POSSESSED, WEREWOLF).

# AIWolf Protocol Specification (ver2.01, 2017)

This guide will include keywords, sentences, operators and grammar related to the protocol specification of the AIWolf competition. The official specification for the competition (in Japanese) can be found [here](http://aiwolf.org/control-panel/wp-content/uploads/2014/03/protocol_2017-2.pdf).

* List of keywords used for building sentences and their usage: 

  * [subject], [target]: one of the agents playing the game (Agent0 ~ AgentN) 
  * [role]: 6 types of roles supported (VILLAGER, SEER, MEDIUM, BODYGUARD, WEREWOLF, POSSESSED)
  * [species]: 2 types of species supported (HUMAN, WEREWOLF)
  * [verb]: 13 types of verbs allowed (full list below)
  * [talk number]: unique id for each sentence (composed by [day number] and [talk_id] for the sentence in that day) 

* Sentences: (13 different types in total)

  * Sentences that express ideas or intention from the player
  
    * [subject] ESTIMATE [target] [role] *(The [subject] is suggesting that [target] could be [role])*
    * [subject] COMINGOUT  [target][role] *(The [subject] is stating that [target] is [role])*

  * Sentences for basic actions of a Werewolf game
  
    * [subject] DIVINATION [target]
    * [subject] GUARD [target]
    * [subject] VOTE [target]
    * [subject] ATTACK [target]

  * Sentences that express the result of a certain action

    * [subject] DIVINED [target] [species]
    * [subject] IDENTIFIED [target] [species]*
    * [subject] GUARDED [target]

*(keyword INQUESTED was used before 2017) 

  * Sentences to express agreement, disagreement

    * [subject] AGREE [talk number]
    * [subject] DISAGREE [talk number]
	
  * Sentences related to the flow of the conversation 

    * [subject] OVER *(finishes participation on to the current conversation)*
    * [subject] SKIP *(skip current round only)*
    
For each of the previous sentences, the subject is always present before the verb. However, the subject can be omitted. In this case, the subject is determined by the context: if stated by a certain speaker, the subject becomes the speaker, otherwise it comes indefinite (all applicable players).

* Operators: used to frame sentences and link them to other subjects or sentences

	* [subject] REQUEST ([sentence])

Same as in the previous section, subject can be also be omitted here.

* Grammar

    * A statement consists of one or more sentences
    * Sentences can be separated by parentheses
    * You can use an operator before a sentence
    * The sentence following an operator is delimited by parentheses. 
    * Although a [subject] is required, if omitted, the speaker is regarded as the subject.

* Example Sentences 

	* COMINGOUT Agent1 SEER　 　　　　　　　*(a declaration that Agent1 is a seer)* 
	* Agent0 COMINGOUT Agent0 SEER　　　　*(Agent0 declares himself as a seer)*
	* DIVINED Agent1 HUMAN 　　　　　　　　　*(the divination shows that Agent1 is a Human)*
	* Agent0 DIVINED Agent2 WEREWOLF　　　*(the divination by Agent0 shows that Agent2 is a Werewolf)*  
	* REQUEST (Agent2 DIVINATION Agent3)　　*(a request is made to Agent2 to perform divination on Agent3)*
	* GUARD Agent2 			　　　　　　　　　　　　　　*(to protect Agent2)*
	* Agent1 REQUEST (Agent0 GUARD Agent3)　*(Agent1 requests that Agent0 protects Agent3)*

* How requests are interpreted
	
	* REQUEST ([subject] ESTIMATE [target] [role])
		* if [subject] is present: *[subject], please suggest that [target] could be a [role]*
		* if there is no subject: *everyone, please suggest that [target] could be a [role]*

	* REQUEST ([subject] COMINGOUT [target] [role])
		* if [subject] is present: *[subject], please report that [target] is [role]*
		* if there is no subject: *someone, please report that [target] is [role]*
 
	* REQUEST ([subject] DIVINATION [target])
		* if [subject] is present: *[subject], please perform divination on [target]*
		* if there is no subject: *let's perform divination on [target]*

	* REQUEST ([subject] GUARD [target])
		* if [subject] is present: *[subject], please protect [target]*
		* if there is no subject: *let's protect [target]*

	* REQUEST ([subject] VOTE [target])
		* if [subject] is present: *[subject], please vote on [target]*
		* if there is no subject: *let's vote on [target]*

	* REQUEST ([subject] ATTACK [target])
		* if [subject] is present: *[subject], please attack [target]*
		* if there is no subject: *let's attack [target]*

	* REQUEST ([subject] DIVINED [target] [species])*
		* if [subject] is present: *[subject], please report that result of divination on [target] is [species]*
		* if there is no subject: *please, someone perform divination on [target]*

	* REQUEST ([subject] IDENTIFIED  [target] [species])
		* if [subject] is present: *[subject], please report that [target] was a [species]*
		* if there is no subject: *someone, please report that [target] was a [species]*

	* REQUEST ([subject] GUARDED  [target])
		* if [subject] is present: *[subject], please report that you protected [target]*
		* if there is no subject: *someone, please report that you protected [target]*

	* REQUEST ([subject] AGREE  [talk number])
		* if [subject] is present: *[subject], please report that you agree with [talk number]*
		* if there is no subject: *everyone, please report that you agree with [talk number]*

	* REQUEST ([subject] DISAGREE  [talk number])
		* if [subject] is present: *[subject], please report that you disagree with [talk number]*
		* if there is no subject: *everyone, please report that you disagree with [talk number]*

	* REQUEST ([subject] OVER)
		* if [subject] is present: *[subject], please finish your talking for now*
		* if there is no subject: *everyone, please finish your talking for now*

	* REQUEST ([subject] SKIP)
		* if [subject] is present: *[subject], don't say anything for this turn*
		* if there is no subject: *everyone, please don't say anything for this turn*
