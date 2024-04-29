import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('netwrokmodel.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extracting input features from the form
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]

    # Feature names for creating DataFrame
    features_name = ['protocol_type', 'flag', 'src_bytes', 'dst_bytes', 'count', 'same_srv_rate', 'diff_srv_rate', 'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_same_src_port_rate']

    # Creating DataFrame from input features
    df = pd.DataFrame(features_value, columns=features_name)

    # Using the loaded model for prediction
    output = model.predict(df)
    print(output)

    # Mapping the output label to human-readable form
    res_val = "fraudulent" if output == 4 else "No fraudulent"

    return render_template('index.html', prediction_text='Patient has {}'.format(res_val))

if __name__ == "__main__":
    app.run()
