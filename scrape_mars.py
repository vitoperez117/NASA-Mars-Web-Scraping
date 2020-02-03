from selenium import webdriver
from bs4 import BeautifulSoup as bs

import requests
import time

mars_nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
mars_jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
mars_twitter_url= "https://twitter.com/marswxreport?lang=en"
mars_facts_url = "https://space-facts.com/mars/"
mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


def scrape_all():

    mars_db_entry = {}

    #Scrape NASA Mars News
    def scrape_mars_news():
        mars_news_entry = {}
        chrome_path = "/usr/local/bin/chromedriver"

        browser = webdriver.Chrome(chrome_path)
        browser.get(mars_nasa_url)

        time.sleep(1)

        soup = bs(browser.page_source, 'html.parser')
        
        mars_news_entry["mars_news_tag"] = soup.find('div', class_='content_title').text
        mars_news_entry["mars_news_body"] = soup.find('div', class_='article_teaser_body').text
        
        mars_db_entry['mars_news_entry'] = mars_news_entry

        browser.close()
        
    #Scrape JPL Featured Mars Image
    def scrape_jpl_mars_image():
        mars_jpl_img_entry = {}

        chrome_path = "/usr/local/bin/chromedriver"
        browser = webdriver.Chrome(chrome_path)

        browser.get(mars_jpl_url)

        time.sleep(1)

        soup = bs(browser.page_source, 'html.parser')
        img_title = soup.find('div', class_='item_tease_overlay').text
        img_url= soup.find('img', class_='thumb')['src']

        mars_jpl_img_entry['img_title'] = img_title
        mars_jpl_img_entry['img_url'] = "https://www.jpl.nasa.gov" + img_url

        mars_db_entry['mars_jpl_img_entry'] = mars_jpl_img_entry

        browser.close()

    #Scrape Twitter Mars Weather
    def scrape_mars_weather():
        
        response = requests.get(mars_twitter_url)
        soup = bs(response.content, 'html.parser')

        mars_db_entry['mars_weather'] =  soup.find('p', class_='TweetTextSize').text

    #Scrape Mars Facts table
    def scrape_mars_facts():

        chrome_path = "/usr/local/bin/chromedriver"
        browser = webdriver.Chrome(chrome_path)

        browser.get(mars_facts_url)

        time.sleep(1)
        soup = bs(browser.page_source, 'html.parser')
        mars_facts_html = str(soup.find('tbody')).encode(encoding='utf-8', errors='ignore')

        mars_db_entry['mars_facts_html'] = mars_facts_html

        browser.close()

    #Scrape Mars Hemisphere Images
    def scrape_mars_hemisphere():
        mars_hemispheres_entry = {}

        chrome_path = "/usr/local/bin/chromedriver"
        browser = webdriver.Chrome(chrome_path)

        browser.get(mars_hemispheres_url)

        soup = bs(browser.page_source, 'html.parser')
        link_names = soup.find_all('h3')
        for index, data in enumerate(link_names):
            link = browser.find_element_by_link_text(str(data.text))
            link.click()
            time.sleep(1)
            
            title = browser.find_element_by_class_name("title")
            image_title = title.text

            image = browser.find_element_by_xpath("//a[@target='_blank']")

            mars_hemispheres_entry[f"hemisphere_name_{index}"] = image_title 
            mars_hemispheres_entry[f"hemisphere_url_{index}"] = image.get_attribute('href')
            
            browser.back()

        time.sleep(1)

        mars_db_entry['mars_hemispheres_entry'] = mars_hemispheres_entry

        browser.close()

    scrape_mars_news()
    scrape_jpl_mars_image()
    scrape_mars_weather()
    scrape_mars_facts()
    scrape_mars_hemisphere()

    print(mars_db_entry)

    return mars_db_entry