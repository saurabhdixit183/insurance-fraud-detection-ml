from flask import Flask, render_template, request
import numpy as np
import pickle

# Load model and scaler
model = pickle.load(open("dtc_model.pkl", "rb"))
scaler = pickle.load(open("Std_Scaler.pkl", "rb"))

app = Flask(__name__)


def get_value(name):
    """Safely get float value from form (blank -> 0)"""
    value = request.form.get(name, "").strip()
    try:
        return float(value) if value != "" else 0.0
    except:
        return 0.0


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    features = [[
        get_value("months_as_customer"),
        get_value("policy_number"),
        get_value("policy_bind_date"),
        get_value("policy_state"),
        get_value("policy_csl"),
        get_value("policy_deductable"),
        get_value("policy_annual_premium"),
        get_value("insured_zip"),
        get_value("insured_sex"),
        get_value("insured_education_level"),
        get_value("insured_occupation"),
        get_value("insured_hobbies"),
        get_value("insured_relationship"),
        get_value("capital_gains"),
        get_value("capital_loss"),
        get_value("incident_date"),
        get_value("incident_month"),
        get_value("incident_type"),
        get_value("collision_type"),
        get_value("incident_severity"),
        get_value("authorities_contacted"),
        get_value("incident_state"),
        get_value("incident_city"),
        get_value("incident_location"),
        get_value("incident_hour_of_the_day"),
        get_value("number_of_vehicles_involved"),
        get_value("property_damage"),
        get_value("bodily_injuries"),
        get_value("witnesses"),
        get_value("police_report_available"),
        get_value("total_claim_amount"),
        get_value("auto_make"),
        get_value("auto_model"),
        get_value("auto_year")
    ]]

    # scale input
    scaled = scaler.transform(features)

    # prediction
    prediction = model.predict(scaled)[0]

    if prediction == 0:
        result = "Legal Insurance Claim"
    else:
        result = "Fraud Insurance Claim"

    return render_template("index.html", predict=result)


if __name__ == '__main__':
    app.run(debug=True)