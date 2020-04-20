import numpy as np
import re
import matplotlib.pyplot as plt
from twython import Twython
from PIL import Image
from wordcloud_fa import WordCloudFa
from wordcloud import WordCloud
from datetime import datetime
from arabic_reshaper import reshape as rshp
from bidi.algorithm import get_display as dsp
from config import fonts
try:
	from mytoken import APP_KEY, APP_SECRET, username
except:
	pass

#Unused funtion
'''def reshape(word):
	try:
		return dsp(rshp(word))
	except:
		return "" '''

#Uncomment these 3 line and fill them!
#username = '' 
#APP_KEY = ""
#APP_SECRET = ""


'''client_args = {
        'proxies': {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
            }
}'''
twitter = Twython(APP_KEY, APP_SECRET)#, client_args=client_args)

user_timeline=twitter.get_user_timeline(screen_name=username, count=1) 
last_id = user_timeline[0]['id']-1
for i in range(20):
	batch = twitter.get_user_timeline(screen_name=username, count=500, max_id=last_id)
	user_timeline.extend(batch)
	last_id = user_timeline[-1]['id'] - 1

tweets = []
for tweet in user_timeline:
    tweets.append(tweet['text'])

tweets_string = ' '.join(tweets)
no_links = re.sub(r'http\S+', '', tweets_string)
result = re.sub(r"\\[a-z][a-z]?[0-9]+", '', no_links)
result = re.sub(r"[-()\"#/@;:<>{}+=~|_.!*?,]", '', result)
result = re.sub('[A-z]', '', result)
result = re.sub("\d+", '', result)

words = result.split(" ")
words = [word for word in words if len(word) > 2]

#In new version should not reverse persian words!
#words = [reshape(word) for word in words]

stopwords = []
res = True
with open('./stopwords') as f:
	while res:
		res = f.readline()
		stopwords.append(res.replace('\n', ''))

#Unused in new version of wordcloud!
#stopwords = [reshape(word) for word in stopwords]

mask = np.array(Image.open('./masks/mygraph.jpg'))


for font in fonts:
	font_name = font
	font_path = './fonts/%s.ttf' % font_name #nastaligh
	wc = WordCloud(background_color="white", max_words=500, mask=mask, stopwords=stopwords, font_path=font_path)#, persian_normalize=False)
	#wc = WordCloudFa(persian_normalize=True, background_color="white", max_words=500, mask=mask, stopwords=stopwords)

	clean_string = ','.join(words)
	wc.generate(clean_string)
	image = wc.to_image()
	image.save('./wordclouds/%s-%s.png' % (username, font_name))
	#image.show()
