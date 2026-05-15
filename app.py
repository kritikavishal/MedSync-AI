from flask import Flask, render_template, request, jsonify
import sqlite3

# IMPORT AGENTS

from agents.ingestion_agent import ingest_patient
from agents.validation_agent import validate_patient
from agents.classification_agent import classify_patient
from agents.research_agent import medical_research
from agents.outreach_agent import send_to_n8n, send_slack_alert

app = Flask(__name__)

# DATABASE CONNECTION

conn = sqlite3.connect('medsync.db', check_same_thread=False)

cursor = conn.cursor()

# CREATE TABLE

cursor.execute('''
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    symptoms TEXT,
    urgency INTEGER,
    phone TEXT
)
''')

conn.commit()

# HOME PAGE

@app.route('/')
def home():
    return render_template('index.html')

# DASHBOARD PAGE

@app.route('/dashboard')
def dashboard():

    cursor.execute("SELECT * FROM patients")

    patients = cursor.fetchall()

    total_patients = len(patients)

    emergency_cases = 0
    medium_cases = 0
    low_cases = 0

    for patient in patients:

        urgency = patient[3]

        if urgency >= 90:
            emergency_cases += 1

        elif urgency >= 50:
            medium_cases += 1

        else:
            low_cases += 1

    return render_template(
        'dashboard.html',
        patients=patients,
        total_patients=total_patients,
        emergency_cases=emergency_cases,
        medium_cases=medium_cases,
        low_cases=low_cases
    )

# SUBMIT API

@app.route('/submit', methods=['POST'])
def submit():

    data = request.json

    # INGESTION AGENT

    name, symptoms, phone = ingest_patient(data)

    # VALIDATION AGENT

    validation_error = validate_patient(
        name,
        symptoms,
        phone
    )

    if validation_error:

        return jsonify({
            "error":validation_error
        })

    # CLASSIFICATION AGENT

    urgency = classify_patient(symptoms)

    # RESEARCH AGENT

    recommendation = medical_research(
    symptoms,
    urgency
)

    # SAVE DATA

    cursor.execute(
        "INSERT INTO patients(name,symptoms,urgency,phone) VALUES(?,?,?,?)",
        (name, symptoms, urgency, phone)
    )

    conn.commit()

    # SEND ALL DATA TO n8n

    send_to_n8n(
        name,
        symptoms,
        urgency,
        phone
    )

    # ALERT STATUS

    alert = "Normal"

    if urgency >= 90:

        alert = "EMERGENCY CASE"

        # SEND SLACK ALERT

        send_slack_alert(
            name,
            symptoms,
            urgency,
            phone
        )

    return jsonify({
        "message":"Patient Added",
        "urgency":urgency,
        "alert":alert,
        "recommendation":recommendation
    })

if __name__ == '__main__':
    app.run(debug=True)