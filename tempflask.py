from flask import Flask, render_template, jsonify, request
import os
import subprocess
from parsedata import read_pdf_files_in_directory , response

app = Flask(__name__, template_folder="/Users/uday_kumar_swamy/Documents/work/spring-2024/IR/IR_project/HealthSphere/views/")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/crawl')
def crawl():
    # Call the Python script using subprocess
    subprocess.run(['python', '/Users/uday_kumar_swamy/Documents/work/spring-2024/IR/IR_project/HealthSphere/crawler/datacrawler.py'])
    return 'Crawling data...'

@app.route('/parse')
def parseData():
    # Assuming you receive tokens in JSON format
    read_pdf_files_in_directory()
    return 'Parsing Data...'

@app.route('/chat',methods=['POST'])
def chat():
    print('enter chat')
    tokens = request.json.get('message', [])
    print(tokens)
    respons = response(tokens)
    return respons

@app.route('/home')
def home():
    return "home!"


if __name__ == "__main__":
    app.run(debug=True,port=8080,use_reloader=True)
