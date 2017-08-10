class Utterance:
    def __init__(self, uttDict= None,type = None, seqnr=None, inputUtt=None, replyUtt=None, deltaT=None, timeStamp=None, intentName=None ,intentScore=None, sentimentScore=None):
        if uttDict is not None:
            self.inputUtt = uttDict["text"]
            #Some types of messages don't have certain fields. If so, set them to default
            self.intentName = uttDict["intentName"] if "intentName" in uttDict else "Postback"
            self.sentimentScore = uttDict["sentiment"] if "sentiment" in uttDict else 0
            self.intentScore = uttDict["intentConfidenceScore"] if "intentConfidenceScore" in uttDict else 1
            self.replyUtt = []
            self.timeStamp = uttDict["timestamp"]
        else:
            self.inputUtt = inputUtt
            self.replyUtt = []
            self.timeStamp = timeStamp
            self.intentName = intentName
            self.intentScore = intentScore
            self.sentimentScore = sentimentScore

    def addReply(self, replyDict):
        self.replyUtt.append(replyDict["text"])