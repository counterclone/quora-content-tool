import streamlit as st
import twitterbot as tb
import pandas as pd
import time
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# st.set_page_config(page_title="Start", page_icon="^0^")

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

hashtag = [""]
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

def process(text):
    encoded_tweet = tokenizer(text,max_length=512, truncation=True, return_tensors='pt')
    return encoded_tweet


def sentiment(text):
    labels = ['Negative', 'Neutral', 'Positive']
    enct = process(text)
    output = model(**enct)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    dic = {}
    for i in range(len(scores)):
        dic[scores[i]] = labels[i]
    return dic[max(dic.keys())]
    
df = pd.read_csv('output.txt', sep='\t')
link = df['text'].iloc[0]
st.write("fetching data from selected link")
# call(link,2)
bot = tb.Twitterbot()
bot.login(0)
time.sleep(5)
tweets, usernames, pure_tweet = bot.get_comments(link,2)
# tweets, usernames, pure_tweet = bot.get_comments(link, rate)
df = pd.DataFrame({'username': usernames, 'tweet': tweets, 'pure_tweet': pure_tweet})
df.dropna(subset=['tweet'], inplace=True)
st.write("fetching complete")
df.to_csv('output_new.csv', index=False)
st.write("csv file saved")

st.write("started analysis")
words = pd.read_csv("Hate speech words - Sheet1.csv")
df = pd.read_csv("output_new.csv")
newdf = df.dropna()

newdf['type'] = newdf['tweet'].apply(lambda text: sentiment(text))

output_path = 'results.csv'
newdf.to_csv(output_path, index=False)

res = pd.read_csv("results.csv")
output_path = 'results.csv'
st.dataframe(newdf, width=2000, height=700)
res.to_csv(output_path, index=False)
st.write("completed")
st.write("switch to show tab")
