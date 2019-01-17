# What is AIWolf?

Quoting from [aiwolf.org](http://aiwolf.org/en/introduction):

> a project to create an “Artificial Intelligence Werewolf” (AIWolf) to play as the werewolf in place of a human player. The objective of this comprehensive project is not only to develop a game-playing algorithm, but also to develop virtual agents, real robots, and so on. The We

The AI Competition currently has 2 branches, one protocol-based where agents can use a predefined grammar to communicate, and one NLP-based. This repository has information on the protocol-based branch of the competition.

# AIWolf Protocol Specification (ver2.01, 2017)

This guide will include keywords, sentences, operators and grammar related to the protocol specification of the AIWolf competition.

* List of keywords used for building sentences and their usage: 

  * [subject], [target]: one of the agents playing the game (Agent0 ~ AgentN) 
  * [role]: 6 types of roles supported (VILLAGER, SEER, MEDIUM, BODYGUARD, WEREWOLF, POSSESSED)
  * [species]: 2 types of species supported (HUMAN, WEREWOLF)
  * [verb]: 13 types of verbs allowed (full list below)
  * [talk number]: unique id for each sentence (composed by [day number] and [talk_id] for the sentence in that day) 

* Sentences: (13 different types in total)

  * Sentences that express ideas or intetion from the player
  
    * [subject] ESTIMATE [target] [role] *(The [subject] is estimating that [target] is [role])*
    * [subject] COMINGOUT  [target][role] *(The [subject] is stating that [target] is [role])*

  * Sentences for basic actions of a Werewolf game
  
    * [subject] DIVINATION [target]
    * [subject] GUARD [target]
    * [subject] VOTE [target]
    * [subject] ATTACK [target]

  * Sentences that express the result of a certain action

	  * [subject] DIVINED [target] [species]
    * [subject] IDENTIFIED [target] [species]
    * [subject] GUARDED [target]

*(keyword INQUESTED was used before 2017) 

  * Sentences to express agreement, disagreement

    * [subject] AGREE [talk number]
    * [subject] DISAGREE [talk number]
	
  * Sentences related to the flow of the conversation 

    * [subject] OVER *(finishes participation on to the current conversation)*
    * [subject] SKIP *(skip current round only)*
    
For each of the previous sentences, the subject is always present before the verb. However, the subject can be omitted. In this case, the subject is determined by the context: if stated by a certain speaker, the subject becomes the speaker, otherwise it comes indefinite (all applicable players).
