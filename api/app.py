import json

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

from api.prediction.handle_prediction import get_IC_through_time

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/markov', methods=['GET', 'POST'])
#@cross_origin()
def upload():
    if request.method == 'GET':
        return render_template('markov.html')
    if 'csvFile' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    csv_file = request.files['csvFile']
    csv_data = csv_file.read().decode('utf-8')
    additionalInfo = json.loads(request.form['additionalInfo'])
    
    #json_data = handle_prediction.get_IC_through_time(csv_data,
                                                      #additionalInfo['worst_IC'],
                                                      #additionalInfo['best_IC'])
    json_data = {'test': 'asd'}
    response = jsonify(json_data)
    #response.content_type = 'application/json'
    #response.headers.add('Access-Control-Allow-Origin', '*')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,OPTIONS')
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/maintenance')
def maintenance():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()
