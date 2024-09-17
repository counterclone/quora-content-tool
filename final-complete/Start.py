import streamlit as st
import twitterbot as tb
import pandas as pd
import time
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

st.set_page_config(page_title="Start", page_icon="^0^")

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

hashtag = [""]

st.title("quora sentiment analyis")


if "submit" not in st.session_state:
    st.session_state["submit"]=False

if "link" not in st.session_state:
    st.session_state["link"]=False

# st.session_state["link"]

def callback1():
    st.session_state["submit"]=True

def callback2(j):
    st.session_state[j]=not st.session_state[j]
    st.write("callback2 called")
    if st.session_state[j]:
        st.write(j)
        string_data = j
        df = pd.DataFrame({'text': [string_data]})
        df.to_csv('output.txt', sep='\t', index=False)



lst = st.text_input('Enter hashtags', "gun")
rate = st.number_input('Refresh Rate', 2)
links=[]

if ( st.button('Submit',on_click=callback1) 
    # or st.session_state["submit"]
    ):
    lst = [tag.strip() for tag in lst.split(" ")]
    hashtag.extend(lst)
    
    st.write("login started")
    bot = tb.Twitterbot()
    bot.login(0)
    st.write("login finished")
    
    st.write("fetching data")
    links = bot.get_tweets(hashtag, rate)
    df = pd.DataFrame({'links': links})
    st.write("fetching complete, select a link ")
    df.to_csv('links.csv', index=False)
    st.write("links file saved")
    links=list(set(links))
    st.write("switch to choose tab")
    # bot.close()

    