import re
from rapidfuzz import process, fuzz  # Replace `fuzzywuzzy` with `rapidfuzz`, an alternative package
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK tokenizer if it's not already installed
nltk.download('punkt')

# Define a knowledge base with structured FAQs
knowledge_base = {
    "admissions_requirements": {
        "keywords": ["admissions", "requirements", "apply", "eligibility"],
        "response": "To apply for admission, you need to submit your high school transcripts, standardized test scores (if required), and a completed application form. For detailed requirements, visit our admissions page."
    },
    "academic_programs": {
        "keywords": ["programs", "courses", "majors", "classes", "fields", "study"],
        "response": "We offer a variety of programs, including majors in Computer Science, Business Administration, Biology, and more. Visit the academic programs page for detailed information."
    },
    "tuition_and_fees": {
        "keywords": ["tuition", "fees", "cost", "price", "payment"],
        "response": "Our tuition is $10,000 per semester for full-time undergraduate students. Additional fees may apply. Visit the tuition and fees page for more details."
    },
    "scholarships_and_financial_aid": {
        "keywords": ["scholarships", "financial aid", "grants", "funding"],
        "response": "We offer various scholarships and financial aid packages. Please visit the financial aid page to learn about available options and eligibility criteria."
    },
    "student_services": {
        "keywords": ["services", "health", "counseling", "support", "facilities"],
        "response": "Our student services include health and wellness programs, counseling services, and career support. Visit the student services page for more details."
    },
    "contact_information": {
        "keywords": ["contact", "email", "phone", "address"],
        "response": "You can contact us at contact@university.edu or call us at (123) 456-7890. We are located at 123 University Ave, Cityville."
    }
}


def preprocess_query(query):
    """
    Preprocess the user's query using basic NLP techniques.
    Tokenizes and lowers the case of all words.
    """
    query = query.lower()
    tokens = word_tokenize(query)
    return tokens


def find_best_match(tokens):
    """
    Find the best match for the user's query from the knowledge base.
    Uses keywords for matching and fuzzy matching for better accuracy.
    """
    all_keywords = {key: kb_entry['keywords'] for key, kb_entry in knowledge_base.items()}
    max_score = 0
    best_match = None

    for key, keywords in all_keywords.items():
        # Use fuzzy matching to find if tokens match any keywords
        for token in tokens:
            match, score = process.extractOne(
                keywords, token, scorer=fuzz.partial_ratio
            )
            if score > max_score:
                max_score = score
                best_match = key

    if max_score > 60:  # Set a threshold for keyword matching accuracy
        return best_match
    return None


def respond_to_query(query):
    tokens = preprocess_query(query)
    match = find_best_match(tokens)

    if match:
        # Return the corresponding response
        return knowledge_base[match]['response']
    else:
        return "I'm sorry, I couldn't understand your question. Could you please rephrase or ask something else?"


def main():
    print("Welcome to the University Chatbot! How can I assist you today?")
    print("You can ask about admissions, academic programs, tuition, scholarships, student services, or contact info.")

    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            print("Thank you for using the University Chatbot. Goodbye!")
            break

        response = respond_to_query(query)
        print(f"Chatbot: {response}")


if __name__ == "__main__":
    main()