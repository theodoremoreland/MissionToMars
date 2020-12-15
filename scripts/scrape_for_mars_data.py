# Native
import io
import os
import re
import time

# Third party
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist


def init_browser_bot(url, preload=False):
    """Each time init_browser_bot runs, it'll reference the variables from the previous init.
    Functions that reference the browser, html, or soup variables without assignments will default
    to the init_broswer_bot's variables, otherwise said variables are limited to local scope and therefore
    require global keyword declarations.
    """
    
    global browser, executable_path, html, soup
    
    try:
        browser.visit(url)
    except:
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=True)
        browser.driver.set_window_size(1280, 720)
        browser.visit(url)
       
    if preload:
        time.sleep(1)
        for _ in range(3):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
    html = browser.html
    soup = bs(html, 'html.parser')


def scrape_mars_NASA_articles():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    init_browser_bot(url, True)
    
    articles = []
    pageHasLoaded = False

    while not pageHasLoaded:
        if(browser.is_element_present_by_css("div.list_text", wait_time=5_000)):
            pageHasLoaded = True
            results = soup.find_all('div', class_='list_text')

            for result in results:
                title = result.find('a').text
                teaser = result.find("div", class_="article_teaser_body").text
                articles.append({"title": title, "teaser": teaser})
                
    return articles


def scrape_mars_NASA_featured_image():
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    init_browser_bot(url)
    
    featured_image_url = ""
    pageHasLoaded = False

    while not pageHasLoaded:
        if(browser.is_element_present_by_id("page", wait_time=5)):
            pageHasLoaded = True
            browser.click_link_by_id('full_image')
            browser.click_link_by_partial_text('more info')
            browser.click_link_by_partial_href('//photojournal.jpl.nasa.gov/jpeg/')
            featured_image_url = browser.url
            # print(f'Featured image url: {featured_image_url}')
            
    return featured_image_url


def scrape_mars_weather_tweets():
    url = "https://twitter.com/marswxreport?lang=en"
    init_browser_bot(url, True)
    
    tweets = []
    pageHasLoaded = False

    while not pageHasLoaded:
        if(browser.is_element_present_by_css('div[data-testid="tweet"]', wait_time=5)):
            pageHasLoaded = True
            results = re.findall(r'InSight sol.*?<', html, re.DOTALL)
            
            for result in results:
                    tweet = result
                    if 'InSight sol' in tweet:
                        tweets.append(tweet[:-1].replace("hPa", "hPa "))

    return tweets


def scrape_mars_space_facts_html_table():
    stringBuffer = io.StringIO()
    url = "https://space-facts.com/mars/"
    space_facts_html = pd.read_html(url)
    
    facts_df = pd.DataFrame({"Property": space_facts_html[0][0], "Value": space_facts_html[0][1]})
    facts_df.set_index("Property").to_html(buf=stringBuffer, classes='table table-striped')
    
    facts_html_table = stringBuffer.getvalue()
    
    return facts_html_table


def scrape_mars_hemisphere_image_urls():
    global browser, html, soup
    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    init_browser_bot(url)
    
    hemisphere_image_urls = []
    pageHasLoaded = False

    while not pageHasLoaded:
        if(browser.is_element_present_by_tag("section", wait_time=5)):
            pageHasLoaded = True
            results = soup.find_all('div', class_='item') 
            counter = 0

            for result in results:
                names = soup.find_all('h3')
                name = names[counter].get_text().rstrip("Enhanced")

                browser.find_by_tag("h3")[counter].click()
                html = browser.html
                soup = bs(html, 'html.parser')
                
                new_url = soup.find("a", string="Sample").get('href')
                browser.visit(new_url)
                img_url = browser.url
                
                hemisphere_image_urls.append({"title": name, "img_url": img_url})

                browser.back()
                browser.back()
                html = browser.html
                soup = bs(html, 'html.parser')
                counter += 1
    return hemisphere_image_urls