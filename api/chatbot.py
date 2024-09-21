import PyPDF2
import nltk
from transformers import pipeline
from flask import Flask, request, jsonify

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)  # Use PdfReader instead of PdfFileReader
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def segment_text(text):
    sentences = nltk.sent_tokenize(text)
    return sentences

def create_chatbot(model_name='jondurbin/airoboros-gpt-3.5-turbo-100k-7b'):
    chatbot = pipeline("text-generation", model=model_name)
    return chatbot

def get_bot_response(chatbot, user_input):
    response = chatbot(user_input, max_new_tokens=100, do_sample=True)[0]['generated_text']
    return response

def split_text_into_chunks(text, chunk_size=2048):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def chatbot_with_pdf_context(pdf_text, user_input):
    chatbot = create_chatbot()
    pdf_chunks = split_text_into_chunks(pdf_text)  # Ensure input length is within limits

    responses = []
    for chunk in pdf_chunks:
        response = get_bot_response(chatbot, chunk)
        responses.append(response)

    return " ".join(responses)  # Combine responses if needed


# app = Flask(__name__)

# @app.route('/chat', methods=['POST'])
def chat():
    # user_input = request.json.get('message')
    pdf_text = extract_text_from_pdf('C:/Users/suraj/Projects/college-clarity/api/2022ENGG_CAP1_CutOff.pdf')
    response = chatbot_with_pdf_context(pdf_text, "can you help me find data for Government College of Engineering, Amravati?")
    print(response)
    return jsonify({'response': response})

# if __name__ == '__main__':
#     app.run(debug=True)

chat()


