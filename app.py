import json
from flask import Flask, request, app, jsonify, url_for, render_template  # type: ignore
import numpy as np
import pandas as pd
import joblib

app = Flask(__name__)

# Load the model
regmodel = joblib.load('regmodel.joblib')
scaler = joblib.load('scaler.joblib')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('https://illustrious-yeot-e1cc48.netlify.app/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    print(data)
    new_data = scaler.transform(np.array(list(data.values())).reshape(1, -1))
    output = regmodel.predict(new_data)
    print(output[0])
    return jsonify(int(output[0]))  # Convert to int before jsonify

@app.route('/predict', methods=['POST'])
def predict():
    data = [float(x) for x in request.form.values()]
    final_input = scaler.transform(np.array(data).reshape(1, -1))
    print(final_input)
    output = regmodel.predict(final_input)[0]
    return render_template("home.html", prediction_text="The House price prediction is {}".format(output))

if __name__ == "__main__":
    app.run(debug=True)

    