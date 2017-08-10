import os
import json
import csv

#This file contains a lot of helper methods that I mostly use to search intents, it has nothing to do with Analytics


def findEvents():
    for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
        if "fallback" in filename.lower() or "_Generic" in filename or not any(i.isdigit() for i in filename):
            continue
        with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents\\"+filename,"r",encoding='utf8') as file:
            try:
                jsondict = json.load(file)

def contextToUseCase(contextnamelist):
    usecaselist = []
    for item in contextnamelist:
        usecaselist.append(item[4:].replace("_"," ").capitalize())
    return usecaselist

def checkEndofConversation():
    for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
        if "fallback" in filename.lower() or "_Generic" in filename or not any(i.isdigit() for i in filename):
            continue
        with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents\\"+filename,"r") as file:
            jsondict = json.load(file)
            messagedict = jsondict["responses"][0]["messages"]
            for channel in messagedict:
                if channel["type"] != 0:
                    continue
                else:
                    if isinstance(channel["speech"], str):
                        if "?" not in channel["speech"]:
                            print("INTENT: " + filename)
                            print("UTTERANCE: " + channel["speech"])
                            print("-------------------------------")
                    else:
                        for utt in channel["speech"]:
                            if "?" not in utt:
                                print("INTENT: "+filename)
                                print("UTTERANCE: "+utt)
                                print("-------------------------------")

def checkContexts():
    for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
        if "fallback" in filename.lower() or "_Generic" in filename or not any(i.isdigit() for i in filename):
            continue
        with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents\\"+filename,"r",encoding='utf8') as file:
            try:
                jsondict = json.load(file)
            except Exception as e:
                print("ERROR:"+filename)
                print(e)
            messagedictlow = jsondict["responses"][0]
            messagedict = jsondict["responses"][0]["affectedContexts"]
            for context in messagedict:
                if context["name"] == "ctx_end_of_conversation":
                    print("INTENT: " + filename)
                    print("----------------------")

#Short utterances in entry intents
def checkShortUtterances():
    for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
        #Skip fallback intents
        if "fallback" in filename.lower():
            continue
        #Open the file
        with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents\\" + filename, "r", encoding='utf8') as file:
            jsondict = json.load(file)
            #Define input and output contexts
            outcontexts = jsondict["responses"][0]["affectedContexts"]
            incontexts = jsondict["contexts"]

            #Skip intents shielded by input contexts
            if len(incontexts) > 0:
                continue

            print("----------------------")
            print("INTENT: " + filename)
            print("----------------------")
            utterancelist = jsondict["userSays"]

            for utterance in utterancelist:
                combinedUtterance = ""
                # Utterances are split if they contain entities, this merges them back together
                for text in utterance["data"]:
                    combinedUtterance += text["text"]

                #disregard utterances with more than 4 words
                if len(combinedUtterance.split()) < 4:
                    print(combinedUtterance)

#Check lifespans of output contexts
def checkLifespans():
    for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
        #Skip fallback intents
        if "fallback" in filename.lower():
            continue
        #Open the file
        with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents\\" + filename, "r", encoding='utf8') as file:
            jsondict = json.load(file)
            #Define input and output contexts
            outcontexts = jsondict["responses"][0]["affectedContexts"]
            for context in outcontexts:
                #Lifespans should only be values 0,1,3,5
                if int(context["lifespan"]) not in [0,1,3,5]:
                    print(filename)
                    print(context["lifespan"])

#Add all usecases in failed conversations

#Check end of conversation
#Check naming conventions
#verify that all non generic use case contexts are eventually set to 0
#Get overview of all actions per day to ICC



#Visualise use cases

def checkActions():
    for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
        if "fallback" in filename.lower() or "_Generic" in filename or not any(i.isdigit() for i in filename):
            continue
        with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents\\"+filename,"r", encoding='utf8') as file:
            jsondict = json.load(file)
            messagedictlow = jsondict["responses"][0]
            messagedict = jsondict["responses"][0]["messages"]
            if "action" in messagedictlow:
                action = messagedictlow["action"]
                if action in ["showicccontactdetails", "activecardlist", "", "endofconversationconfirmed", "resetsmscontexts"]:
                    continue
                for channel in messagedict:
                    if channel["type"] != 0:
                        continue
                    else:
                        if isinstance(channel["speech"], str):
                                print("INTENT: " + filename)
                                print("UTTERANCE: " + channel["speech"])
                                print("ACTION: " + messagedictlow["action"])
                                print("-------------------------------")
                        else:
                            for utt in channel["speech"]:
                                    print("INTENT: " + filename)
                                    print("UTTERANCE: " + utt)
                                    print("ACTION: " + messagedictlow["action"])
                                    print("-------------------------------")
                                    break
            else:
                continue

def checkICCaction():
    for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
        if "fallback" in filename.lower() or "_Generic" in filename or not any(i.isdigit() for i in filename):
            continue
        with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents\\"+filename,"r", encoding='utf8') as file:
            jsondict = json.load(file)
            messagedictlow = jsondict["responses"][0]
            messagedict = jsondict["responses"][0]["messages"]
            if "action" in messagedictlow:
                action = messagedictlow["action"]
                if action  not in ["showicccontactdetails"]:
                    continue
                for channel in messagedict:
                    if channel["type"] != 0:
                        continue
                    else:
                        if isinstance(channel["speech"], str):
                                print("INTENT: " + filename)
                                print("UTTERANCE: " + channel["speech"])
                                print("ACTION: " + messagedictlow["action"])
                                print("-------------------------------")
                        else:
                            for utt in channel["speech"]:
                                    print("INTENT: " + filename)
                                    print("UTTERANCE: " + utt)
                                    print("ACTION: " + messagedictlow["action"])
                                    print("-------------------------------")
            else:
                continue

def checkICCmessage():
    for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
        if "fallback" in filename.lower() or "_Generic" in filename or not any(i.isdigit() for i in filename):
            continue
        with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents\\"+filename,"r", encoding='utf8') as file:
            jsondict = json.load(file)
            messagedictlow = jsondict["responses"][0]
            messagedict = jsondict["responses"][0]["messages"]
            if "action" in messagedictlow:
                action = messagedictlow["action"]
            else:
                action = "NONE"
            for channel in messagedict:
                if channel["type"] != 0:
                    continue
                else:
                    if isinstance(channel["speech"], str):
                        if "+" in channel["speech"] or "ICC" in channel["speech"] or "Contact" in channel["speech"]:
                            print("INTENT: " + filename)
                            print("UTTERANCE: " + channel["speech"])
                            print("ACTION: " + action)
                            print("-------------------------------")
                    else:
                        for utt in channel["speech"]:
                            if "+" in utt or "ICC" in utt or "Contact" in utt:
                                print("INTENT: " + filename)
                                print("UTTERANCE: " + utt)
                                print("ACTION: " + action)
                                print("-------------------------------")

def getIntentsWithActions():
    with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\actions.csv", "w") as writefile:
        writer = csv.writer(writefile)
        for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
            with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents\\"+filename,"r", encoding='utf8') as file:
                jsondict = json.load(file)
                messagedictlow = jsondict["responses"][0]
                messagedict = jsondict["responses"][0]["messages"]
                if "action" in messagedictlow:
                    action = messagedictlow["action"]
                    if action in [""]:
                        continue
                    writer.writerow([action,filename.split(".")[0]])
                else:
                    continue

def checkReplies():
    for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
        intentname = filename.split(".")[0]
        with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents\\"+filename,"r", encoding='utf8') as file:
            jsondict = json.load(file)
            messagedict = jsondict["responses"][0]["messages"]
            for reply in messagedict:
                try:
                    #print(reply["speech"])
                    if "help" in reply["speech"].lower():
                        if "generic" in intentname.lower():
                            print(intentname)
                            print(reply["speech"])
                except: pass


def findIntentJumps():
    #Build intentname,action dict
    actiondict = {}
    #Build intentname,event dict
    eventdict = {}
    for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
        intentname = filename.split(".")[0]
        with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents\\"+filename,"r", encoding='utf8') as file:
            jsondict = json.load(file)
            messagedictlow = jsondict["responses"][0]
            messagedict = jsondict["responses"][0]["messages"]
            events = jsondict['events']
            if len(events) > 0:
                eventdict[events[0]["name"]] = intentname
            try:
                action = messagedictlow["action"]
                if "fireevent" in action:
                    if action.split(":")[1] in actiondict:
                        actiondict[action.split(":")[1]].append(intentname)
                    else:
                        actiondict[action.split(":")[1]] = [intentname]
            except:
                continue
    jumpingintentlist = []
    for key in actiondict:
        if key in eventdict:
            #This conditions is there to only return external jumps
            for intent in actiondict[key]:
                if intent.split("_")[0] != eventdict[key].split("_")[0]:
                    jumpingintentlist.append(intent)
    return jumpingintentlist

    #NOW CREATE PAIRS OF KEYS

def addToUseCaseDict(usecasedict,intentname,contextname,category):
    for contextkey,value in usecasedict.items():
        if value["ContextName"] == contextname:
            print(usecasedict[contextkey]["Intents"][category])
            usecasedict[contextkey]["Intents"][category].append(intentname)
            return usecasedict


def categorizeIntents(self):
    generalUseCaseContextList = ["ctx_activate_card", "ctx_sms_authentication", "ctx_card_delivery",
                                 "ctx_card_stop",
                                 "ctx_info_charges_abroad", "ctx_newpin", "ctx_order_card", "ctx_pin_by_sms",
                                 "ctx_unblock_card", "ctx_unblock_card_ry", "ctx_unblock_card_rn", "ctx_use_abroad"]
    generalUseCaseContextSet = set(generalUseCaseContextList)
    usecaseNameList = self.contextToUseCase(generalUseCaseContextList)

    # Build the dictionary that will be converted to JSON in the end
    finaldict = {}
    for usecase, context in zip(usecaseNameList, generalUseCaseContextList):
        finaldict[usecase] = {"ContextName": context, "Intents":
            {"Start": [], "Intermediate": [], "End": [], "Fallback": [], "Jump": []}}

    for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
        intentname = filename.split(".")[0]

        # Open the file
        with open("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents\\" + filename, "r",
                  encoding='utf8') as file:
            hasinput = True
            hasoutput = True
            jsondict = json.load(file)

            # Define input and output contexts
            outcontextsdict = jsondict["responses"][0]["affectedContexts"]
            outcontextslist = []
            for context in outcontextsdict:
                if context['lifespan'] > 0:
                    outcontextslist.append(context["name"])
            incontextslist = jsondict["contexts"]

            # See if any of the general contexts are present in either the input or output contexts
            # If it is present, save the fallback
            if generalUseCaseContextSet.isdisjoint(incontextslist):
                hasinput = False
            else:
                incontext = next(iter(generalUseCaseContextSet.intersection(incontextslist)))

            if generalUseCaseContextSet.isdisjoint(outcontextslist):
                hasoutput = False
            else:
                outcontext = next(iter(generalUseCaseContextSet.intersection(outcontextslist)))

            '''
            We use the following truth table to determine what the intent is:
            Input/Output    Intent Category         Remarks

            False/False     Generic intent
            False/True      Start intent
            True/False      End intent              Checks end_of_conversation to be sure
            True/True       Intermediate intent*    *if the context is not the same in input and output, it's an exit
                                                    because it jumps from one use case to another
            '''

            if (not hasinput) and (not hasoutput):
                continue
            elif (not hasinput) and hasoutput:
                finaldict = self.addToUseCaseDict(usecasedict=finaldict, intentname=intentname, contextname=outcontext,
                                                  category="Start")
            elif hasinput and (not hasoutput):
                if "fallback" in intentname.lower() and hasinput:
                    finaldict = self.addToUseCaseDict(usecasedict=finaldict, intentname=intentname,
                                                      contextname=incontext, category="Fallback")
                    continue
                if "ctx_end_of_conversation" in outcontextslist:
                    finaldict = self.addToUseCaseDict(usecasedict=finaldict, intentname=intentname,
                                                      contextname=incontext, category="End")
                else:
                    print("FUCK: " + intentname)
            elif hasinput and hasoutput:
                if incontext == outcontext:
                    finaldict = self.addToUseCaseDict(usecasedict=finaldict, intentname=intentname,
                                                      contextname=incontext, category="Intermediate")
                else:
                    finaldict = self.addToUseCaseDict(usecasedict=finaldict, intentname=intentname,
                                                      contextname=incontext, category="Jump")
    return finaldict

def testOSwalk():
    for root,dirs,files in os.walk("C:\\Users\\demeyde\\Desktop\\ING\\Analytics"):
        print(root)
        print(dirs)
        print(files)
        print("-----------------------------")


testOSwalk()
