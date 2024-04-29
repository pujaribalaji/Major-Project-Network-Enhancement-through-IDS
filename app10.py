import numpy as np
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for
import pickle

app = Flask(__name__)
model = pickle.load(open('netwrokmodel.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]

    features_name = ['protocol_type', 'flag', 'src_bytes', 'dst_bytes', 'count', 'same_srv_rate', 'diff_srv_rate', 'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_same_src_port_rate']

    df = pd.DataFrame(features_value, columns=features_name)
    output = model.predict(df)

    if output == 0:
        res_val = "No intrustion"
    else:
        res_val = "Network Intrustion happened"

    # Redirect to result route with the prediction text as a URL parameter
    return redirect(url_for('result', prediction=res_val))

@app.route('/result')
def result():
    # Retrieve the prediction text from the URL parameter
    prediction_text = request.args.get('prediction', 'No prediction')
    return render_template('result.html', prediction_text=prediction_text)

if __name__ == "__main__":
    app.run()
