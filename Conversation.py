from Utterance import Utterance
import json

#Conversations contain a list of utterances, as well as some statistics about the conversation
class Conversation:
    _ID = 0
    def __init__(self):
        self.id = self._ID
        self.__class__._ID += 1
        self.utteranceList = []
        self.intentList = ["Start"]
        self.firstUttTime = 0
        self.lastUttTime = 0
        self.entryIntent = None
        self.exitIntent = None
        self.convDuration = 0
        self.messageNo = 0

    #Add an utterance (user input or reply) to the conversation
    def addUtterance(self, uttDict):
        #If the conversation is new, set the first message time and intent
        if self.firstUttTime == 0:
            self.firstUttTime = int(uttDict["timestamp"])
            #Somehow sometimes a message from a user gets confused with a message from marie
            try:
                self.entryIntent = uttDict["intentName"]
            except:
                self.entryIntent = "ERROR"
                uttDict["intentName"] = "ERROR"
                uttDict["type"] = "Incoming"
                json.dump(uttDict, open("log.txt", 'a'),indent=2)
                print("Intervention detected")


        self.lastUttTime = int(uttDict["timestamp"])
        self.convDuration = self.lastUttTime - self.firstUttTime

        #If an utterance is made by a user, make a new utterance. Else, add it as a reply
        if uttDict["type"] == "Incoming":
            #if self.entryIntent == None:
            self.intentList.append(uttDict["intentName"])
            self.exitIntent = uttDict["intentName"]
            utt = Utterance(uttDict)
            self.utteranceList.append(utt)
        else:
            self.utteranceList[-1].addReply(uttDict)

    def getConversationIntents(self):
        convIntentList = []
        for utterance in self.utteranceList:
            convIntentList.extend(utterance.intentName)
        return convIntentList

    def getConversationIntentsWithText(self):
        convIntentList = []
        for utterance in self.utteranceList:
            convIntentList.extend((utterance.inputUtt,utterance.intentName))
        return convIntentList