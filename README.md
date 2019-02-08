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

# AIWolf Competition General Rules

There are two formats of games being run at the AIWolf competition: with 5 or 15 players each game. The role distribution happens as fololows:

| Role      | 5 Players  | 15 Players |
| --------- | ----------:| ----------:|
| Villager  | 2 | 8 |
| Seer      | 1 | 1 |
| Possessed | 1 | 1 |
| Werewolf  | 1 | 3 |
| Medium    | - | 1 |
| Bodyguard | - | 1 |

The following fluxogram (adapted from the original [4th AIWolf Competition regulation document](https://github.com/ehauckdo/AIWoof/blob/master/docs/4th_AIWolf_Competition_Rules.pdf)) describes the flow of a Werewolf game in the competition platform: 

![alt text](https://github.com/ehauckdo/AIWoof/blob/master/docs/aiwolf_fluxogram.png "Fluxogram of a Werewolf game")

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

To execute the python script, you need a few libraries including numpy, pandas, etc. To check which libraries and which versions you need, check the requirements.txt file in the root folder. You can install all of them at once by running:

```
pip install -r requirements
```

It is highly recommended to setup a virtual environment before running this command, to assure there will be no conflicits with already installed libraries. You can check how to install virtualenv and how to create a new environment [here](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/).

Once the server is set up and you have the required libraries, you can connect the sample python agent in the current repository by executing

```
./aiwoof.py -h localhost -p 10000
```

You can also request a role to the server by passing -r [ROLE] as an argument (roles can be VILLAGER, SEER, MEDIUM, BODYGUARD, POSSESSED, WEREWOLF).

# AIWolf Protocol Specification (ver3.6, 2019)

This guide will include keywords, sentences, operators and grammar related to the protocol specification of the AIWolf competition. The official specification for the competition (in Japanese) can be found [here](http://aiwolf.org/control-panel/wp-content/uploads/2014/03/protocol_2017-2.pdf).

* List of keywords used for building sentences and their usage: 

  * [subject], [target]: one of the agents playing the game (Agent0 ~ AgentN) ???
  * [role]: 6 types of roles supported (VILLAGER, SEER, MEDIUM, BODYGUARD, WEREWOLF, POSSESSED)
  * [species]: 2 types of species supported (HUMAN, WEREWOLF) ???
  * [verb]: 15 types of verbs allowed (full list below)
  * [talk number]: unique id for each sentence (composed by [day number] and [talk_id] for the sentence in that day) 
  * If ANY is specified for any of [subject][target][role][species]、then ANY can refer to any object in the set of [subject][target][role][species].

* Sentences: (13 different types in total)

  * Sentences that express ideas or intention from the player (2 types)
  
    * [subject] ESTIMATE [target] [role] *(The [subject] is suggesting that [target] could be [role])*
    * [subject] COMINGOUT  [target][role] *(The [subject] is stating that [target] is [role])*

  * Sentences for basic actions of a Werewolf game (4 types)
  
    * [subject] DIVINATION [target]
    * [subject] GUARD [target]
    * [subject] VOTE [target]
    * [subject] ATTACK [target]

  * Sentences that express the result of a certain action (5 types)

    * [subject] DIVINED [target] [species]
    * [subject] IDENTIFIED [target] [species]*
    * [subject] GUARDED [target]
    * [subject] VOTED [target]
    * [subject] ATTACKED [target]

*(keyword INQUESTED was used before 2017) 

  * Sentences to express agreement, disagreement

    * [subject] AGREE [talk number]
    * [subject] DISAGREE [talk number]
	
  * Sentences related to the flow of the conversation 

    * [subject] OVER *(finishes participation on to the current conversation)*
    * [subject] SKIP *(skip current round only)*
    
The two sentences above related to conversation flow can only be used as single sentences, never in a nested manner.

* Operators: used to frame sentences and link them to other subjects or sentences (8 types)

	* [subject] REQUEST [target] ([sentence])

Requests that target acts according to [sentence]. If [subject][target][role][species] in sentence is ANY, the action must be upon one of the available options of the set.

	* [subject] INQUIRE [target] ([sentence])

Inquires target about [sentence]. If ANY is not included in the sentence, target is simply asked if it agrees with the content. If ANY is included, it is required to answer with the appropriate object within the available objects of the set.

	* [subject] BECAUSE ([sentence1]) ([sentence2]) *(because of sentence1, subject is stating sentence2)*

	* [subject] DAY [day_number] ([sentence]) *(on day [day_number], the situation described in [sentence] took place)*
	
	* [subject] NOT ([sentence]) *(negate sentence)*

	* [subject] AND ([sentence1]) ([sentence2])... *(asserts that all sentences are true)*

	* [subject] OR ([sentence1]) ([sentence2]).... *(asserts that at least one sentence is true)*

	* [subject] XOR ([sentence1]) ([sentence2]) *(only one of the two sentences is true)*

* Grammar

    * A statement consists of one or more sentences
    * Sentences can be separated by parentheses
    * You can use an operator before a sentence
    * The sentence following an operator is delimited by parentheses. 
    * Although a [subject] is required, if omitted, the speaker is regarded as the subject.
    * The speaker [subject] can be omitted (unspecified). It is recommended to omit the subject when appropriate to make the sentences shorter. However, note that every agent should be able to interpret sentences in the full or shortened format. When [subject] is omitted in sentences with a wide scope, [subject] is interpreted as the speaker. In the case of sentences with a narrow scope, it depends on the operator, as follows:

		* REQUEST, INQUIRE: interpreted as the same as [target]
		* Other cases: interpreted as the same as [subject]


* Example Sentences 

	* COMINGOUT Agent1 SEER　 　　　　　　　*(a declaration that Agent1 is a seer)* 
	* Agent0 COMINGOUT Agent0 SEER　　　　*(Agent0 declares himself as a seer)*
	* DIVINED Agent1 HUMAN 　　　　　　　　　*(the divination shows that Agent1 is a Human)*
	* Agent0 DIVINED Agent2 WEREWOLF　　　*(the divination by Agent0 shows that Agent2 is a Werewolf)*  
	* REQUEST (Agent2 DIVINATION Agent3)　　*(a request is made to Agent2 to perform divination on Agent3)*
	* GUARD Agent2 			　　　　　　　　　　　　　　*(to protect Agent2)*
	* Agent1 REQUEST (Agent0 GUARD Agent3)　*(Agent1 requests that Agent0 protects Agent3)*

* Example Sentences (using REQUEST)

	* REQUEST Agent1 (ESTIMATE Agent2 [role]) 
		* *(requests Agent1 to estimate Agent2 as [role])*
	* REQUEST ANY (ESTIMATE Agent1 [role])  
		* *(requests everyone/someone to estimate Agent1 as [role])*
	* REQUEST Agent1 (COMINGOUT Agent2 [role])  
		* *(requests Agent1 to announce the role of Agent2 as [role])*
	* REQUEST ANY (COMINGOUT Agent1 [role])  
		* *(requests everyone/someone tto announce the role of Agent1 as [role])*
	* REQUEST Agent1 (DIVINATION Agent2)  
		* *(requests Agent1 to perform divination on Agent2)*
	* REQUEST ANY (DIVINATION Agent1)  
		* *(requests everyone/someone to perform divination on Agent1)*
	* REQUEST Agent1 (GUARD Agent2)  
		* *(requests Agent1 to protect Agent2)*
	* REQUEST ANY (GUARD Agent2)  
		* *(requests everyone/someone to protect Agent2)*
	* REQUEST Agent1 (VOTE Agent2)  
		* *(requests Agent1 to vote on Agent2)*
	* REQUEST ANY (VOTE Agent2)  
		* *(requests everyone/someone to vote on Agent2)*
	* REQUEST Agent1 (ATTACK Agent2)  
		* *(requests Agent1 to attack Agent2)*
	* REQUEST ANY (Attack Agent1)  
		* *(requests everyone/someone to attack Agent1)*
	* REQUEST Agent1 (DIVINED Agent2 [species])  
		* *(requests Agent1 to announce the result of a divination in which Agent2 is releaved as [species])*
	* REQUEST ANY (DIVINED Agent2 [species])  
		* *(requests everyone/someone to announce the result of a divination in which Agent2 is releaved as [species])*
	* REQUEST Agent1 (IDENTIFIED Agent2 [species])  
		* *(requests Agent1 to state that Agent2 was identified as [species] after dying)*
	* REQUEST ANY (IDENTIFIED Agent2 [species])  
		* *(requests everyone/someone to state that Agent2 was identified as [species] after dying)*
	* REQUEST Agent1 (GUARDED Agent2)  
		* *(requests that Agent1 state that he has protected Agent2)*
	* REQUEST ANY (GUARDED Agent2)  
		* *(requests everyone/someone to state that he has protected Agent2)*
	* REQUEST Agent1 (AGREE [talk number])  
		* *(requests that Agent1 state that he agrees with [talk number])*
	* REQUEST ANY (AGREE [talk number])  
		* *(requests everyone/someone to state that they agree with [talk number])*
	* REQUEST Agent1 (DISAGREE [talk number])  
		* *(requests that Agent1 state that he disagrees with [talk number])*
	* REQUEST ANY (DISAGREE [talk number])  
		* *(requests everyone/someone to state that they disagree with [talk number])*

* Exemple Sentences (using BECAUSE)

	* Agent2 BECAUSE (DAY 1 Agent1 vote Agent2) (vote Agent1) *(Agent2 is voting on Agent1 because on DAY 1 Agent 1 voted on Agent2)*

* Example Sentences (using INQUIRE)

	* Agent2 INQUIRE Agent1 (VOTED ANY) / Agent2 INQUIRE Agent1 (Agent1 VOTED ANY)  
		* *(Agent2 asks Agent1 who Agent1 voted)*
	* Agent2 INQUIRE Agent1 (VOTE ANY) / Agent2 INQUIRE Agent1 (Agent1 VOTE ANY)  
		* *(Agent2 asks Agent1 who Agent1 is goinG to vote)*
	* Agent2 INQUIRE Agent1 (ESTIMATE Agent2 WEREWOLF) / Agent2 INQUIRE Agent1 (Agent1 ESTIMATE Agent2 WEREWOLF)  
		* *(Agent2 asks Agent1 if Agent1 thinks he is a WEREWOLF)*

* Example Sentences (using ANY)

Using ANY in a statement is equivalent to using the same statement with all available options expanded and joined by OR: 

Agent2 INQUIRE Agent1 (VOTED ANY)
is equivalent to
Agent2 INQUIRE Agent1 (OR (VOTED Agent1) (VOTED Agent2) (VOTED Agent3)…)

REQUEST ANY (DIVINED [agent] [species])
is equivalent to
OR (REQUEST Agent1 (DIVINED [agent] [species])) (REQUEST Agent2 (DIVINED [agent]
[species])) (REQUEST Agent2 (DIVINED [agent] [species]))…

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
