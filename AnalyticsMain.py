import json
import os
import pickle
from Person import Person
from Analysis import Analysis
import re

STARTDATE = 20170829
DEBUG = True
'''
Person
    ID
    Name
    [Conversation]

Conversation
    [Utterance]
'''
dir = os.getcwd()
LOGDIR = "C:\\Users\\demeyde\\Documents\\Craftworkz\\INGAnalytics\\Logs"
#LOGDIR = "T:\\Marie\\Log\\Production\\MiddleMan_IN"

def checkAndAdd(personList,newPerson):
    for persons in personList:
        if newPerson["user"]["fbid"] == persons.id:
            try:
                persons.parseConvDict(newPerson["messaging"])
                return personList
            except Exception as e:
                print("-----------------------------")
                print("ERROR PARSING JSON")
                print("Exception: "+ str(e))
                print("Json:")
                print(newPerson)
                print("-----------------------------")
    # If the person is not already in the list add him by calling the Person constructor and passing the user parameters
    try:
        personList.append(Person(convDict=newPerson["messaging"],personDict=newPerson["user"]))
    except Exception as e:
        print("-----------------------------")
        print("ERROR PARSING JSON")
        print("Exception: "+ str(e))
        print("Json:")
        print(newPerson)
        print("-----------------------------")

    return personList


#Builds a dictionary where each use case is a key, and each intent a value associated with its use case
#Returns a dict with the following format: {useCase1:[Intent1,Intent2,...],useCase2:[Intent1,Intent2],...}
def buildIntentDict():
    useCase = set()
    intentList = []
    #This loop builds a set of use cases and a list of intents
    #The json files in the folder are provided by exporting Marie from api.ai and copying the intent json files into the Intents folder
    dir = os.getcwd()
    folderdir = os.path.join(dir,"Intents")
    for filename in os.listdir(folderdir):
        #We don't add tests
        if filename[0] == "_" and filename[1] == "_":
            continue
        #we remove the json file extention to get the actual intent name
        intentname = filename.split(".json")[0]
        intentList.append(intentname)
        #We split the intent at the number and remove the leading and trailing underscore characters
        group = re.split('(\D+)', intentname)[1].strip("_")
        #Since there are a lot of different Generic use cases, we bundle them all in one.
        group = "Generic" if "Generic" in group else group
        group = "unblock_card" if ("_rn" in group or "_ry" in group) else group
        useCase.add(group)

    #This loop builds the intent dictionary. There is probably a better way to build the dict in the previous loop, but the performance loss is minimal
    intentDict = {}
    for key in useCase:
        if "Generic" in key:
            intentDict["Generic"] = ["Generic"]
            continue
        valueList = []
        for value in intentList:
            if key in value:
                valueList.append(value)
        intentDict[key] = valueList

    return intentDict

#Right now, we provice a flow for dataloading and data analysis. This will probable not be necessary in the future
if not DEBUG:
    personList = []

    #Returns all filenames in the folder
    count = sum(len(files) for r,d,files in os.walk(LOGDIR))
    print(count)
    current = 1

    for root,dir,files in os.walk(LOGDIR):
        # This is a quick and hacky way to reject folders that are earlier than our start date, and to reject folders
        # with a different kind of name
        try:
            if int(root[-8:]) < STARTDATE:
                continue
        except:
            continue
        for filename in files:
            #Discards non txt files
            if ".txt" not in filename:
                continue
            try:
                with open(os.path.join(root,filename),"rb") as data_file:                    
                    data = json.load(data_file)
                    for key,element in data.items():
                        personList = checkAndAdd(personList, element)
            except Exception as e:
                print("----------------------------")
                print("ERROR LOADING FILE")
                print(e)
                print(filename)
                print("----------------------------")
                continue
            current += 1
            print("Progress:"+str((current*100/count))+"%")
    pickle.dump(personList,open("personlist.pickle","wb"))


#For analysis, we build a list on three different levels: Persons,Conversations and Utterances
#go = input("Press Enter if you want to analyse")
#if go == "": DEBUG = True
DEBUG = True
if DEBUG:
    personList = pickle.load(open("personList.pickle","rb"))
    conversationList = []
    utteranceList = []
    for person in personList:
        for conversation in person.convList:
            conversationList.append(conversation)
            for utterance in conversation.utteranceList:
                utteranceList.append(utterance)

    intentdict = buildIntentDict()
    a = Analysis(personlist=personList,conversationlist=conversationList,utterancelist=utteranceList,usecasedict=intentdict,startDate=STARTDATE)
    a.getConversationsExcel()
    a.getFallbackConversationsExcel()
    a.getFailedConversationsExcel()
    a.save()
    #a.getPersons()
    #a.getFallbackConversations()
    #a.getFailedConversations()
    #a.buildGraph()
