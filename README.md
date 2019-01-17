# What is AIWolf?

Quoting from [aiwolf.org](http://aiwolf.org/en/introduction):

> a project to create an “Artificial Intelligence Werewolf” (AIWolf) to play as the werewolf in place of a human player. The objective of this comprehensive project is not only to develop a game-playing algorithm, but also to develop virtual agents, real robots, and so on. 

The AI Competition currently has 2 branches, one protocol-based where agents can use a predefined grammar to communicate, and one NLP-based. This repository has information on the protocol-based branch of the competition.

To learn the rules and how to play the Werewolf game, please refer to [this website](https://www.playwerewolf.co/rules/) 

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
