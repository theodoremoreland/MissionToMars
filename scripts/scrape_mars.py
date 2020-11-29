#!/usr/bin/env python
# coding: utf-8

# In[18]:


import io
import os
import time
import requests
import pymongo
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist


# In[19]:
def scrape():

    titles = []
    teasers = []
    tweets = []
    hemisphere_image_urls = []

    news_title = ""
    news_p = ""
    mars_weather = ""
    featured_image_url = ""


    # In[20]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[21]:


    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser.visit(url)

    html = browser.html

    soup = bs(html, 'html.parser')


    # In[22]:


    load = "y"

    while load == "y":

        if(browser.is_element_present_by_tag("ul", wait_time=5)):
            
            load = "n"

            results = soup.find_all('div', class_='list_text')

            for result in results:
                try:
                    title = result.find('a').text
                    titles.append(title)
                except ElementDoesNotExist:
                    print("Child tag <a> does not exist or does not have valid text.")

                try:
                    teaser = result.find("div", class_="article_teaser_body").text
                    teasers.append(teaser)
                except ElementDoesNotExist:
                    print("Child tag <div, class='article_teaser_body'> does not exist or does not have valid text.")
                    

        
        else:
            print("Parent Element <ul> Not Found. The webpage has either changed or hasn't completed loading.")
            load = input("Try again: y/n?").lower()[0]
            
    print(f"\n{titles[0]}:")
    print(f"\n{teasers[0]}")


    # In[23]:


    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    try:
        browser.visit(url)
    except:
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)

    html = browser.html

    soup = bs(html, 'html.parser')


    # In[24]:


    load = "y"

    while load == "y":

        if(browser.is_element_present_by_id("page", wait_time=5)):

            load ="n"
            
            try:
                browser.click_link_by_id('full_image')
                time.sleep(5)
            except:
                print("id: 'full_image' was not found.")

            try:
                browser.click_link_by_partial_text('more info')
                time.sleep(5)
            except:
                print("'more info' tab was not found.")

            try:
                browser.click_link_by_partial_href('//photojournal.jpl.nasa.gov/jpeg/')
                featured_image_url = browser.url
                print(f'Featured image url: {featured_image_url}')
            except:
                print("full_image.jpg was not found.")
        else:
            print("id: 'page' Not Found. The webpage has either changed or hasn't completed loading.")
            load = input("Try again: y/n?").lower()[0]


    # In[25]:


    url = "https://twitter.com/marswxreport?lang=en"
    time.sleep(5)


    try:
        browser.visit(url)
    except:
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)

    html = browser.html

    soup = bs(html, 'html.parser')


    # In[26]:


    load = "y"

    while load == "y":

        if(browser.is_element_present_by_tag("ol", wait_time=5)):
            
            load = "n"
            results = soup.find_all('div', class_='js-tweet-text-container')

            for result in results:
                try:
                    tweet = result.find('p').text
                    
                    if 'InSight sol' in tweet:
                        tweets.append(tweet.replace("hPa", "hPa "))
                        
                except ElementDoesNotExist:
                    print("Child tag <p> does not exist or does not have valid text.")

        else:
            print("Parent Element <ol> Not Found. The webpage has either changed or hasn't completed loading.")
            load = input("Try again: y/n?").lower()[0]

    ur1 = "https://thumbs.gfycat.com/ExcitableSeveralAlligator-small.gif"
    print(f"\n{tweets[0]}")


    # In[27]:


    url = "https://space-facts.com/mars/"
    time.sleep(5)


    try:
        browser.visit(url)
    except:
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)

    table = pd.read_html(url)


    # In[28]:


    string = io.StringIO()
    facts_df = pd.DataFrame({"Property": table[0][0], "Value": table[0][1]})
    facts = facts_df.set_index("Property").to_html(buf=string, classes='table table-striped')
    facts = string.getvalue()
    print(facts)


    # In[29]:


    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    time.sleep(5)


    try:
        browser.visit(url)
    except:
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)

    html = browser.html

    soup = bs(html, 'html.parser')


    # In[30]:


    load = "y"

    while load == "y":

        if(browser.is_element_present_by_tag("section", wait_time=5)):
            
            load = "n"
            
            results = soup.find_all('div', class_='item') 
            counter = -1

            for result in results:
                
                counter += 1
                
                try:
                    time.sleep(4)
                    names = soup.find_all('h3')
                    name = names[counter].get_text().rstrip("Enhanced")
                    print(name)
                    browser.find_by_tag("h3")[counter].click()
                    
                    time.sleep(5)
                except:
                    print("<h3> element was not found.")
                    
                    
                try:
                    
                    html2 = browser.html
                    soup2 = bs(html2, 'html.parser')
                    new_url = soup2.find("a", string="Sample").get('href')
                    browser.visit(new_url)
                    img_url = browser.url
                    print(img_url)
                    time.sleep(2)
                    browser.back()
                    time.sleep(2)
                    browser.back()
                    hemisphere_image_urls.append({"title": name, "img_url": img_url})
                except:
                    print("{a: text= 'Sample'} element was not found.")
                    break

            
        else:
            print("Parent Element <section> Not Found. The webpage has either changed or hasn't completed loading.")
            load = input("Try again: y/n?").lower()[0]
    browser.visit(ur1)


    # In[31]:


    news_title = titles[0]
    news_p = teasers[0]
    mars_weather = tweets[0]
    hemisphere_image_urls = hemisphere_image_urls
    featured_image_url = featured_image_url


    # In[32]:


    time.sleep(15)
    browser.quit()

    mars_data = {"news_title": news_title,
                "news_p": news_p,
                "mars_weather": mars_weather,
                "mars_facts": facts,
                "featured_image_url": featured_image_url,
                "hemisphere_image_urls": hemisphere_image_urls}

    return mars_data

from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

if __name__ == '__main__':
    app.run()