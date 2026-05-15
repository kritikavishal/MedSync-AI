def validate_patient(name, symptoms, phone):

    if name == "":
        return "Name Required"

    if symptoms == "":
        return "Symptoms Required"

    if len(phone) != 10:
        return "Phone must be 10 digits"

    return None