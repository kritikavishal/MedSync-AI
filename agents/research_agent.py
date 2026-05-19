from openai import OpenAI

# GROQ CLIENT

client = OpenAI(

    api_key= #add your own api key

    base_url= # ADD THE BASE URL
)

def medical_research(symptoms, urgency):

    prompt = f"""
Patient Symptoms: {symptoms}
Urgency Score: {urgency}

Rules:

- Urgency below 50 = Low Severity
- Urgency between 50 and 89 = Moderate Severity
- Urgency 90 and above = Critical Severity

Analyze and provide:

🩺 Department
⚠ Severity
📋 Recommendation

If urgency score is below 50:
also provide:

💊 Basic OTC medicine suggestions
🏠 Home remedies

If urgency score is above 90:
recommend immediate emergency medical attention.

Keep the response:
- short
- professional
- healthcare style
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    result = response.choices[0].message.content

    return result
