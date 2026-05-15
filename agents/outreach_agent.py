import requests

# SEND DATA TO n8n

def send_to_n8n(name, symptoms, urgency, phone):

    requests.post(

        "http://localhost:5678/webhook/emergency-alert",

        json={

            "name":name,
            "symptoms":symptoms,
            "urgency":urgency,
            "phone":phone
        }
    )

# SEND SLACK ALERT

def send_slack_alert(name, symptoms, urgency, phone):

    webhook_url = "https://hooks.slack.com/services/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"

    message = {

        "text":

        f"🚨 Emergency Patient Detected\n\n"

        f"Name: {name}\n"

        f"Symptoms: {symptoms}\n"

        f"Urgency: {urgency}\n"

        f"Phone: {phone}"
    }

    requests.post(webhook_url, json=message)