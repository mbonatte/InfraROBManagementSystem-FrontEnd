// modes.js

// JavaScript for mode switching
const current_mode = document.getElementById('current-mode');

const visualizeModeIcon = document.getElementById('visualize-mode');
const predictionModeIcon = document.getElementById('prediction-mode');
const maintenanceModeIcon = document.getElementById('maintenance-mode');
const optimizationModeIcon = document.getElementById('optimization-mode');

function getCurrentMode(){
    mode = current_mode.innerHTML.split(' ')[2].split('<')[0];
    return mode;
}

const mapModeToFunction = {'visualize': switchToVisualizeMode,
                     'prediction': switchToPredictionMode,
                     'maintenance': switchToMaintenanceMode,
                     'optimization': switchToPOptimizationMode
                     };

// Function to switch to Visualize Mode
function switchToVisualizeMode() {
    // Implement logic to switch to Visualize Mode
    // For example, update the UI and make database requests
    //current_mode.innerHTML = '<h1>Current Mode: Visualize</h1>';
}

// Function to switch to Prediction Mode
function switchToPredictionMode() {
    // Implement logic to switch to Prediction Mode
    // Update the UI
    
    
    // Make prediction requests
}

// Function to switch to Visualize Mode
function switchToMaintenanceMode() {
    // Implement logic to switch to Visualize Mode
    // Update the UI
    
    addActionFields(infoDiv);
    
    // Make database requests
}

// Function to switch to Prediction Mode
function switchToPOptimizationMode() {
    // Implement logic to switch to Prediction Mode
    // For example, update the UI and make prediction requests
    
    addOptimizationFields(infoDiv);
    
    //createChart('newChart', data.Performance, data.Cost, 'Area under curve', 'Cost', `Pareto curve - ${result_id}`);
    //plotDummies(data.Dummies)
    //addResultFields(data);
}

// Function to switch modes
window.addEventListener('load', switchMode());
function switchMode(mode='visualize') {
    console.log(`DEBUGGING - switchMode - ${mode}`);
    //hideSidebar();
    // Implement logic to switch to the selected mode
    
    // For example, update the UI and make requests based on the mode
    current_mode.innerHTML = `<h1>Current Mode: ${mode}</h1>`;
    
    // Highlight the active mode icon and remove active class from others
    document.querySelectorAll('.sidebar-icon').forEach((icon) => {
        if (icon.id === `${mode}-mode`) {
            icon.classList.add('active');
            mapModeToFunction[mode]();
        } else {
            icon.classList.remove('active');
        }
    });
    
    // Update the UI
    if (mode === 'maintenance') {
            infoDiv.innerHTML = '';
            switchToMaintenanceMode();
    } else if (mode === 'optimization') {
            infoDiv.innerHTML = '';
            switchToPOptimizationMode();
    } else {
        displayRoadInfo({});
    };
}

// Event listeners for mode switching (using a single function)
document.querySelectorAll('.sidebar-icon').forEach((icon) => {
    icon.addEventListener('click', () => {
        const mode = icon.id.replace('-mode', ''); // Extract the mode from the icon ID
        switchMode(mode);
    });
});

////////////////////////////////////////////////////////////////////
// MAINTENANCE //
function creatNumMaintenanceSelect(div){
    // Create and append the "Select the number of maintenance actions" dropdown
    const numMaintenanceSelect = document.createElement('select');
    numMaintenanceSelect.id = 'numMaintenanceSelect';

    const option_1 = document.createElement("option");
    option_1.value = 'numMaintenance';
    option_1.text = 'Select the number of maintenance actions:';
    numMaintenanceSelect.appendChild(option_1);
    
    for (let i = 1; i < 5; i++) {
        const option1 = document.createElement("option");
        option1.value = i;
        option1.text = i;
        numMaintenanceSelect.appendChild(option1);
    };
    
    div.appendChild(numMaintenanceSelect);
    
    return numMaintenanceSelect
    
};

function addActionFields(div) {
    const numMaintenanceSelect = creatNumMaintenanceSelect(div);
    
    // Create and append an event listener to generate the form on selection change
    numMaintenanceSelect.addEventListener('change', createMaintenanceForm);
    
    // Create a container div for the form
    const formContainer = document.createElement('div');
    formContainer.id = 'formContainer';
    
    // Function to create the maintenance form based on the selected number of actions
    function createMaintenanceForm() {
        const numActions = parseInt(numMaintenanceSelect.value);
        const time_horizon = 50;
        
        // Clear any previous form elements
        formContainer.innerHTML = '';
        
        for (let i = 0; i < numActions; i++) {
            const formGroup = document.createElement('div');
            
            // Create a time selection dropdown
            const timeSelect = document.createElement('select');
            timeSelect.id = "time-maintenance-" + (i+1);
            for (let j = 0; j < time_horizon; j++) {
                const timeOption = document.createElement("option");
                if (j == 0) {
                    timeOption.value = "";
                    timeOption.text = "Select time:";
                } else {
                    timeOption.value = j;
                    timeOption.text = j;
                }
                
                timeSelect.add(timeOption);
            }

            // Create an action selection dropdown
            const actionSelect = document.createElement('select');
            actionSelect.id = "maintenance-action-" + (i+1);
            const actionOption_ = document.createElement('option');
            actionOption_.value = "";
            actionOption_.textContent = "Select action:";
            actionSelect.appendChild(actionOption_);
            
            for (const option of maintenanceActions) {
                const actionOption = document.createElement('option');
                actionOption.value = option.name;
                actionOption.textContent = option.name;
                actionSelect.appendChild(actionOption);
            }
            
            formGroup.appendChild(timeSelect);
            //formGroup.appendChild(document.createElement('br'));
            formGroup.appendChild(actionSelect);
            formContainer.appendChild(formGroup);
            
        }
    }
    
    // Append elements to the infoDiv
    div.appendChild(formContainer);
    
    // Create and append a button to submit the form data
    const submitButton = document.createElement('button');
    submitButton.textContent = 'Submit Form';
    submitButton.addEventListener('click', postDataToServer);
    
    // Append the submit button to the infoDiv
    div.appendChild(submitButton);
    
    
    
}

// Function to send data to the server via a POST request
async function postDataToServer() {
    if (!roadSelected){
        return;
    }
    defaultChartMode(roadSelected);
    
    const numActions = parseInt(numMaintenanceSelect.value);

    // Create an array to store the form data
    let maintenanceData = {};
    
    for (let i = 0; i < numActions; i++) {
        
        const timeSelect = document.getElementById("time-maintenance-" + (i+1));
        const actionSelect = document.getElementById("maintenance-action-" + (i+1));

        // Get the selected time and action values
        const timeValue = timeSelect.value;
        const actionValue = actionSelect.value;

        // Push the data for each action to the maintenanceData
        maintenanceData[timeValue] = actionValue;
    }

    // Send the formData to the server via a POST request
    // Fetch request for prediction based on road properties
    
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    
    last_inspection = await convertLastInspection(roadSelected);
    
    raw = {}
    
    raw['prediction_settings'] = PREDICTION_SETTINGS;
    raw['prediction_thetas'] = PREDICTION_THETAS;
    raw['actions_effect'] = maintenanceActions;
    raw['action_schedule'] = maintenanceData;
    
    raw['initial_ICs'] = last_inspection;
    
    raw['road_properties'] = roadSelected;
    
    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify(raw),
      redirect: "follow"
    };
    
    const response = await fetch('/prediction', requestOptions);    
    
    const prediction = await response.json();
    
    setChartMaintenanceMode(roadSelected, prediction);
};

////////////////////////////////////////////////////////////////////
// OPTIMIZATION //
function addOptimizationFields(div, content={}) {   
    div.innerHTML = "";

    const resultSelection = document.createElement('div');
    resultSelection.id = 'result-selection';
    
    resultSelection.addEventListener('change', () => {
        const result = document.getElementById("individualResult");
        const label = result.options[result.selectedIndex].text;
        const perf = content.Performance[result.value];
        const cost = content.Cost[result.value];
        addNewPointGraph(perf, cost, label);
        
        changeActionsText(content.Actions_schedule[result.value]);
        
        const x = content.Markov[result.value].Time
        const y = content.Markov[result.value].IC
        plotOptimizationPrediction(x, y, label);
    });

    addResultFields(resultSelection, content);
    
    // Append elements to the infoDiv
    div.appendChild(resultSelection);
    
    /////////////////////////////////////////////////////////
    //Add new Graph to div
    const paretoChartWrapper = document.createElement('div');
    paretoChartWrapper.id = 'pareto-chart-wrapper';
    
    const paretoChart = document.createElement('canvas');
    paretoChart.id = 'pareto-chart';
    paretoChart.width = 450;
    paretoChart.height = 300;
    // paretoChart.width = width;
    
    paretoChartWrapper.appendChild(paretoChart);
    
    div.appendChild(paretoChartWrapper);
    /////////////////////////////////////////////////////////
    //Add text to write maintenance schedule
    const maintenanceSchedule = document.createElement('table');
    maintenanceSchedule.id = 'maintenance-schedule-text';
    
    div.appendChild(maintenanceSchedule);
}

function addResultFields(selectDiv, content) {
    try{content.Performance.length;}
    catch{return;};
    
	const result = document.createElement("select");
	result.name = "individualResult";
	result.id = "individualResult";
	
	const option_ = document.createElement("option");
	option_.value = 'Select maintenance schedule';
	option_.text = 'Select maintenance schedule';
	result.add(option_);
	
	for (let i = 0; i < content.Performance.length; i++) {
		const option1 = document.createElement("option");
		option1.value = i;
		option1.text = `Maintenance schedule ${i+1}`;
		result.add(option1);
	}
    selectDiv.appendChild(result);
}

function addNewPointGraph(x, y, label){
	new_chart = Chart.getChart('pareto-chart');
	
	// Get the chart data
	const chartData = new_chart.data;
	
	// Add a new dataset
		const selectedResult = {
		  type: 'scatter',
		  label: label,
		  data: [{	x: x,
					y: y
				}],
		  backgroundColor: 'rgba(0, 0, 0, 1)',
		  borderColor: 'rgba(0, 0, 0, 1)',
		  borderWidth: 4
		};
	
	if (chartData.datasets.length < 3){
		// Add the new dataset to the datasets array
		chartData.datasets.push(selectedResult);
	}
	else {
		// Remove the last dataset to the datasets array
		chartData.datasets.pop();
		// Add the new dataset to the datasets array
		chartData.datasets.push(selectedResult);
	}
	// Update the chart
		new_chart.update();
};

function changeActionsText(result){
	const actions_text = document.getElementById("maintenance-schedule-text");
    
    actions_text.innerHTML = `
        <tr>
            <th colspan="2">Maintenance Schedule</th>
        </tr>
        <tr>
            <th>Time</th>
            <th>Action</th>
        </tr>
        `
    
    // Iterate through the data and create table rows and cells
    for (const time in result) {
        const action = result[time];
        const row = actions_text.insertRow();
        
        // Create table cells for "Time" and "Action"
        const timeCell = row.insertCell(0);
        timeCell.textContent = time;
        
        const actionCell = row.insertCell(1);
        actionCell.textContent = action;
    }
    
	// actions_text.innerHTML = `Actions = ${JSON.stringify(result)}`;
    
        
	
}

function plotOptimizationPrediction(x, y, label) {	
	createChart('performanceChart', x, y, 'Time', 'IC', label);
};

////////////////////////////////////////////////////////////////////

function setChart(road) {
    console.log(`DEBUGGING - setChart - ${road['Section_Name']}`);
    performance_indicators.innerHTML = "";
    
    const mapModeToChart = {'visualize': setChartVizualizeMode,
                         'prediction': setChartPredictionMode,
                         'maintenance': defaultChartMode,
                         'optimization': setChartOptimizationMode
                         };
    mode = getCurrentMode();
    
    mapModeToChart[mode](road);
    
}

function defaultChartMode(road){
    console.log(`DEBUGGING - defaultChartMode - ${road['Section_Name']}`);
    performance_indicators.innerHTML = "";
    createChart('performanceChart', [], [], 'Year', '', road['Section_Name']);
}

function setChartVizualizeMode(road) {
    console.log(`DEBUGGING - setChartVizualizeMode - ${road['Section_Name']}`);
    performance_indicators.innerHTML = "";
    createChart('performanceChart', [], [], 'Year', '', road['Section_Name']);
    
    EDP_PI_List = ['EDP', 'PI'];
    
    EDPList = ['Cracking', 'Surface_Defects', 'Transverse_Evenness', 'Longitudinal_Evenness', 'Skid_Resistance', 
              //'Macro_Texture', 'Bearing_Capacity'
              ];
    PIList = ['123', '123', '423'];
    
    PIList = ['Cracking_ASFiNAG', 'Surface_Defects_ASFiNAG', 'Transverse_Evenness_ASFiNAG', 'Longitudinal_Evenness_ASFiNAG', 'Skid_Resistance_ASFiNAG', 'Bearing_Capacity_ASFiNAG',
              'Safety_ASFiNAG',	'Comfort_ASFiNAG',	'Functional_ASFiNAG', 'Surface_Structural_ASFiNAG', 'Structural_ASFiNAG', 'Global_ASFiNAG'
              ];
    
    // Create a selection which the user can select if he wants to see the EDP or transformed indicators.
    const EDP_PI = document.createElement("select");
    EDP_PI.name = "EDP_PI";
    EDP_PI.id = "EDP_PI";
    
    const option_1 = document.createElement("option");
    option_1.value = 'Select';
    option_1.text = 'Select';
    EDP_PI.add(option_1);
    
    for (let i = 0; i < EDP_PI_List.length; i++) {
        const option1 = document.createElement("option");
        option1.value = EDP_PI_List[i];
        option1.text = EDP_PI_List[i];
        EDP_PI.add(option1);
        performance_indicators.appendChild(EDP_PI);
    }
    
    // based on the selection of the user, shows the EDP or PI list
    EDP_PI.addEventListener('change', () => {
        console.log(`DEBUGGING - change_EDP_PI - ${document.getElementById("EDP_PI").value}`);
        
        if (performance_indicators.childElementCount > 1) {
            performance_indicators.removeChild(performance_indicators.lastChild);
        }
        
        const indicator = document.createElement("select");
        indicator.name = "indicator";
        indicator.id = "indicator";
        
        const option_ = document.createElement("option");
        option_.value = 'Select indicator';
        option_.text = 'Select indicator';
        indicator.add(option_);
        
        let lista = []
        
        if (document.getElementById("EDP_PI").value == 'EDP') {
            lista = EDPList;
        };
        
        if (document.getElementById("EDP_PI").value == 'PI') {
            lista = PIList;
        };
        
        for (let i = 0; i < lista.length; i++) {
            const option1 = document.createElement("option");
            option1.value = lista[i];
            option1.text = lista[i];
            indicator.add(option1);
            performance_indicators.appendChild(indicator);
        }
        indicator.addEventListener('change', () => {
            console.log(`DEBUGGING - change_PI - ${document.getElementById("indicator").value}`);
            
            const performance_indicator = document.getElementById("indicator").value;
            
            let dates =  road['inspections'].map(obj => obj.Date)//.map(date => new Date(date));
            let performance =  road['inspections'].map(obj => obj[performance_indicator]);
            
            createChart('performanceChart', dates, performance, 'Year', performance_indicator, road['Section_Name']);
        });
    });
};


async function convertLastInspection(road) {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    
    raw = {}
    
    raw["institution"] = "ASFiNAG";
    raw["road_sections"] = [road];
    
    const requestConvertOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify(raw),
      redirect: "follow"
    };
    
    const response_con = await fetch('/convert', requestConvertOptions);
    const converted = await response_con.json();
    const last_inspection = converted[0]['inspections'][converted[0]['inspections'].length - 1];
    
    // Filter to only include properties with '_ASFiNAG'
    const filteredData = Object.keys(last_inspection)
        .filter(key => key.includes('_ASFiNAG'))
        .reduce((obj, key) => {
            const newKey = key.replace('_ASFiNAG', '');
            obj[newKey] = last_inspection[key];
            return obj;
        }, {});
        
    filteredData["date"] = last_inspection["Date"];
    
    return filteredData
};

async function setChartPredictionMode(road) {  
    console.log(`DEBUGGING - setChartPredictionMode - ${road['Section_Name']}`);
    
    createChart('performanceChart', [], [], 'Year', '', road['Section_Name']);
    
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    
    last_inspection = await convertLastInspection(road);
    
    raw = {}
    
    raw['prediction_settings'] = PREDICTION_SETTINGS;
    raw['prediction_thetas'] = PREDICTION_THETAS;
    raw['initial_ICs'] = last_inspection;
    
    raw['road_properties'] = road;
    
    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: JSON.stringify(raw),
      redirect: "follow"
    };
    
    const response = await fetch('/prediction', requestOptions);
    
    const prediction = await response.json();
              
    PIList = Object.keys(prediction)
    
    // Create a selection which the user can select if he wants to see the EDP or transformed indicators.
    const indicator = document.createElement("select");
    indicator.name = "indicator";
    indicator.id = "indicator";
    
    const option_1 = document.createElement("option");
    option_1.value = 'Select PI';
    option_1.text = 'Select PI';
    indicator.add(option_1);
    
    for (let i = 0; i < PIList.length; i++) {
        const option1 = document.createElement("option");
        option1.value = PIList[i];
        option1.text = PIList[i];
        indicator.add(option1);
        performance_indicators.appendChild(indicator);
    }
    
    date = road.inspections[road.inspections.length - 1].Date.split('/');
    year = date[2];
    
    indicator.addEventListener('change', () => {
        const performance_indicator = document.getElementById("indicator").value;
        
        let performance =  prediction[performance_indicator]
        
        // Use a loop to add the constant value to each element
        const new_dates = [];
        for (let i = 0; i < performance.length; i++) {
            new_dates.push(i + parseInt(year));
        }

        createChart('performanceChart', new_dates, performance, 'Year', performance_indicator, road['Section_Name']);
    });
};

function setChartMaintenanceMode(road, prediction) {
    console.log(`DEBUGGING - setChartMaintenanceMode - ${road['Section_Name']}`);
    performance_indicators.innerHTML = "";
    PIList = Object.keys(prediction)
    
    // Create a selection which the user can select if he wants to see the EDP or transformed indicators.
    const indicator = document.createElement("select");
    indicator.name = "indicator";
    indicator.id = "indicator";
    
    const option_1 = document.createElement("option");
    option_1.value = 'Select PI';
    option_1.text = 'Select PI';
    indicator.add(option_1);
    
    for (let i = 0; i < PIList.length; i++) {
        const option1 = document.createElement("option");
        option1.value = PIList[i];
        option1.text = PIList[i];
        indicator.add(option1);
        performance_indicators.appendChild(indicator);
    }
    
    date = road.inspections[road.inspections.length - 1].Date.split('/');
    year = date[2];
    
    performance_indicators.addEventListener('change', () => {
        const performance_indicator = document.getElementById("indicator").value;
        
        let performance =  prediction[performance_indicator];
        
        // Use a loop to add the constant value to each element
        const new_dates = [];
        for (let i = 0; i < performance.length; i++) {
            new_dates.push(i + parseInt(year));
        }

        createChart('performanceChart', new_dates, performance, 'Year', performance_indicator, road['Section_Name']);
    });
};

function setChartOptimizationMode(road) {  
    
    data = road.optimization;
    
    addOptimizationFields(infoDiv, data)
    
    var data_x_y = [];

    for (var i = 0; i < data.Performance.length; i++) {
        data_x_y.push({ 'x': data.Performance[i], 'y': data.Cost[i] });
    }
    
    const ctx = document.getElementById('pareto-chart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
          // labels: data_x,
          datasets: [{
            label: 'Pareto curve',
            data: data_x_y,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            x: {
              type: 'linear',
              title: {
                display: true,
                text: 'Area under curve',
              }
            },
            y: {
              type: 'linear',
              title: {
                display: true,
                text: 'Cost',
              }
            },
          },
          //maintainAspectRatio: false
        }
    });
    
    plotDummies(data.Dummies)

};

function plotDummies(dummies){
	new_chart = Chart.getChart('pareto-chart');
	
	// Get the chart data
	const chartData = new_chart.data;
	
	// Convert to data array
    var data = [];
    for (let i = 0; i < dummies.Performance.length; i++) {
      data.push({ x: dummies.Performance[i], y: dummies.Cost[i] });
    }
	
	// Add a new dataset
		const result = {
		  type: 'scatter',
		  label: 'Dummies',
		  data: data,
		  backgroundColor: 'rgba(220,220,220, 0.5)',
		  borderColor: 'rgba(220,220,220, 0.5)',
		  borderWidth: 3
		};
	
    if (chartData.datasets.length > 1){
        chartData.datasets.pop();
    }
	chartData.datasets.push(result);
    
	// Update the chart
	new_chart.update();
};