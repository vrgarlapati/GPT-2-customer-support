# GPT-2-customer-support
## FINE TUNE A GENERATIVE PRE-TRAINED TRANSFORMER (GPT) MODEL AND CREATE AN INTERACTIVE HOW-TO-INSTRUCTION SYSTEM FOR CUSTOMER SUPPORT

### Project Introduction
Users running into issues operating the Momentum software may reach out to customer service for support, which requires support personnel to expend valuable time on providing assistance and causes customers to have to wait for answers, even for issues with potentially simple solutions. If provided with an alternate means of handling these requests that doesn’t require direct support by customer service, both support resources and customer time can be saved and applied to more critical tasks. The creation of a GPT-2 based customer service model fine-tuned to the Momentum product manual can supply an additional line of support that does not require human intervention. Through the use of this model, customers will be able to get their questions answered quickly and precisely based directly on information taken from the product manual, ensuring they will only need to reach out to support for the most complex issues.


### Repository Information

#### Table of Contents

- Documentation
- Requirements
- Setup
- Execution
- Maintainers


#### Documentation

This project utilizes the following documentation:
- https://accure.ai/docs
- https://huggingface.co/docs/transformers/model_doc/gpt2
- https://huggingface.co/docs/transformers/model_doc/gptj


#### Requirements

The machine where the actual model fine-tuning will be performed (using the scripts from the ModelCreation folder) requires all of the libraries listed in the "Requirements.txt" file to be installed. 

For all other folders, please ensure the libraries listed in the "required libraries" section at the top of each script are installed on the machine they will be executed on. Additionally, ensure the variables listed in the "environment variables & settings" section of each script are adjusted as needed.


#### Setup

##### Data Acquisition (WebScraper)

1. Navigate to the WebScraper/MPM_WebScraper script
2. Create an account on the Accure Inc. documentation page (https://accure.ai/docs) and check that you are able to log in successfully and access the Momentum Product Manual (MPM)
3. Using any utility that lets you access browser cookies, retrieve the cookie created when you logged into the page. (Should be in the format of "wordpress_logged_in_..." with a value of "<username>...")
4. Paste the retrieved cookie key & value into the "acct_cookies" variable in the MPM_WebScraper script's environment variables section, following the provided example
5. Execute the script and ensure MPM.txt & MPM.json files containing the contents of the MPM were successfully created in the Data/Scraping directory

##### Data Conditioning (DataConditioner)

1. Navigate to the DataConditioner/MPM_ManualAdjGenerator script
2. Under the "articles_to_copy" variable, specify the numbers (based on MPM.json) of any articles for which you wish to copy the text into the template for manual adjustments
3. Execute the script and ensure a MPM_manual_adj_template.json file based on the layout of the MPM.json file was successfully created in the Data/Conditioning directory
4. Fill out the MPM_manual_adj_template.json file by manually updating the text bodies for any articles that require changes (such as replacing figures & tables with text descriptions to retain important information). Afterwards, rename the file to MPM_manual_adj.json. (Alternatively, use the existing MPM_manual_adj.json with prior manual adjustments already in place and make any updates necessary.)
5. Execute the DataConditioner/MPM_DataConditioner script and ensure a MPM_conditioned.json containing the manual adjustments and other preprocessing was created in the Data/Conditioning directory

##### (Optional) Hyperparameter Tuning (ModelCreation/HyperparameterTuning)

1. Place the files from the ModelCreation/HyperparameterTuning/Metrics directory into the ModelCreation/HyperparameterTuning folder and adjust them to test any paramaters as necessary
2. Execute the HyperparameterTuning script and inspect the results to determine the best set of parameters to use
3. Navigate to the ModelCreation/ModelFinetuningAndVisualization/ModelFinetuningAndVisualization script and update the "training_args" variable with the discovered parameters

##### Model Fine-tuning (ModelCreation/ModelFinetuningAndVisualization)

1. Ensure the ModelCreation/ModelFinetuningAndVisualization/ModelFinetuningAndVisualization script is placed on a machine with sufficient specifications to perform the fine-tuning (e.g. Hopper Cluster with 80+ GB VRAM GPU)
2. Retrieve the MPM_conditioned.json created during the Data Conditioning step from the Data/Conditioning directory and placed it in the folder with the script, renaming it to "MPM.json"
3. Adjust all instances of the output folder in the script to whatever location you wish to save the model (currently set to '/scratch/kkonatha/test8')
4. Execute the fine-tuning script and inspect the test output and visualizations to determine its performance. Ensure the actual model was created in the specified output location
5. Deploy the fine-tuned model to its final location (e.g. MLOps)
6. Navigate to the FrontEnd/MPM_FrontEnd script and update the "model_url" and "API_token" variables to point to your hosted model_doc/gpt2

NOTE: The ModelCreation/ModelFinetuningAndVisualization/OtherVersions directory contains other versions of the fine-tuning script that may be useful. The "_Prior" version is an older version of the script with some additional visualizations, and the "_Experimental" version is a newer one attempting to address some problems with the current model, such as lack of default messages for unknown topics, though that version hasn't been fully evaluated.


### Execution

##### Gradio Front-end (FrontEnd)

1. Navigate to the FrontEnd/MPM_FrontEnd script and execute it
2. Open the link provided in the script's output to display the Gradio front-end
3. Enter queries on the left and hit submit, then wait for the generated response from the model to be returned


### Contributors

- Edward Wu
- John Patrick Wood
- Karunya Konathala
- Videsh Reddy Garlapati
- Valerie Caetto
