from Conversation import Conversation

TIMEOUT = 120000
#Contains information about a certain user and a list of conversations this user had with Marie.
class Person:
    def __init__(self,convDict,id=None,fName="",lName="",personDict=None):
        #The preferred method is to pass a dictionary and have the Person class parse it. However, parameters can also be passed individually
        if personDict is not None:
            #TODO: fname and lastname not guaranteed
            self.lName = personDict["lastName"]
            self.fName = personDict["firstName"]
            self.id = personDict["fbid"]
        else:
            self.lName = lName
            self.fName = fName
            self.id = id
        self.convList = []
        self.parseConvDict(convDict)

    #Parses the conversation dict passed on from the json logs into the OO structure
    def parseConvDict(self,convDict):
        try:
            for key, messageDict in convDict["messages"].items():
                self.parseMessageDict(messageDict)
        #Older files have a list of messages instead of a dict, this handles it.
        except Exception as e:
            #if the list is empty, discard it
            if len(convDict["messages"]) == 0:
                print("EMPTY DICT")
            else:
                for messageDict in convDict["messages"]:
                    self.parseMessageDict(messageDict)

    def parseMessageDict(self,messageDict):
        # Make a new conversation if there is none yet
        if self.convList == []:
            conv = Conversation()
            conv.addUtterance(messageDict)
            self.convList.append(conv)
        else:
            # calculate the time difference between this message and the last message in the conversation
            timeDiff = int(messageDict["timestamp"]) - self.convList[-1].lastUttTime
            # If the message is older than the most recent message, it is a duplicate and can be discarded
            if timeDiff <= 0:
                pass
            # If the message is within the timeout limit, add it to the conversation, else make a new one
            elif timeDiff < TIMEOUT:
                self.convList[-1].addUtterance(messageDict)
            else:
                conv = Conversation()
                conv.addUtterance(messageDict)
                self.convList.append(conv)

    #GET all intents of a certain user, ordered by conversation
    #Returns a list of lists, each sublist being a sequence of intents in a conversation
    def getPersonIntents(self):
        personIntentList = []
        for conversation in self.convList:
            personIntentList.extend(conversation.getConversationIntents())
        return personIntentList

    #GET all intents with associated user text
    #Returns a list of list of tuples. Each tuple contains the user input and associated detected intent
    def getPersonIntentsWithText(self):
        personIntentList = []
        for conversation in self.convList:
            personIntentList.extend(conversation.getConversationIntentsWithText())
        return personIntentList