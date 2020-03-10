#import dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests

#Set up the browser
def browser_setup():
    # @NOTE: Replace the path with your actual path to the chromedriver NOT DONE YET
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    
    #Make an empty dictionary to import to mongodb
    mars_data = {} 
    
    #initiate the browser
    browser = browser_setup()
    
    
    #MARS NEWS
    #Visit the Nasa Web Page with Splinter
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # Create a HTML object to parse with Beautiful Soup
    html = browser.html

    #Parse HTML Object with Beautiful Soup
    soup = bs(html, 'html.parser')
    
    #Retrieve the latest News Title and News Paragraph data
    #Inspect web page for root path to information use soup.find to pull the data
    
    #Place the News data into a dictionary
    mars_data['news_title'] = soup.find('div', class_ ='list_text').find('a').text
    mars_data['news_paragraph'] = soup.find('div', class_='article_teaser_body').text
        
        
        
        
    #MARS IMAGE
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
    #featured_image_url

    #add to the dictionary
    mars_data['featured_image_url'] = featured_image_url
         
         
         
    #MARS TWEET
    #Grab the latest weather report tweet from the mars twitter account
    twitter_weather_url= 'https://twitter.com/MarsWxReport/status/1235261528946937856' 
    browser.visit(twitter_weather_url)
    
    #create an HTML object to parse with Beautiful Soup
    html_twitter_weather= browser.html

    #parse object with Beautiful Soup
    soup = bs(html_twitter_weather, 'html.parser')
    
    #Grab the latest weather tweet
    latest_weather_tweet = soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-1blvdjr r-16dba41 r-ad9z0x r-bcqeeo r-19yat4t r-bnwqim r-qvutc0').text
    
    #Add the weather tweet to the dictionary
    mars_data['latest_weather_tweet'] = latest_weather_tweet
    
    
    
    
    #MARS FACTS
    #place URL in variable to be called by pandas
    mars_facts_url = 'https://space-facts.com/mars/'

    #Use pandas to parse the URL
    mars_facts = pd.read_html(mars_facts_url)
    
    #Index into the correct dataframe
    mars_facts_df = mars_facts[0]
    
    #Change titles 
    mars_facts_df.columns = ['Perameter', 'Facts']
    
    #prep for HTML page
    mars_facts_df.set_index('Perameter', inplace=True)
    
    #Save to HTML
    mars_facts_df.to_html("mars_facts_df.html")
    
    mars_facts = mars_facts_df.to_html()
    
    #Add mars facts to the dictionary
    mars_data['mars_facts'] = mars_facts
    
    
    #MARS HEMISPHERES
    #Grab high resolution images for each Mars Hemisphere
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    #create HTML object to be parsed
    hemispheres_html = browser.html

    #parse HTML with Beautiful Soup
    soup = bs(hemispheres_html, 'html.parser')
    
    #Grab the items that has the hemispheres information
    items = soup.find_all('div', class_='item')

    #Hemisphere URL list
    hemisphere_pic_urls = []

    #Plase main url in variable to combine later
    hemisphere_url = 'https://astrogeology.usgs.gov'
    
    #create a loop  to grab each link and create a dictoinary 
    for i in items:
        #grab the title
        title = i.find('h3').text

        #website link for images
        img_url = i.find('a', class_='itemLink product-item')['href']

        #Visit the link that contains the full image using browser
        browser.visit(hemisphere_url + img_url)

        #make html object of hemisphere
        img_html = browser.html

        #use beautiful soup to parse each hemisphere
        soup = bs(img_html, 'html.parser')

        #grab the full image data
        img_url = hemisphere_url + soup.find('img', class_='wide-image')['src']

        hemisphere_pic_urls.append({'title':title, 'img_url':img_url})
    
    #add to dictionary
    mars_data['hemisphere_pic_urls'] = hemisphere_pic_urls
        
        
        
        
        
        
        
        
    return mars_data
    

  

# #Nasa Mars News
# def scrape_mars_news():
#     try:
#         #Make an empty dictionary to import to mongodb
#         mars_data = {} 
        
#         #initiate the browser
#         browser = browser_setup()
        
#         #Visit the Nasa Web Page with Splinter
#         url = 'https://mars.nasa.gov/news/'
#         browser.visit(url)
        
#         # Create a HTML object to parse with Beautiful Soup
#         html = browser.html

#         #Parse HTML Object with Beautiful Soup
#         soup = bs(html, 'html.parser')
        
#         #Retrieve the latest News Title and News Paragraph data
#         #Inspect web page for root path to information use soup.find to pull the data
        
#         #Place the News data into a dictionary
#         mars_data['news_title'] = soup.find('div', class_ ='list_text').find('a').text
#         mars_data['news_paragraph'] = soup.find('div', class_='article_teaser_body').text
        
        
#         return mars_data
    
#     finally:
        
#         browser.quit()
# print(scrape_mars_news())

        
#  #JPL Mars Space Images
# def scrape_images():
#      try:
        
#          #initiate the browser
#          browser = browser_setup()
        
#          #Use splinter to find the url for the current featured image
#          mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#          browser.visit(mars_image_url)
        
#          #create an HTML object to parse with Beautiful Soup
#          html_image = browser.html

#          #parse HTML with Beautiful Soup
#          soup = bs(html_image, 'html.parser')
        
#          #grab the background image url
#          featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

#          #connect the main url for the website to the background image url
#          #base url
#          main_url = 'https://www.jpl.nasa.gov'

#         #join base url and background url
#          featured_image_url = main_url + featured_image_url
        
#          #Full link for image
#          featured_image_url
        
#          #add to the dictionary
#          mars_data['featured_image_url'] = featured_image_url
        
         
        #  return mars_data
  
        
#          browser.quit()
# print(scrape_images())         
         
        
# #Mars Weather
# def scrape_mars_weather():
#     try:
        
#         #initiate the browser
#         browser = browser_setup()
        
#         #Grab the latest weather report tweet from the mars twitter account
#         twitter_weather_url= 'https://twitter.com/MarsWxReport/status/1235261528946937856' 
#         browser.visit(twitter_weather_url)
        
#         #create an HTML object to parse with Beautiful Soup
#         html_twitter_weather= browser.html

#         #parse object with Beautiful Soup
#         soup = bs(html_twitter_weather, 'html.parser')
        
#         #Grab the latest weather tweet
#         latest_weather_tweet = soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-1blvdjr r-16dba41 r-ad9z0x r-bcqeeo r-19yat4t r-bnwqim r-qvutc0').text
        
#         #Add the weather tweet to the dictionary
#         mars_data['latest_weather_tweet'] = latest_weather_tweet
        
#         return mars_data
#     finally:
        
#         browser.quit()
        

# #Mars Facts
# #Scrape table containing facts about planet mars using pandas
# def scrape_mars_facts():
    
    
#         #place URL in variable to be called by pandas
#         mars_facts_url = 'https://space-facts.com/mars/'

#         #Use pandas to parse the URL
#         mars_facts = pd.read_html(mars_facts_url)
        
#         #Index into the correct dataframe
#         mars_facts_df = mars_facts[0]
        
#         #Change titles 
#         mars_facts_df.columns = ['Perameter', 'Facts']
        
#         #prep for HTML page
#         mars_facts_df.set_index('Perameter', inplace=True)
        
#         #Save to HTML
#         mars_facts_df.to_html("mars_facts_df.html")
        
#         mars_facts = mars_facts_df.to_html()
        
#         #Add mars facts to the dictionary
#         mars_data['mars_facts'] = mars_facts
        
#         return mars_data
    
    
# #Mars Hemispheres
# def scrape_mars_hemispheres():
#     try:
        
#         #initiate the browser
#         browser = browser_setup()
        
#         #Grab high resolution images for each Mars Hemisphere
#         hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#         browser.visit(hemispheres_url)

#         #create HTML object to be parsed
#         hemispheres_html = browser.html

#         #parse HTML with Beautiful Soup
#         soup = bs(hemispheres_html, 'html.parser')
        
#         #Grab the items that has the hemispheres information
#         items = soup.find_all('div', class_='item')

#         #Hemisphere URL list
#         hemisphere_pic_urls = []

#         #Plase main url in variable to combine later
#         hemisphere_url = 'https://astrogeology.usgs.gov'
        
#         #create a loop  to grab each link and create a dictoinary 
#         for i in items:
#             #grab the title
#             title = i.find('h3').text

#             #website link for images
#             img_url = i.find('a', class_='itemLink product-item')['href']

#             #Visit the link that contains the full image using browser
#             browser.visit(hemisphere_url + img_url)

#             #make html object of hemisphere
#             img_html = browser.html

#             #use beautiful soup to parse each hemisphere
#             soup = bs(img_html, 'html.parser')

#             #grab the full image data
#             img_url = hemisphere_url + soup.find('img', class_='wide-image')['src']

#             hemisphere_pic_urls.append({'title':title, 'img_url':img_url})
        
#         #add to dictionary
#         mars_data['hemisphere_pic_urls'] = hemisphere_pic_urls
        
#          return mars_data
#      finally:
        
#         browser.quit()
        
      



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        