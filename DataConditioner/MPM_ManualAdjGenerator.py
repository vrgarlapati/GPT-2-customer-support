#!/usr/bin/env python3

## Generates a template manual adjustment JSON file based on the contents of the Momentum Product Manual JSON


#-------------- SETUP --------------
# Import required libraries
import os
import json


# Set environment variables & settings (edit these to fit environment)
#Input File
input_file_name    = 'MPM.json'
input_file_root    = ".."
input_file_folder  = os.path.join("Data", "Scraping")
#Output File
output_file_name   = 'MPM_manual_adj_template.json'
output_file_root   = ".."
output_file_folder = os.path.join("Data", "Conditioning")
#List of article numberings to copy the article bodies for from the original MPM source file 
#(format: Product_Num.Section_Num.Article_Num)
articles_to_copy   = ['1.1.3', '1.2.1', '1.2.2', '1.2.3', '1.2.4', '1.2.6', '1.2.7', '1.2.8', '1.3.3', '1.3.4', '1.3.5', 
                      '1.3.6', '1.4.1', '1.4.2', '1.4.3', '2.1.1', '2.1.3', '2.1.4', '2.2.1', '2.2.2', '2.2.3', '2.3.4', 
                      '2.2.5', '2.2.6', '2.2.7', '2.3.1', '2.3.2', '2.3.3', '2.4.1', '2.4.4', '3.2.1', '3.2.2', '3.2.3', 
                      '3.3.1', '3.3.5', '3.3.6', '3.3.7', '3.3.8', '3.3.9', '3.3.10', '3.3.11', '3.3.12', '3.3.13', 
                      '3.4.1', '3.4.2', '3.5.1', '3.5.2', '3.5.3', '3.5.4', '3.5.5', '3.5.6', '3.5.7', '3.5.8', '3.5.9', 
                      '3.6.1', '3.6.2', '3.7.1', '3.7.2', '3.8.1', '4.1.1', '4.2.1', '4.3.1']

# Set other variables
input_file_path    = os.path.join(input_file_root, input_file_folder, input_file_name)
output_file_path   = os.path.join(output_file_root, output_file_folder, output_file_name)

# Create a dictionary to hold the Product_Num mappings for the Product_Title
product_num_map = {'Momentum' : 1, 'MLOps' : 2, 'Impulse EDW' : 3, 'Inset BI' : 4, 'APIs' : 5}


#-------------- MAIN --------------
# Import the contents of the MPM JSON file
f = open(input_file_path, encoding="utf-8")
data = json.load(f)
f.close()


# Create variable to hold the contents of the replacement JSON objects
replacement_jsons = []

for article in data:
    article_id = f"{product_num_map[article['Product_Title']]}.{article['Section_Num']}.{article['Article_Num']}"
    body_text = article['Article_Body'] if (article_id in articles_to_copy) else ''
    replacement_jsons.append({"Product_Title": article['Product_Title'],
                              "Section_Title": article['Section_Title'],
                              "Article_Title": article['Article_Title'],
                              "Article_ID"   : article_id,
                              "Article_Body" : body_text})


# Create a new JSON file and write the product manual JSON objects to it
f = open(output_file_path, "w", encoding="utf-8")
f.write(json.dumps(replacement_jsons, indent=4))
f.close()
