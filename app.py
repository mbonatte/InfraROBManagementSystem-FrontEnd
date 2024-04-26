import io
import uuid
import json

import numpy as np
import pandas as pd

from pathlib import Path
THIS_FOLDER = Path(__file__).parent.resolve()

from functools import wraps

from flask import Flask, render_template, request, redirect, session, jsonify, send_file

from handle.handle_convert import get_converted_IC
from handle.handle_fit_model import get_fitted_model
from handle.handle_prediction import handle_PMS_prediction
from handle.handle_optimization import handle_PMS_optimization
from handle.handle_optimization_network import handle_PMS_network_optimization

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
    try:
        data = request.get_json(force=True)
        # Validate essential fields
        if 'road_sections' not in data or 'institution' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        json_data = get_converted_IC(data['road_sections'], data['institution'])
        response = jsonify(json_data)
        response.content_type = 'application/json'
        return response
    except KeyError as e:
        return jsonify({'error': f'Missing key {e.args[0]}'}), 400
    except Exception as e:
        # General error handling (unexpected errors)
        return jsonify({'error': str(e)}), 500

@app.route('/fit_model', methods=['POST'])
def fit_model_post():    
    try:
        data = request.get_json(force=True)
        
        # Validate essential fields
        if 'institution' not in data or 'road_sections' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        json_data = get_fitted_model(data['institution'], data['road_sections'])
        response = jsonify(json_data)
        response.content_type = 'application/json'
        return response
    except KeyError as e:
        return jsonify({'error': f'Missing key {e.args[0]}'}), 400
    except Exception as e:
        # General error handling (unexpected errors)
        return jsonify({'error': str(e)}), 500

      
# @app.route('/optimization', methods=['POST'])
# def optimization_post():
#     if ('inspectionsFile' not in request.files and 'maintenanceFile' not in request.files):
#         return jsonify({'error': 'No file uploaded'}), 400
#     inspections_file = request.files['inspectionsFile']
#     inspections_data = inspections_file.read().decode('utf-8')
    
#     maintenance_file = request.files['maintenanceFile']
#     maintenance_data = json.loads(maintenance_file.read().decode('utf-8'))

#     worst_best_IC = json.loads(request.form['worst_best_IC'])
#     time_block = json.loads(request.form['time_block'])
#     time_horizon = json.loads(request.form['time_horizon'])
#     result_id = json.loads(request.form['result_id'])

#     optimization_output = get_pareto_curve(inspections_data,
#                                            maintenance_data,
#                                            int(worst_best_IC['worst_IC']),
#                                            int(worst_best_IC['best_IC']),
#                                            time_block,
#                                            int(time_horizon)
#                                            )

#     # Writing to optimization_output.json
#     # path = THIS_FOLDER / 'database/optimization_output.json'
#     # with open(path, "r+") as file:
#     #     data = json.load(file)
#     #     data[result_id] = optimization_output
#     #     file.seek(0)
#     #     file.write(json.dumps(data,
#     #                           indent=4))
    
#     response = jsonify(optimization_output)
#     response.content_type = 'application/json'
#     return response

# @app.route('/run_optimization', methods=['POST'])
# def run_optimization():
#     return get_pareto_curve_all_roads()

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
    try:
        data = request.get_json(force=True)
        
        # Validate essential fields
        required_fields = ['prediction_thetas', 'road_properties', 'prediction_settings']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        thetas = data['prediction_thetas']
        actions = data.get('actions_effect', {})
        action_schedule = data.get('action_schedule', {})
        initial_ICs = data.get('initial_ICs', {})
        road_properties = data['road_properties']
        prediction_settings = data['prediction_settings']
        
        ASFiNAG_indicators = handle_PMS_prediction(
            road_properties=road_properties,
            thetas=thetas,
            actions=actions,
            action_schedule=action_schedule,
            initial_ICs=initial_ICs,
            **prediction_settings)
        
        response = jsonify(ASFiNAG_indicators)
        response.content_type = 'application/json'
        return response
    except KeyError as e:
        return jsonify({'error': f'Missing key {e.args[0]}'}), 400
    except Exception as e:
        # General error handling (unexpected errors)
        return jsonify({'error': str(e)}), 500

@app.route('/optimization', methods=['POST'])
def optimization_PMS_post():
    try:
        data = request.get_json(force=True)
        
        # Validate essential fields
        required_fields = ['prediction_thetas', 'actions_effect', 'road_properties', 'prediction_settings', 'optimization_settings']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        thetas = data['prediction_thetas']
        actions = data['actions_effect']
        initial_ICs = data.get('initial_ICs', {})
        road_properties = data['road_properties']
        prediction_settings = data['prediction_settings']
        optimization_settings = data['optimization_settings']
        
        ASFiNAG_indicators = handle_PMS_optimization(
            road_properties=road_properties,
            thetas=thetas,
            actions=actions,
            initial_ICs=initial_ICs,
            **prediction_settings,
            **optimization_settings)
        
        response = jsonify(ASFiNAG_indicators)
        response.content_type = 'application/json'
        return response
    except KeyError as e:
        return jsonify({'error': f'Missing key {e.args[0]}'}), 400
    except Exception as e:
        # General error handling (unexpected errors)
        return jsonify({'error': str(e)}), 500

@app.route('/optimization_network', methods=['POST'])
def optimization_network_PMS_post():
    try:
        data = request.get_json(force=True)

        # Check for essential fields
        if 'road_optimization' not in data or 'optimization_settings' not in data:
            return jsonify({'error': 'Missing required fields'}), 400

        road_optimization = data['road_optimization']
        optimization_settings = data['optimization_settings']
        
        result = handle_PMS_network_optimization(
            road_optimization=road_optimization,
            **optimization_settings
        )
        
        response = jsonify(result)
        response.content_type = 'application/json'
        return response
    except KeyError as e:
        return jsonify({'error': f'Missing key {e.args[0]}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
