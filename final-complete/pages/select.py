import streamlit as st
import pandas as pd

def callback2(j):
    # st.session_state[j]=not st.session_state[j]
    # st.write("callback2 called")
    # if st.session_state[j]:
    st.write(j)
    string_data = j
    df = pd.DataFrame({'text': [string_data]})
    df.to_csv('output.txt', sep='\t', index=False)
    st.write("button selected move to fetch")

df=pd.read_csv("links.csv")
links = df["links"]
links =list(set(links))
for i in links:
    if(st.button(i,key=i)):
        callback2(i)
