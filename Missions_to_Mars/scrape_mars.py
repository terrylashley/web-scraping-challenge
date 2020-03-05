#import dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests


#Set up the browser
def browser_setup():
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
#Make an empty dictionary to import to mongodb
mars_data = {}

#Nasa Mars News
def scrape_mars_news():
    try:
        
        #initiate the browser
        browser = browser_setup()
        
        #Visit the Nasa Web Page with Splinter
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        
        #Create a HTML object to parse with Beautiful Soup
        html = browser.html

        #Parse HTML Object with Beautiful Soup
        soup = bs(html, 'html.parser')
        
        #Retrieve the latest News Title and News Paragraph data
        #Inspect web page for root path to information use soup.find to pull the data

        news_title = soup.find('div', class_ ='list_text').find('a').text

        news_paragraph = soup.find('div', class_='article_teaser_body').text
        
        #Place the News data into a dictionary
        mars_data['news_title'] = news_title
        mars_data['news_paragraph'] = news_paragraph
        
        return mars_data
    
    finally:
        
        browser.quit()
        
#JPL Mars Space Images
def scrape_images():
    try:
        
        #initiate the browser
        browser = browser_setup()
        
        #Use splinter to find the url for the current featured image
        mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(mars_image_url)
        
        #create an HTML object to parse with Beautiful Soup
        html_image = browser.html

        #parse HTML with Beautiful Soup
        soup = bs(html_image, 'html.parser')
        
        #grab the background image url
        featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        #connect the main url for the website to the background image url
        #base url
        main_url = 'https://www.jpl.nasa.gov'

        #join base url and background url
        featured_image_url = main_url + featured_image_url
        
        #Full link for image
        featured_image_url
        
        #add to the dictionary
        mars_data['featured_image_url'] = featured_image_url
        
        return mars_data
    finally:
        
        browser.quit()
        
        