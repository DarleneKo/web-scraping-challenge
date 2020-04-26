# # MISSION TO MARS:  (Part 2: MongoDB and Flask Application)

# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd
import time

# Initialize Browser for Windows Users
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    time.sleep(3)
    return browser

# Create Scrape Function
def scrape():
    browser = init_browser()
    
    ###################################################################################################################
    # NASA MARS NEWS SECTION:
    ###################################################################################################################
    
    # create mars_data dictionary that we can insert into mongo
    mars_data = {}
    
    # Visit the url for Mars News using Splinter
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(3)
    
    # Create BeautifulSoup object; parse with 'html'
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'html.parser')
    
    
    # Examine the results, then determine element that contains sought info (Latest News Title)
    list_text = news_soup.find('div', class_='list_text')
    news_title = list_text.find('div', class_='content_title').find('a').text
    #print(news_title)  

    # Place Scraped Data into Dictionary
    mars_data["News_Title"] = news_title
    
    # Examine the results, then determine element that contains sought info (Latest News Paragraph)
    news_p = list_text.find('div', class_='article_teaser_body').text
    #print(news_p)
    
    # Place Scraped Data into Dictionary
    mars_data["News_Paragraph"] = news_p
    
    ###################################################################################################################
    # JPL MARS SPACE IMAGES - FEATURED IMAGE SECTION:
    ###################################################################################################################
    
    # Visit the url for JPL Featured Space Image using Splinter
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    time.sleep(3)

    # Find and Click the Full Image Button on the Website
    button = browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(3)
    
    # Create BeautifulSoup object; parse with 'html'
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, 'html.parser')
    
    # Examine the results, then determine Parent Element that contains sought info (Latest Full Image after Clicking Button)
    full_image = image_soup.find('img', class_='fancybox-image')
    #print(full_image)
    
    # Extract the inner attribute
    full_image_url = full_image.attrs['src']
    #full_image_url
    
    # Combine main url page with the full image url for the featured image url
    main_jpl_url = "https://www.jpl.nasa.gov"
    featured_image_url = f'{main_jpl_url}{full_image_url}'
    #print(featured_image_url)
    
    # Place Scraped Data into Dictionary
    mars_data["Featured_Image"] = featured_image_url
    
    
    ###################################################################################################################
    # MARS WEATHER SECTION:
    ###################################################################################################################
    
    # Visit the url for the Mars Weather Twitter Account using Splinter
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(3)
    
    # Create BeautifulSoup object; parse with 'html'
    weather_html = browser.html
    weather_soup = BeautifulSoup(weather_html, 'html.parser')
    
    # Examine the results, then determine Parent Element that contains sought info (Latest Tweet)
    weather_timeline = weather_soup.find('div', attrs={"aria-label": "Timeline: Mars Weather’s Tweets"})
    #print(weather_timeline)
    
    # Examine the results, then determine 1st Child Element that contains sought info (Latest Tweet)
    latest_tweet = weather_timeline.find('div',
                                         attrs={'lang': 'en',
                                                'dir': 'auto',
                                                'class': 'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'})
    # Print the scraped information
    #print(latest_tweet)               
    
    # Examine the results, then determine 2nd Child Element that contains sought info (Latest Tweet)
    mars_weather = latest_tweet.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text
    #print(mars_weather)
    
    # Place Scraped Data into Dictionary
    mars_data["Mars_Weather"] = mars_weather
    
    
    ###################################################################################################################
    # MARS FACTS SECTION:
    ###################################################################################################################
    
    # We can use the read_html function in Pandas to automatically scrape any tabular data from a page.
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    #tables

    # What we get in return is a list of dataframes for any tabular data that Pandas found.
    type(tables)
    
    # We can slice off any of those dataframes that we want using normal indexing.
    df = tables[0]
    #df
    
    # Assign the columns `['Description', 'Value']`
    df.columns = ['Description','Value']
    #df
    
    # Set the index to the `Description` column without row indexing
    df.set_index('Description', inplace=True)
    #df
    
    # Save the table as HTML string
    html_string = df.to_html()
    #df.to_html()
    
    # Place Scraped Data into Dictionary
    mars_data["Mars_Facts"] = html_string
    
    ###################################################################################################################
    # MARS HEMISPHERES SECTION:
    ###################################################################################################################
    
    # Visit the url for the USGS Astrogeology site using Splinter
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    time.sleep(3)
    
    # Create BeautifulSoup object; parse with 'html'
    all_hemispheres_html = browser.html
    all_hemispheres_soup = BeautifulSoup(all_hemispheres_html, 'html.parser')
    
    # Examine the results, then determine element that contains sought info (All Hemispheres)
    all_hemispheres = all_hemispheres_soup.find_all('div', class_='item')
    #print(all_hemispheres)
    
    # Store the main_url
    all_hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Create empty list for All Hemisphere urls
    all_hemispheres_image_url = []
    
    # Loop through data for All Hemispheres
    for x in all_hemispheres:
    
        # Store Title for each Hemisphere
        title = x.find('h3').text
    
        # Store url for each Hemisphere
        individual_hemisphere_url = x.find('a', class_='itemLink product-item')['href']
    
        # Visit the link that contains the full image
        browser.visit(all_hemispheres_main_url + individual_hemisphere_url)
        time.sleep(3)
    
        # HTML Object of individual hemisphere
        individual_hemisphere_html = browser.html
    
        # Parse HTML with Beautiful Soup for each individual hemisphere
        individual_hemisphere_soup = BeautifulSoup(individual_hemisphere_html, 'html.parser')
    
        # Retrieve full image source 
        img_url = all_hemispheres_main_url + individual_hemisphere_soup.find('img', class_='wide-image')['src']
    
        # Append the retreived information into a list of dictionaries 
        all_hemispheres_image_url.append({"title" : title, "img_url" : img_url})
    
        # Display hemisphere_image_urls
        #all_hemispheres_image_url
        
    # Place Scraped Data into Dictionary
    mars_data["Mars_Hemispheres"] = all_hemispheres_image_url
    
    # End the session and return all the keys and values from Mars Data Dictionary
    browser.quit()
    return mars_data

# Test if Scrape Function works properly
if __name__ == "__main__":
    print("\nTesting Data Retrieval...\n")
    print(scrape())
    print("\nProcess Complete!\n")

