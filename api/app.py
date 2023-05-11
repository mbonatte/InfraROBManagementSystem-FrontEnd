import json

from flask import Flask, render_template, request, jsonify

from prediction.handle_prediction import get_IC_through_time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/inspections')
def inspections():
    return render_template('home.html')

@app.route('/markov', methods=['GET', 'POST'])
#@cross_origin()
def upload():
    if request.method == 'GET':
        return render_template('markov.html')
    if 'inspectionsFile' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    inspections_file = request.files['inspectionsFile']
    inspections_data = inspections_file.read().decode('utf-8')
    worst_best_IC = json.loads(request.form['worst_best_IC'])
    time_block = json.loads(request.form['time_block'])
    time_hoziron = json.loads(request.form['time_horizon'])
    
    json_data = get_IC_through_time(inspections_data,
                                    worst_best_IC['worst_IC'],
                                    worst_best_IC['best_IC'],
                                    time_block,
                                    time_hoziron)
    response = jsonify(json_data)
    response.content_type = 'application/json'
    return response

@app.route('/maintenance')
def maintenance():
    return render_template('home.html')

@app.route('/optimization')
def optimization():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()
