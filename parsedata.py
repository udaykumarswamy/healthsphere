import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('punkt')
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from PIL import Image 
import pytesseract 
import sys 
import fitz
from pdf2image import convert_from_path 
import os
import nltk
from nltk.tokenize import word_tokenize
import spacy
import random
import string
import logging
import logging.config



logging.config.fileConfig('temp.conf')
logger = logging.getLogger('healthsphere')


def read_pdf_files_in_directory():
    logger.info('parsing started...')
    pdf_directory = '/Users/uday_kumar_swamy/Documents/work/spring-2024/IR/IR_project/HealthSphere/healthdata'
    corpus = ""
    if not os.path.exists(pdf_directory):
        print(f"Directory '{pdf_directory}' does not exist.")
        return corpus
    
    for file_name in os.listdir(pdf_directory):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(pdf_directory, file_name)
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                corpus += text
            doc.close()
    logger.info('parsing completed...')
    return corpus

sent_tokens = nltk.sent_tokenize(read_pdf_files_in_directory() ) #converts to list of scentences
word_tokens = nltk.word_tokenize(read_pdf_files_in_directory() ) #converts to list of words
sentToken = sent_tokens[:4]
wordToken = word_tokens[:4]
lemmer = nltk.stem.WordNetLemmatizer()
nltk.download('wordnet')

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

#Greetings
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREETING_RESPONSES = ["hi", "hey", "nods", "hi there", "hello", "I am glad! you are talking to me"]
def greeting(scentence):  
    for word in scentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
        


def response(user_response):
    chatbot_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words="english")
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-5:-1]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf == 0):
        chatbot_response = chatbot_response + "I am sorry! I don't understand you"
        return chatbot_response
    
    else:
        for i in range(4):
          chatbot_response += sent_tokens[idx[i]] + '\n'
          # Add the next 3 sentences after the matched sentence
        next_sentences = sent_tokens[idx[-1]+1:idx[-1]+5]
        chatbot_response += '\n'.join(next_sentences)
        return chatbot_response
