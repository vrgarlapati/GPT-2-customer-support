#!/usr/bin/env python3

## Creates a Gradio-based web interface that users can interact with and pose questions to. The questions are sent via 
## REST API calls to a GPT model fine-tuned to the conditioned Momentum Product Manual dataset and hosted in a MLOPS instance
## on AWS. The responses generated by the model are received via a REST response and returned to the user in text form through
## the interface.


#-------------- SETUP --------------
# Import required libraries
import gradio as gr
import requests
import time


# Set environment variables & settings (edit these to fit environment)
#MLOPS Endpoint Config
model_url = "http://one.accure.ai:8446/mlops/v1/predict/interaction_101/2/default_cluster"
API_token = "8b33b192db3f50b488f005aaa7d6cd0e2fef8ea6"

#Time Settings (in seconds)
initialwait = 1
retrytime   = 5
timeout     = 60


#-------------- FUNCTIONS --------------
def call_gpt_endpoint(input_text):
    payload = {
        "X": [{"text": input_text}]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {API_token}"
    }
    
    response = requests.post(model_url, json=payload, headers=headers)
    
    await_rest_response(response)
    
    if response.status_code == 200:
        return response.json()["result"]["pred_response"]["predictions"][0][0]["generated_text"]
    else:
        return f"Error: Unable to get response from the MPS Chatbot. Status code: {response.status_code}"
    
def await_rest_response(response):
    time.sleep(initialwait)
    time_elapsed = initialwait
    
    while response.status_code == 204:
        if (time_elapsed > timeout or response.status_code != 204):
            break
        else:
            time.sleep(retrytime)
            time_elapsed += retrytime


#-------------- MAIN --------------
iface = gr.Interface(
    fn=call_gpt_endpoint,
    title="Momentum Product Support",
    description="A web interface utilizing a fine-tuned GPT model to answer questions regarding the Momentum suite of products.",
    inputs=gr.Textbox(lines=4, label="Please enter your question:"),
    outputs=gr.Textbox(label="MPS Chatbot Response")
)

iface.launch()