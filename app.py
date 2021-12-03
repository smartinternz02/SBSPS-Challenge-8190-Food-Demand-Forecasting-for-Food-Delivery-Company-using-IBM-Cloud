import pandas as pd
import numpy as np
import pickle
import os
from flask import Flask, request, render_template
import requests
import json
API_KEY = "qyNC12c3YyY0bhfyfYq0VVErI3i_iTxexfk059pJOhrq"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print("mltoken", mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app= Flask(__name__, template_folder="templates")
@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/home', methods=['GET'])
def about():
    return render_template('home.html')

@app.route('/pred', methods=['GET'])
def page():
    return render_template('upload.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    print("[INFO] loading model...")
    model = pickle.loads(open('fdemand.pkl', "rb").read())
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    print(features_value)
    features_name = ['homepage_featured', 'emailer_for_promotion', 'op_area', 'cuisine','city_code', 'region_code', 'category']
    
    prediction = model.predict(features_value)
    output=prediction[0]
    print(output)
    return render_template('upload.html', prediction_text= output)

 
    payload_scoring = {"input_data": [{"field": ["id", "week", "center_id", "meal_id", "checkout_price", "base_price", "emailer_for_promotion", "homepage_featured"], "values": [[1379560, 1, 55, 2539, 340.0, 205.0, 0, 1]]}]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/346f6e2b-7733-496c-a352-abd243e8e46a/predictions?version=2021-11-30', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions = response_scoring.json()
    print(predictions['predictions'][0]['values'][0][0])
    
    
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8000, debug=False)