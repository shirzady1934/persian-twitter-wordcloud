import re
import tweepy
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from config import fonts
from datetime import datetime
from wordcloud import WordCloud
from mytoken import APP_KEY, APP_SECRET, ACCESS_TOEKN, ACCESS_TOEKN_SECRET
#from arabic_reshaper import reshape as rshp
#from bidi.algorithm import get_display as dsp

try:
	from mytoken import username
except:
	username = input("Enter username:")
	

#Funtion for reshape words
#def reshape(word):
#	try:
#		return dsp(rshp(word))
#	except:
#		return ""

#Uncomment these 3 line and fill them!
#username = '' 
#APP_KEY = ""
#APP_SECRET = ""


auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
auth.set_access_token(ACCESS_TOEKN, ACCESS_TOEKN_SECRET)
twitter = tweepy.API(auth,wait_on_rate_limit=True)

user_timeline = []
for tweet in tweepy.Cursor(twitter.user_timeline,id=username, count=200).items():
	user_timeline.append(tweet)
	if len(user_timeline) >= 4000:
		break

tweets = []
for tweet in user_timeline:
    tweets.append(tweet._json['text'])

tweets_string = ' '.join(tweets)
no_links = re.sub(r'http\S+', '', tweets_string)
result = re.sub(r"\\[a-z][a-z]?[0-9]+", '', no_links)
result = re.sub(r"[-()\"#/@;:<>{}+=~|_.!*?,]", '', result)
result = re.sub('[A-z]', '', result)
result = re.sub("\d+", '', result)
words = result.split(" ")
words = [word for word in words if len(word) > 2]
stopwords = []

with open('./stopwords') as f:
	stopwords = [line.strip('\n') for line in f]

#Reshape words for display!
#words = [reshape(word) for word in words]
#stopwords = [reshape(word) for word in stopwords]

clean_string = ','.join(words)
mask = np.array(Image.open('./masks/mygraph.jpg'))
name_time = datetime.now().strftime('%y-%m-%d')

for font in fonts:
	font_name = font
	font_path = './fonts/%s.ttf' % font_name
	wc = WordCloud(background_color="white", max_words=500, mask=mask, stopwords=stopwords, font_path=font_path)
	wc.generate(clean_string)
	image = wc.to_image()
	image.save('./wordclouds/%s-%s-%s.png' % (username, font_name, name_time))
