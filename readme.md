 More details are shown in Big-Data-Report.pdf

# Architecuture

## Data Preperation and Preprocessing

### Crawl Tweets Raw Data
https://drive.google.com/drive/folders/1yYzYO8ShHNNOwI5HtfTQwEPiojcpvavF?usp=sharing
We crawl and save raw tweets in search_tweets.py. We crawl the data and save it in data/.... The total number of tweets is about 200000. You can change the following parameters:
1. Key_words: covid19 OR covid OR coronavirus OR covid-19
2. Location: Singapore geocode:1.31,103.83,30km
3. Time: since 2020-03-16 until 2020-03-23

***Some tricks***: For standard developer, we can only get around 20000 every 15 mins, and every time we use the api to crawl data, it will choose the data from the latest, so we can set "max_id" in api, so every time we will search the tweets from the max_id. Another problem is about the location. The parameter name of location is "geocode" which is not obviously showed in twitter api document.

### Traing and Get RNN Model 
Run mainLSTM.py and save the model my_model3_lstm.h5. We already save it, so you can just use it without training the model again.

### Get Features 

#### 1. get_users_features()
Using spark-rdd to calculate the users' emotion, influencer_score and retweets number. The influencer_score is depend on favorite_num and retweets_num, which is the average of (favorate_num+retweets_num) of all the tweets of a user. Save it as 'users_emotion_influencer_retweets.npz'. You can read it in the following way: 

filev = np.load('users_emotion_influencer_retweets.npz', mmap_mode='r',allow_pickle=True)

v=filev['re']

For an example in v, [595632288 0.8223876953125 41706.0 set()], the first means user_id, the second means user's emotion, the third means user's influencer_score, the last one means the set of all the retweeter users'id.
The total number of users is 74172.

#### 2. get_everyday_features()
Run get_everyday_features() in getFeatures.py and save the number of different emotions and key words of different emotion group every day. We will have 7 days' emotion_words.npz files.

## Data visualizaition

### 1. Every day emotion and keywords
Check the data visualization through following links.

A. 7 day's emotion:
https://observablehq.com/@clearonexu/grouped-bar-chart

B. 7 day's keywords:
https://observablehq.com/@clearonexu/zoomable-circle-packing

There are 7 big circles, represents 7 days. In each circle, there is:

1. positive_words_1: In positive tweets, the single words_cloud.
2. positive_words_2: In positive tweets, the pair words_cloud.
3. negative_words_1: In negative tweets, the single words_cloud.
4. negative_words_2: In pnegative tweets, the pair words_cloud.

### 2. Tweets' retweeter graph 
