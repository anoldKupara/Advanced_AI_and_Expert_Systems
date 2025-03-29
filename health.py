knowledge_base = {
    "Diabetes": ["fatigue", "increased thirst", "frequent urination"],
    "Hypertension": ["headaches", "dizziness", "blurred vision"],
    "Hyperthyroidism": ["weight loss", "rapid heartbeat", "sweating"],
    "Hypothyroidism": ["dry skin", "fatigue", "slow heart rate"],
    "Bronchitis": ["coughing", "chest discomfort", "shortness of breath"]
}

def diagnose_disease(symptoms):
    possible_diseases = []

    for disease, disease_symptoms in knowledge_base.items():
        matching_symptoms = [symptom for symptom in symptoms if symptom in disease_symptoms]
        if matching_symptoms:
            possible_diseases.append(disease)

    return possible_diseases

def main():
    print("Welcome to the Disease Diagnosis Centre")
    symptoms = input("Please enter your symptoms (comma-separated): ")

    symptoms = [symptom.strip().lower() for symptom in symptoms.split(",")]

    possible_diseases = diagnose_disease(symptoms)

    if possible_diseases:
        print("\nPossible Diseases based on your symptoms:")
        for disease in possible_diseases:
            print(f"- {disease}")
    else:
        print("\nNo matching disease found. Please visit the nearest medical centre and see a doctor.")

if __name__ == "__main__":
    main()
