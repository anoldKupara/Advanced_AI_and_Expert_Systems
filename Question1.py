from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches

app = Flask(__name__)

knowledge_base = {
    "malaria": ["fever", "chills", "sweating", "headache", "muscle pain", "nausea", "vomiting"],
    "migraine": ["severe headache", "nausea", "sensitivity to light", "blurred vision"],
    "lupus": ["fatigue", "joint pain", "rash", "fever", "hair loss", "sun sensitivity"],
    "flu": ["fever", "cough", "body aches", "fatigue", "sore throat", "runny nose"],
    "typhoid": ["fever", "weakness", "abdominal pain", "constipation", "rash", "headache"]
}

def correct_symptom(symptom):
    all_symptoms = [symptom for symptoms in knowledge_base.values() for symptom in symptoms]
    closest_match = get_close_matches(symptom, all_symptoms, n=1, cutoff=0.7)
    return closest_match[0] if closest_match else symptom

def diagnose(symptoms_input):
    diagnosis_score = {}

    for disease, symptoms in knowledge_base.items():
        match_count = sum(1 for symptom in symptoms_input if symptom in symptoms)
        diagnosis_score[disease] = match_count

    max_match = max(diagnosis_score.values())

    if max_match > 1:
        best_matches = [disease for disease, score in diagnosis_score.items() if score == max_match]
        return best_matches, max_match
    else:
        return [], 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def handle_diagnosis():
    data = request.json
    symptoms_input = [correct_symptom(symptom.strip().lower()) for symptom in data.get('symptoms', [])]
    diagnoses, match_count = diagnose(symptoms_input)

    if match_count > 0:
        response = {
            'status': 'success',
            'diagnoses': [d.capitalize() for d in diagnoses],
            'match_count': match_count
        }
    else:
        response = {
            'status': 'fail',
            'message': 'No significant matches found. Please consult a doctor.'
        }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)