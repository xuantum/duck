# Step02 needs "tokenized_text.pkl" and "cnt.pkl" generated in Step01.
# Step02 creates a "Top tweeted stocks" message and a wordcloud image and tweets them.
print('==============================================')
print('            Step02 Started')
print('==============================================')
# Change directory
#import os
#os.chdir(os.path.dirname(os.path.abspath(__file__)))
from matplotlib.pyplot import figure, axes, imshow, axis, savefig
from pandas import read_pickle
from time import sleep
from wordcloud import WordCloud, STOPWORDS
import tweet_func
from config import keys

# Load the objects generated in step01
tokenized_text = read_pickle('tokenized_text.pkl')
cnt = read_pickle('cnt.pkl')

# Create message(top ranking)
tweet = 'Top tweeted stocks:\n'
for i_tuple in cnt:
        tweet = tweet + i_tuple[0]
        if len(tweet) > 250:
            tweet = tweet + '\n\n #stockstowatch'
            break
print(tweet)
print('----------------------------------------------')
print('word count =', len(tweet))
print('==============================================')

# Generate wordcloud image
wc = WordCloud(width = 1280, height = 720, random_state=1, background_color='black', colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(tokenized_text)
# Save png image
#today = date.today()
#file_path = './images/WordCloud' + str(today) + '.png'
file_path = './images/WordCloud.png'
fig = figure(figsize=(8,4.5), dpi=160)
ax = axes([0,0,1,1])
imshow(wc, interpolation="nearest", aspect="equal")
axis('off')
savefig(file_path, dpi=160)
#show()
print('WordCloud Completed!')
sleep(2)

# Tweet with a image
tweet_func.tweet_msg(keys, tweet, file_path)
print('==============================================')
print('            Step02 Completed!')
print('==============================================')
