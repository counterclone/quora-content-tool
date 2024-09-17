from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time, os
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def remove_non_ascii(input_string):
    return ''.join(char if ord(char) < 128 else '' for char in input_string)

def remove_extra_spaces(text):
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text

def keep_alphabets_and_spaces(input_string):
    cleaned_string = re.sub(r'[^a-zA-Z\s]', '', input_string)
    return cleaned_string

def remove_duplicates(input_list):
    seen = set()
    result = []
    for item in input_list:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result



cred =pd.read_csv("cred.csv")
k=0

def listToString(s):
    str1 = " "
    return (str1.join(map(str, s)))

class Twitterbot:
    
    def __init__(self):
       
        print("login")
        self.k=0
        edge_options = Options()  # Use EdgeOptions instead of ChromeOptions
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
        
        edge_options.add_argument(f'user-agent={user_agent}')
        #edge_options.add_argument("--headless=new")
        
        self.bot = webdriver.Edge( options=edge_options)  # Specify the path to msedgedriver
        
        

        

    def login(self,k):
        bot=self.bot
        self.email =cred['username'][k]
        self.password= cred['password'][k]
        print("login started")
        #bot.get('https://twitter.com/i/flow/login?input_flow_data=%7B"requested_variant"%3A"eyJsYW5nIjoiZW4ifQ%3D%3D"%7D')
        #bot.get('https://twitter.com/i/flow/login')
        bot.get('https://www.quora.com')
        # time.sleep(1)
        # page_source = bot.page_source
        # soup = BeautifulSoup(page_source,'html.parser')
        # signin=bot.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[5]/a/div')
        # signin.click()
        # print("signin clicked")
        # time.sleep(4)
        page_source = bot.page_source
        soup = BeautifulSoup(page_source,'html.parser')
        email=bot.find_element(By.NAME,'email')
        email.send_keys(self.email)
       
        #time.sleep(2)
        password = bot.find_element(By.NAME,'password')
        #password = bot.find_element(By.CSS_SELECTOR,'#react-root > div > div > div > main > div > div > div > div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox > div.css-175oi2r.r-16y2uox.r-1jgb5lz.r-13qz1uu.r-1ye8kvj > div.css-175oi2r.r-1fq43b1.r-16y2uox.r-1wbh5a2.r-1dqxon3 > div > div > div > div.css-175oi2r.r-mk0yit.r-13qz1uu > div > label > div > div.css-175oi2r.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1wzrnnt.r-1udh08x.r-xd6kpl.r-1pn2ns4.r-ttdzmv')
        password.send_keys(self.password)
        time.sleep(7)
        
        button=bot.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[4]/button')
        button.click()
        
        print("login finished")

    def get_tweets(self, hashtag_list,l): 
        
        bot=self.bot
        
        num=0
        i=0
        links=[]
        while i<len(hashtag_list):
            t=l
            p=0
            hashtag=hashtag_list[i]
            print(hashtag)

                    #https://twitter.com/search?q=hello&src=typed_query
            bot.get('https://www.quora.com/search?q=' + hashtag )
            time.sleep(3)
            if(hashtag==""):
                i+=1
                continue
            
            while(t>0):
                page_source = bot.page_source
                soup = BeautifulSoup(page_source,'lxml')
                t-=1
               
                a=soup.find_all('div',{'class':'q-box qu-borderBottom qu-p--medium'})
                print("number of links ", len(a))
                for b in a:
                    link=b.find('a',{'class':'q-box Link___StyledBox-t2xg9c-0 gOCLNQ puppeteer_test_link qu-display--block qu-cursor--pointer qu-hover--textDecoration--underline'})
                    print(link['href'])
                    links.append(link['href'])
                    p+=1
                
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(5)
            print(f"number of tweets fetched by {hashtag} = {p}")
            if(p==0):
                self.k+=1
                cv=self.k
                i-=1
                self.login(cv)
                continue
            i+=1
            num+=p
            time.sleep(1)
        
        print(f"total tweets fetched {num} ")
        return links
    
    def get_comments(self,link,r):
        bot=self.bot
        r=1
        tweets=[]
        pure_tweets=[]
        username=[]
        div_counter=0
        
        bot.get(link)
        time.sleep(7)
        while r>0:
            r-=1
            page_source = bot.page_source
            soup = BeautifulSoup(page_source,'html.parser')
            tp=soup.find('div',{'id':'mainContent'})
            with open('output.txt', 'w') as file:
                file.write(tp.prettify())
            df.to_csv('data.txt', sep='\t', index=False)
            divs_out1 = tp.find('div',{'class':'q-box qu-borderAll qu-borderRadius--small qu-borderColor--raised qu-boxShadow--small qu-bg--raised'})
            divs_out=divs_out1.find_next_sibling('div').find_next_sibling()
        #     # with open('output.html', 'w',encoding='utf-8') as file:
        #     #     file.write(divs_out.prettify())
            
            
        #     # divs_out.find_all('div',{'class':'q-box'})
        #     divs_in = []
        #     while True:  # Loop from 0 to 9
        #         class_name = 'q-box dom_annotate_question_answer_item_' + str(div_counter) + ' qu-borderAll qu-borderRadius--small qu-borderColor--raised qu-boxShadow--small qu-mb--small qu-bg--raised'
        #         element = divs_out.find('div', {'class': class_name})
        #         div_counter+=1
        #         if element:  # If element is found, add it to the list
        #             divs_in.append(element)
        #         else:  # If element is not found, break out of the loop
        #             break
        #     # with open('test.html', 'w',encoding='utf-8') as file:
        #     #     file.write(divs_in[0].prettify())
        #     print("divs_in",len(divs_in))

        #     for i in divs_in:
        #         a=i.find('div',{'class':'q-click-wrapper qu-display--block qu-tapHighlight--none qu-cursor--pointer ClickWrapper___StyledClickWrapperBox-zoqi4f-0 daLTSH'})
        #         user_div2=a.find('div',{'class':'q-relative'}).find('div',{'class':'q-flex'})
        #         # .find('div',{'class':'q-flex qu-alignItems--flex-start'})
        #         user_div1=user_div2.find('div',{'class':'q-box qu-flex--auto'})
        #         if(user_div1 is None):
        #             user_div1=user_div2.find('div',{'class':'q-box qu-flex--auto qu-alignSelf--center'})
        #         user_div=user_div1.find('div',{'class':'q-box'})
        #         content_div=i.find('div',{'class':'q-box spacing_log_answer_content puppeteer_test_answer_content'})
        #         user_span=user_div.find('span',{'class':'q-box'})
        #         a_user=user_span.find('a',{'class':'q-box Link___StyledBox-t2xg9c-0 gOCLNQ puppeteer_test_link qu-color--gray_dark qu-cursor--pointer qu-hover--textDecoration--underline'})

        #         user=a_user.find('span',attrs=lambda x: x is None or len(x) == 0).find('span').text
        #         cont=content_div.find_all('span')
        #         content=""
        #         for j in cont:
        #             content=content+j.text
        #         print(user+" "+content)
        #         print("---------------------------------------")
        #         username.append(user.encode('utf-8'))
        #         tweets.append(keep_alphabets_and_spaces(remove_extra_spaces(remove_non_ascii(content))))
        #         pure_tweets.append(content.encode('utf-8'))
        #     bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        #     time.sleep(7)
        # return tweets,username,pure_tweets
        




       

     

        



            
