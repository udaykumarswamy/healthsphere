#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 15:27:47 2024

@author: uday_kumar_swamy
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import warnings
import fitz
import os
import string
import logging
import logging.config
import configparser
nltk.download('punkt')
warnings.filterwarnings('ignore')

# Read the properties file
config = configparser.ConfigParser()
config.read('config.properties')

logConf = config.get('LogFile', 'logConfiguration')
downloadPath = config.get('download','downloadPath')

logging.config.fileConfig(logConf)
logger = logging.getLogger('healthsphere')
try:
    os.mkdir(downloadPath)
except:
    logger.info('directory exists..')

def read_pdf_files_in_directory():
    """
    Reads text from PDF files within a directory and constructs a corpus.

    Returns:
        str: The corpus containing text from all PDF files in the directory.
    """
    logger.info('parsing started...')
    pdf_directory = downloadPath
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
    tokenise(corpus)
    logger.info('parsing completed...')
    return corpus



sent_tokens =[]
word_tokens = []
sentToken = []
wordToken =[]
def tokenise(corpus):
    """
    Tokenizes the input corpus into sentences and words.

    Args:
        corpus (str): The input text corpus.

    Returns:
        None
    """
    global sent_tokens, word_tokens, sentToken, wordToken
    sent_tokens =  nltk.sent_tokenize(corpus) #converts to list of scentences
    word_tokens = nltk.word_tokenize(corpus) #converts to list of words
    sentToken = sent_tokens[:4]
    wordToken = word_tokens[:4] 
    
 
   

lemmer = nltk.stem.WordNetLemmatizer()
nltk.download('wordnet')
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemTokens(tokens):
    """
    Lemmatizes a list of tokens using a lemmatizer.

    Args:
        tokens (list): A list of tokens to be lemmatized.
        lemmer: A lemmatizer object.

    Returns:
        list: A list of lemmatized tokens.
    """
    return [lemmer.lemmatize(token) for token in tokens]


def LemNormalize(text):
    """
    Normalizes and lemmatizes text.

    Args:
        text (str): The text to be normalized and lemmatized.
        lemmer: A lemmatizer object.
        remove_punct_dict: A dictionary for removing punctuation.

    Returns:
        list: A list of lemmatized tokens.
    """
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


def response(user_response):
    """
    Generates a response from the chatbot based on the user's input.

    Args:
        user_response (str): The user's input.
        sent_tokens (list): A list of sentence tokens.
        TfidfVec: A TF-IDF vectorizer object.

    Returns:
        str: The chatbot's response.
    """
    chatbot_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words="english")
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-5:-1]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    distances = cosine_distances(tfidf[-1], tfidf[:-1])[0]  # Compute cosine distances with all documents except the last one (user_response)
    idx_distances = [(i, distance) for i, distance in enumerate(distances)]
    idx_distances.sort(key=lambda x: x[1])  # Sort based on distances
    top_5_idx_distances = idx_distances[:5]  # Get the top 5 distances and their indices
    
    # Extract information about the matched documents and their indices
    matched_documents = [sent_tokens[i] for i, _ in top_5_idx_distances]
    matched_indices = [i for i, _ in top_5_idx_distances]
   
    
    if(req_tfidf == 0):
        chatbot_response = chatbot_response + "I am sorry! I don't understand you, try another keyword or parse data again."
        return chatbot_response
    
    else:
        for i in range(4):
          chatbot_response += sent_tokens[idx[i]] + '\n'
          
        next_sentences = sent_tokens[idx[-1]+1:idx[-1]+5]
        chatbot_response += '\n'.join(next_sentences)
        distances_str = '\n'.join([str(d) for d in top_5_idx_distances])
        indices_str = '\n'.join([str(i) for i in matched_indices])

        chatbot_response += '\n'.join(matched_documents)
        chatbot_response += '\n\n'

        chatbot_response += 'Distances:\n' + distances_str + '\n\n'
        chatbot_response += 'Indices:\n' + indices_str
        return chatbot_response 


