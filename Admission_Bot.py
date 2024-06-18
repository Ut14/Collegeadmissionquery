import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Sample data of admission-related questions and responses
admission_data = {
    "procedures": "The admission procedure involves filling out an application form, submitting required documents, and attending an interview.",
    "requirements": "To apply, you need your high school transcripts, standardized test scores, letters of recommendation, and a personal statement.",
    "deadlines": "Application deadlines vary by college. Please check the respective college's website for specific dates."
}

# Preprocess the data
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]
    tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(tokens)

# Preprocess the admission data
preprocessed_admission_data = {key: preprocess(value) for key, value in admission_data.items()}

# Create TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the admission data
tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_admission_data.values())

# Function to get response to user query
def get_response(query):
    query_vector = tfidf_vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix)
    most_similar_index = np.argmax(similarity_scores)
    return list(admission_data.keys())[most_similar_index]

# Function to provide personalized responses based on user context
def provide_personalized_response(user_input):
    return admission_data[user_input]

# Example conversation loop
print("Welcome to College Admission Chatbot!")
print("Ask me anything about admission procedures, requirements, deadlines, or any other related topic. Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Chatbot: Goodbye!")
        break
    else:
        response_key = get_response(preprocess(user_input))
        if response_key in admission_data:
            response = provide_personalized_response(response_key)
            print("Chatbot:", response)
        else:
            print("Chatbot: I'm sorry, I couldn't understand your question. Please try rephrasing or ask another question related to admission procedures, requirements, deadlines, or any other related topic.")

        # Ask if the user has more questions
        more_questions = input("Chatbot: Do you have more questions? (yes/no): ")
        if more_questions.lower() != 'yes':
            print("Chatbot: Okay, feel free to ask whenever you have more questions. Goodbye!")
            break
