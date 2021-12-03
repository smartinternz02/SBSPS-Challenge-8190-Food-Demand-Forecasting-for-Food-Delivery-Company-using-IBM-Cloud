# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 22:14:16 2021

@author: Hafsa Sheikh
"""
import requests
import json
API_KEY = "qyNC12c3YyY0bhfyfYq0VVErI3i_iTxexfk059pJOhrq"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print("mltoken", mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": ["id", "week", "center_id", "meal_id", "checkout_price", "base_price", "emailer_for_promotion", "homepage_featured"], "values": [[ 2.0, 3, 647, 56, 3 ,250.0, 0, 0]]}]}

response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/346f6e2b-7733-496c-a352-abd243e8e46a/predictions?version=2021-11-30', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())
predictions = response_scoring.json()
print(predictions['predictions'][0]['values'][0][0])