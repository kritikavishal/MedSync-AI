def classify_patient(symptoms):

    urgency = 30

    symptoms_lower = symptoms.lower()

    # HIGH PRIORITY

    if "chest pain" in symptoms_lower:
        urgency = 95

    elif "breathing problem" in symptoms_lower:
        urgency = 90

    elif "accident" in symptoms_lower:
        urgency = 100

    elif "heart attack" in symptoms_lower or "heartattack" in symptoms_lower:
        urgency = 100

    # MEDIUM PRIORITY

    elif "fever" in symptoms_lower:
        urgency = 60

    elif "vomiting" in symptoms_lower:
        urgency = 55

    elif "body pain" in symptoms_lower:
        urgency = 50

    # LOW PRIORITY

    elif "headache" in symptoms_lower:
        urgency = 40

    elif "cold" in symptoms_lower:
        urgency = 30

    return urgency