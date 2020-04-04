import json
from getFeatures import get_everyday_features
import numpy as np
filev = np.load('emotion_words.npz', mmap_mode='r',allow_pickle=True)
v=filev['re']


data={}
data["name"]="key_words"
data["children"]=[]
all_data = v
for i in range(7):
    t1_0=[{"name":t[0],"value":t[1]} for t in all_data[i][1]]
    s1 =set()
    t2_0=[]
    for t in all_data[i][2]:
        if (t[0][0],t[0][1]) not in s1 and (t[0][1],t[0][0]) not in s1 and t[0][0]!='' and t[0][1]!='':
            s1.add(t[0])
            print(s1)
            t2_0.append({"name": t[0], "value": t[1]})
    t1_1 = [{"name": t[0], "value": t[1]} for t in all_data[i][3]]
    s2=set()
    t2_1=[]
    for t in all_data[i][4]:
        if (t[0][0],t[0][1]) not in s2 and (t[0][1],t[0][0]) not in s2 and t[0][0]!='' and t[0][1]!='':
            s2.add(t[0])
            t2_1.append({"name": t[0], "value": t[1]})
    data["children"].append({"name":"3."+str(i+17),
                             "children":[
                                 {"name":"negative_words_1","children":t1_0},
                                 {"name": "negative_words_2", "children": t2_0},
                                 {"name": "positive_words_1", "children": t1_1},
                                 {"name": "positive_words_2", "children": t2_1}
                             ]})
with open('words_all.json', 'w') as outfile:
    json.dump(data, outfile)
