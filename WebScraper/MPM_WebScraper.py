#!/usr/bin/env python3

## Retrieves all articles in the Momentum Product Manual (https://accure.ai/docs/)
## and stores them in a plain text and JSON file with respective formats.


#-------------- SETUP --------------
# Import required libraries
import requests
import json
import time
import os
from bs4 import BeautifulSoup


# Set environment variables & settings (edit these to fit environment)
#Accure Account Cookie - Find and paste key value pair for cookie created when logged into Acccure website
#                        (e.g. 'wordpress_logged_in_...': '<username>...')
acct_cookies = {
    '': '',
}
#Output Files
output_file_name   = "MPM"
output_file_root   = ".."
output_file_folder = os.path.join("Data", "Scraping")

# Set other variables
output_file_path = os.path.join(output_file_root, output_file_folder, output_file_name)

# Create an ordered tuple corresponding to all the Momentum products (categories) in the manual
products = ('Momentum', 'MLOps', 'Impulse EDW', 'Inset BI', 'APIs')

# Create variables to hold the contents of all articles in text and JSON forms
article_texts = []
article_jsons = []


#-------------- FUNCTIONS --------------
# Create a function that retrieves the contents of articles and stores them in the list variables
def store_article_contents(url, prod_num, section_title, section_num, article_num):
    # Grab the contents of the current Momentum Product Manual article
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the article's title and body from the page contents
    article_title = soup.find('h1', {'class': 'eckb-article-title'}).text
    article_body = soup.find('div', {'id': 'eckb-article-content-body'}).get_text()
    
    # Combine the title and body to form the page's text and store it in the texts list
    article_texts.append(" \n".join((article_title,article_body)))
    
    # Create a dictionary with all the mapped values and store it in the JSONs list 
    article_jsons.append({"URL"          : url,
                          "Product_Title": products[prod_num],
                          "Section_Title": section_title,
                          "Section_Num"  : section_num,
                          "Article_Title": article_title,
                          "Article_Num"  : article_num,
                          "Article_Body" : article_body})


#-------------- MAIN --------------
# Grab the contents of the Momentum Product Manual index page
docs_url = 'https://accure.ai/docs/'
response = requests.get(docs_url, cookies=acct_cookies)

# Extract the URLs for all articles in the index, keeping track of section and article numbers
soup = BeautifulSoup(response.content, 'html.parser')
prod_num = -1
for category in soup.find('div', {'class':'epkb-panel-container'}).find_all('div', recursive=False):
    prod_num += 1
    sec_num = 0
    for section in category.find_all('section', recursive=False):
        sec_num += 1
        art_num = 0
        sec_title = section.find('h3', {'class':'epkb-cat-name'}).text
        for url in [url['href'] for url in section.find_all('a',{'class':'epkb-mp-article'})]:
            art_num += 1
            time.sleep(1)
            store_article_contents(url, prod_num, sec_title, sec_num, art_num)


# Create a new plaintext file and write the product manual text to it
f = open(f"{output_file_path}.txt", "w", encoding="utf-8")
f.write('\n\n'.join(article_texts))
f.close()

# Create a new JSON file and write the product manual JSON objects to it
f = open(f"{output_file_path}.json", "w", encoding="utf-8")
f.write(json.dumps(article_jsons, indent=4))
f.close()
