from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
import os
import re
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pickle
import tweepy

consumer_key = 'sUScSVIjrgUd5cO96QjAPHz5G'
consumer_secret = 'zrfgZX8Kig4uodBEH7BfRYFa1Xj81ZTOLylczo1utXWjDW6Uls'
access_token = '1217112496491749376-buFH3a4MADn0570uexCEetJAcdLAZa'
access_token_secret = 'XaeyAgs3ppsgnjsSKG09Rj4fCcBqXlNknefO2mtAX8ko3'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

conf = SparkConf().setAppName("spark_json2")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

MAX_SEQUENCE_LENGTH = 500
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
word_index = tokenizer.word_index
model = load_model('my_model3_lstm.h5')

def get_emotion(sentence):
    s = classifier(sentence)
    if s>=0.5: return 1
    else: return 0

def classifier(sentence):
    global model
    global tokenizer
    input_text = [sentence]
    input_sequence = tokenizer.texts_to_sequences(input_text)
    input_data = pad_sequences(input_sequence, maxlen=MAX_SEQUENCE_LENGTH)
    return model.predict(input_data)[0][0]

def get_retweeters(id):
    try:
        return set(api.retweeters(id=id, count=100))
    except tweepy.TweepError:
        return set()

def get_users_features():
    global_rdd = sc.emptyRDD()
    data_file_names = os.listdir('data/')
    for data_file_name in data_file_names[1:]:
        print(data_file_name)
        jsons_sql = sqlContext.read.json('data/' + data_file_name)
        userid_fulltext_rdd = jsons_sql.rdd.map(lambda line: (line.user.id, (
        classifier(line.full_text), (line.favorite_count + line.retweet_count), get_retweeters(line.id), 1)))
        global_rdd += userid_fulltext_rdd  #
    temp_results = global_rdd.reduceByKey(
        lambda n1, n2: (n1[0] + n2[0], n1[1] + n2[1], n1[2].union(n2[2]), n1[3] + n2[3]))
    results = temp_results.map(lambda x: (x[0], x[1][0] / x[1][3], x[1][1] / x[1][3], x[1][2]))
    result = results.collect()
    re = np.array(result)
    np.savez('users_emotion_influencer_retweets.npz', re=re)

def get_words(text):
    with open('stopwords.txt', 'r') as f:
        stopwords = set(f.read().split('\n'))
    s=set(re.split(r'[^A-Za-z\'\-]+',text.lower()))
    s=s.difference(stopwords)
    return list(map(lambda x:(x,1),s))
def get_words2(text,p):
    with open('stopwords.txt', 'r') as f:
        stopwords = set(f.read().split('\n'))
    s=set(re.split(r'[^A-Za-z\'\-]+',text.lower()))
    s=s.difference(stopwords)
    s =s.intersection(p)
    s.discard('')
    s = list(s)
    if len(s)==0: return [(('',''),1)]
    else:
        new_ls=[]
        for i in range(len(s)):
            for j in range(len(s)):
                if i!=j:
                    new_ls.append(((s[i],s[j]),1))
        return new_ls
def get_words3(text,p):
    with open('stopwords.txt', 'r') as f:
        stopwords = set(f.read().split('\n'))
    s=set([i[0] for i in text])
    s=s.difference(stopwords)
    s =s.intersection(p)
    s.discard('')
    s = list(s)
    if len(s)==0: return [(('',''),1)]
    else:
        new_ls=[]
        for i in range(len(s)):
            for j in range(len(s)):
                if i!=j:
                    new_ls.append(((s[i],s[j]),1))
        return new_ls
def get_everyday_features(): #calculate every day's positive and negative, calculate word count.
    data_file_names = os.listdir('data/')
    all_data = []
    for data_file_name in data_file_names[1:]:
        #data_file_name = 'covid_0316.json'
        data = []
        jsons_sql = sqlContext.read.json('data/' + data_file_name)
        total_rdd = jsons_sql.rdd.map(lambda line: (get_emotion(line.full_text), (1, get_words(line.full_text))))
        total_rdd = sc.parallelize(total_rdd.collect())
        daily_rdd = total_rdd.reduceByKey(
            lambda x1, x2: (x1[0] + x2[0], x1[1] + x2[1]))  # (emotion=1,(count,[text])),(0,...)
        emotion_rdd = daily_rdd.map(lambda x: (x[0], x[1][0]))  # (emotion=1,count),(e=0,count)
        words_rdd = daily_rdd.map(lambda x: x[1][1])  # ([text],[text])
        data.append(emotion_rdd.collect())
        for w in words_rdd.collect():
            rdd1 = sc.parallelize(w).reduceByKey(lambda x1, x2: x1 + x2)
            topk = rdd1.takeOrdered(200, key=lambda x: -x[1])
            p = [i[0] for i in topk]
            words_rdd2 = total_rdd.map(lambda x: get_words3(x[1][1], p))
            daily_words_rdd2 = words_rdd2.reduce(lambda l1, l2: l1 + l2)
            rdd2 = sc.parallelize(daily_words_rdd2).reduceByKey(lambda x1, x2: x1 + x2)
            topk2 = rdd2.takeOrdered(200, key=lambda x: -x[1])
            data.append(topk)
            data.append(topk2)
        all_data.append(data)
    np.savez('emotion_words.npz', re=all_data)
    return all_data


