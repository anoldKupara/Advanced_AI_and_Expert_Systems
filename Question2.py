import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Load knowledge base
with open('knowledge_base.json', 'r') as file:
    knowledge_base = json.load(file)

# Initialize tools
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()


# Preprocessing function
def preprocess_input(user_input):
    tokens = word_tokenize(user_input.lower())
    filtered_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    return filtered_tokens


# Match query to knowledge base
def get_response(user_input):
    processed_input = preprocess_input(user_input)

    for question, answer in knowledge_base.items():
        processed_question = preprocess_input(question)
        if any(word in processed_question for word in processed_input):
            return answer
    return "I'm sorry, I can't help with that. Please reach out to support."


# Main chatbot loop
def chatbot():
    print("Welcome to the University Chatbot! Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break

        response = get_response(user_input)
        print(f"Chatbot: {response}")


if __name__ == "__main__":
    chatbot()