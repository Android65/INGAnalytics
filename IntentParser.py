import os
import re
import networkx as nx
import matplotlib.pyplot as plt

r = re.compile("([a-zA-Z]+)([0-9]+)")
useCase = set()
intentList = []

i = 0
j = 0
for filename in os.listdir("C:\\Users\\demeyde\\Desktop\\ING\\Analytics\\Intents"):
    if filename[0] == "_" and filename[1] == "_":
        continue
    intentname = filename.split(".json")[0]
    intentList.append(intentname)
    group = re.split('(\D+)', intentname)[1].strip("_")
    group = "unblock_card" if("rn" in group or "ry" in group) else group
    group = "Generic" if "Generic" in group else group
    useCase.add(group)
    if "Generic" not in group:
        j += 1
    i += 1


intentDict = {}
k = 0
l = 0
m = 0
for key in useCase:
    valueList = []
    for value in intentList:
        if key in value:
            valueList.append(value)
    if len(valueList) > 1:
        k += 1
        l += len(valueList)
        #if key != "Generic":
            #l += len(valueList)
    else:
        m += 1
    intentDict[key] = valueList

G = nx.Graph()
for key, val in intentDict.items():
    for node in val:
        G.add_node(node)

nx.draw(G)
plt.show()





print("Total Non-Trivial Use Cases: "+str(k))
print("Total Non-Trivial Intents: " + str(l))
print(m)

