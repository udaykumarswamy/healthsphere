
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 15:27:47 2024

@author: uday_kumar_swamy
"""
from flask import Flask, render_template, jsonify, request
import subprocess
import configparser
from parsedata import read_pdf_files_in_directory , response


# Read the properties file
config = configparser.ConfigParser()
config.read('config.properties')

# Get the template folder path from the properties file
template_folder = config.get('Flask', 'template_folder')

app = Flask(__name__, template_folder=template_folder)


@app.route("/")
def index():
    """
    Renders the index.html template.

    This function is a Flask route that renders the index.html template
    when the root URL ("/") of the application is accessed.

    Returns:
        str: The rendered HTML content of the index.html template.
    """
    return render_template("index.html")

@app.route('/crawl')
def crawl():
    """
    Crawls data using a Python script.

    This function triggers the execution of a Python script named datacrawler.py
    using the subprocess module. The Python script is expected to perform crawling
    operations to gather data.

    Returns:
        str: A message indicating that data crawling is in progress.
    """
    subprocess.run(['python', 'crawler/datacrawler.py'])
    return 'Crawling data...'

@app.route('/parse')
def parseData():
    """
    Parses data from PDF files in a directory.

    This function triggers the `read_pdf_files_in_directory` function,
    which reads PDF files in a directory and parses the data. The parsed
    data could be processed further as needed.

    Returns:
        str: A message indicating that data parsing is in progress.
    """
    read_pdf_files_in_directory()
    return 'Parsing Data...'

@app.route('/chat',methods=['POST'])
def chat():
    """
    Handles chat messages.

    This function receives chat messages sent via POST request in JSON format.
    It extracts the message tokens from the JSON data and passes them to the 
    `response` function to generate a response. The generated response is then 
    returned.

    Returns:
        str: The response to the chat message.
    """
    tokens = request.json.get('message', [])
    respons = response(tokens)
    return respons


if __name__ == "__main__":
    app.run(debug=True,port=8080,use_reloader=True)
