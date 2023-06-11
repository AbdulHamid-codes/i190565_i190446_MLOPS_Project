from flask import request
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import numpy as np
from flask import redirect
from contextlib import _RedirectStream
from flask import Flask, render_template, url_for

from flask_googlemaps import GoogleMaps

app = Flask(__name__)


# # Initialize the extension
# GoogleMaps(app)


@app.route('/')
def index():
    return render_template('options.html')


with open('linearRegression_model.pkl', 'rb') as f:
    model = pickle.load(f)


@app.route('/demand_supply')
def demand_supply():
    return render_template('demand_supply.html')


@app.route('/ride_cancellation')
def ride_cancellation():
    return render_template('ride_cancellation.html')


@app.route('/submit-form', methods=['POST'])
def submit_form():
    region_id = int(request.form.get('region_id'))
    time_slot = int(request.form.get('time_slot'))

    print("Region id: ", region_id, "Time Slot: ", time_slot)
    print(type(region_id), "    ", type(time_slot))
    data = {"region_id": region_id, "time_slot": time_slot}

    # Convert the input values to a NumPy array
    input_vals = np.array([[region_id, time_slot]])
    # my_dataframe = pd.DataFrame(input_vals)

    # create a DataFrame from the numpy array with column names
    df = pd.DataFrame(input_vals, columns=['region_id', 'time_slot'])

    with open('linearRegression_model.pkl', 'rb') as f:
        model = pickle.load(f)
     # Make a prediction using the loaded model
    prediction = model.predict(df)

    # Return the prediction as a string
    predicted_ds_gap = prediction[0][0]
    data["gap"] = round(predicted_ds_gap)

    return render_template('prediction.html', data=data)


@app.route('/find_drivers', methods=['POST'])
def find_drivers():
    with open('frequentDrivers.pickle', 'rb') as f:
        fd = pickle.load(f)
     # Make a prediction using the loaded model
    drivers = fd

    return render_template('frequent_drivers.html', data=drivers)


if __name__ == "__main__":
    app.run(port=5001)
