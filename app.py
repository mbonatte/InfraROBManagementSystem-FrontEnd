import uuid
import json

import pandas as pd

from pathlib import Path
THIS_FOLDER = Path(__file__).parent.resolve()

from functools import wraps

from flask import Flask, render_template, request, redirect, session, jsonify, send_file

from handle.handle_convert import get_converted_IC
from handle.handle_prediction import get_IC_through_time, get_IC_through_time_for_road, handle_PMS_prediction
from handle.handle_maintenance import get_IC_through_time_maintenance, get_IC_through_time_maintenance_road
from handle.handle_optimization import get_pareto_curve, get_pareto_curve_all_roads

app = Flask(__name__)
app.secret_key = 'your_secret_key1'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the username and password are valid
        if username == 'InfraROB_PMS' and password == 'InfraROB_PMS_123':
            session['logged_in'] = True
            return redirect('/home')
        else:
            return 'Invalid login credentials'
    return render_template('login.html')

@app.route('/')
@app.route('/home')
@login_required
def index():
    return render_template('home.html')

@app.route('/database/genericdatabase')
def download_generic_csv():
    path = THIS_FOLDER / 'database/GenericDataBase.csv'
    return send_file(path, as_attachment=True)
    
@app.route('/database/asfinagdatabase')
def download_asfinag_csv():
    path = THIS_FOLDER / './database/ASFiNAGDataBase.csv'
    return send_file(path, as_attachment=True)
    
@app.route('/database/roadproperties')
def download_road_properties_csv():
    path = THIS_FOLDER / './database/road_sections_properties.csv'
    return send_file(path, as_attachment=True)
    
@app.route('/database/actionseffect')
def download_actions_effect():
    path = THIS_FOLDER / './database/ActionsEffects.json'
    return send_file(path, as_attachment=True)

@app.route("/manual")
@login_required
def manual():
    manual_id = request.args.get('reference')
    if not manual_id:
        return render_template('manual.html')
    try:
        return render_template('manual/'+manual_id+'.html')
    except:
        return render_template('manual.html')

@app.route('/documents/ASFiNAG')
def download_ASFiNAG():
    path = THIS_FOLDER / 'documents/ASFiNAG.pdf'
    return send_file(path, as_attachment=True)

@app.route('/map')
@login_required
def show_maps():
    from datetime import datetime
    
    path_properties = THIS_FOLDER / './database/road_sections_properties.csv'
    path_inpections = THIS_FOLDER / './database/road_sections_inpections.csv'
    
    road_properties = pd.read_csv(path_properties).to_dict('records')
    road_inpections = pd.read_csv(path_inpections).to_dict('records')
    
    path = THIS_FOLDER / 'database/optimization_output.json'
    with open(path, "r") as file:
        road_optimizations = json.load(file)
    
    for road in road_properties:
        filtered_inspections = [r for r in road_inpections if r['Section_Name'] == road['Section_Name']]
        road['inspections'] = sorted(filtered_inspections, key=lambda d: datetime.strptime(d['Date'], "%d/%m/%Y"))
        
        road['optimization'] = road_optimizations[road['Section_Name']]
        
    path = THIS_FOLDER / 'database/ActionsEffects.json'
    with open(path, "r") as file:
        maintenanceActions = json.load(file)
    
    return render_template('map.html', roads=road_properties, maintenanceActions=maintenanceActions)

@app.route('/config', methods=['GET'])
@login_required
def config_PMS():
    return render_template('config.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/convert', methods=['POST'])
def convert_post():
    if ('inspectionsFile' not in request.files and 'propertiesFile' not in request.files):
        return jsonify({'error': 'No file uploaded'}), 400
        
    inspections_file = request.files['inspectionsFile']
    inspections_data = inspections_file.read().decode('utf-8')
    properties_file = request.files['propertiesFile']
    properties_data = properties_file.read().decode('utf-8')
    institution = json.loads(request.form['institution'])
    
    json_data = get_converted_IC(inspections_data,
                                 properties_data,
                                 institution,
                                 )
                                    
    response = jsonify(json_data)
    response.content_type = 'application/json'
    return response

@app.route('/markov', methods=['POST'])
def markov_post():
    if 'inspectionsFile' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    inspections_file = request.files['inspectionsFile']
    inspections_data = inspections_file.read().decode('utf-8')

    institution = json.loads(request.form['institution'])
    worst_best_IC = json.loads(request.form['worst_best_IC'])
    time_block = json.loads(request.form['time_block'])
    time_horizon = json.loads(request.form['time_horizon'])

    properties_data = None
    if institution == 'ASFiNAG':
        properties_file = request.files['propertiesFile']
        properties_data = properties_file.read().decode('utf-8')

    json_data = get_IC_through_time(
        inspections_data,
        institution,
        worst_best_IC['worst_IC'],
        worst_best_IC['best_IC'],
        time_block,
        time_horizon,
        asset_properties=properties_data
    )

    response = jsonify(json_data)
    response.content_type = 'application/json'
    return response

@app.route('/markov/road', methods=['POST'])
def markov_post_road():
    
    road = json.loads(request.form['road'])

    institution = 'ASFiNAG'
    worst_best_IC = {'worst_IC': 5, 'best_IC':1}
    time_block = 'year'
    time_horizon = 50

    json_data = get_IC_through_time_for_road(
        road,
        institution,
        worst_best_IC['worst_IC'],
        worst_best_IC['best_IC'],
        time_block,
        time_horizon
    )

    response = jsonify(json_data)
    response.content_type = 'application/json'
    return response

@app.route('/maintenance/road', methods=['POST'])
def maintenance_post_road():
    
    road = json.loads(request.form['road'])
    maintenance_scenario = json.loads(request.form['maintenance'])
    
    institution = 'ASFiNAG'
    worst_best_IC = {'worst_IC': 5, 'best_IC':1}
    time_block = 'year'
    time_horizon = 50
    
    path = THIS_FOLDER / 'database/ActionsEffects.json'
    with open(path, "r") as file:
        maintenance_data = json.load(file)

    json_data = get_IC_through_time_maintenance_road(
        road,
        institution,
        maintenance_scenario,
        maintenance_data,
        worst_best_IC['worst_IC'],
        worst_best_IC['best_IC'],
        time_block,
        time_horizon,
    )

    response = jsonify(json_data)
    response.content_type = 'application/json'
    return response

@app.route('/maintenance', methods=['POST'])
def maintenance_post():
    if ('inspectionsFile' not in request.files and 'maintenanceFile' not in request.files):
        return jsonify({'error': 'No file uploaded'}), 400
    inspections_file = request.files['inspectionsFile']
    inspections_data = inspections_file.read().decode('utf-8')
    
    maintenance_file = request.files['maintenanceFile']
    maintenance_data = json.loads(maintenance_file.read().decode('utf-8'))
    
    institution = json.loads(request.form['institution'])
    worst_best_IC = json.loads(request.form['worst_best_IC'])
    time_block = json.loads(request.form['time_block'])
    time_horizon = json.loads(request.form['time_horizon'])
    maintenance_scenario = json.loads(request.form['maintenanceScenario'])
    
    properties_data=None
    if institution == 'ASFiNAG':
        properties_file = request.files['propertiesFile']
        properties_data = properties_file.read().decode('utf-8')
    
    json_data = get_IC_through_time_maintenance(inspections_data,
                                                institution,
                                                maintenance_data,
                                                maintenance_scenario,
                                                worst_best_IC['worst_IC'],
                                                worst_best_IC['best_IC'],
                                                time_block,
                                                time_horizon,
                                                asset_properties = properties_data)
    response = jsonify(json_data)
    response.content_type = 'application/json'
    return response
      
@app.route('/optimization', methods=['POST'])
def optimization_post():
    if ('inspectionsFile' not in request.files and 'maintenanceFile' not in request.files):
        return jsonify({'error': 'No file uploaded'}), 400
    inspections_file = request.files['inspectionsFile']
    inspections_data = inspections_file.read().decode('utf-8')
    
    maintenance_file = request.files['maintenanceFile']
    maintenance_data = json.loads(maintenance_file.read().decode('utf-8'))

    worst_best_IC = json.loads(request.form['worst_best_IC'])
    time_block = json.loads(request.form['time_block'])
    time_horizon = json.loads(request.form['time_horizon'])
    result_id = json.loads(request.form['result_id'])

    optimization_output = get_pareto_curve(inspections_data,
                                           maintenance_data,
                                           int(worst_best_IC['worst_IC']),
                                           int(worst_best_IC['best_IC']),
                                           time_block,
                                           int(time_horizon)
                                           )

    # Writing to optimization_output.json
    path = THIS_FOLDER / 'database/optimization_output.json'
    with open(path, "r+") as file:
        data = json.load(file)
        data[result_id] = optimization_output
        file.seek(0)
        file.write(json.dumps(data,
                              indent=4))
    
    response = jsonify(optimization_output)
    response.content_type = 'application/json'
    return response

@app.route('/run_optimization', methods=['POST'])
def run_optimization():
    return get_pareto_curve_all_roads()

@app.route("/get_optimization_result")
def submit_info():
    _hash = request.args.get('result_id')
    
    path = THIS_FOLDER / 'database/optimization_output.json'
    with open(path, "r") as file:
        data = json.load(file)
    try:    
        response = jsonify(data[_hash])
        response.content_type = 'application/json'
        return response
    except KeyError:
        return jsonify({'error': 'No result found'}), 404

@app.route('/prediction', methods=['POST'])
def prediction_post():
    data = request.get_json(force=True)

    thetas = data['prediction_thetas']
    actions = data['actions_effect']
    action_schedule = data.get('action_schedule', {})
    road_properties = data['road_properties']
    prediction_settings = data['prediction_settings']
    
    ASFiNAG_indicators = handle_PMS_prediction(
        road_properties = road_properties,
        thetas = thetas,
        actions = actions,
        action_schedule = action_schedule,
        **prediction_settings)
    
    response = jsonify(ASFiNAG_indicators)
    response.content_type = 'application/json'
    return response


if __name__ == '__main__':
    app.run(debug=True)
