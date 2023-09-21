// modes.js

// JavaScript for mode switching
const current_mode = document.getElementById('current-mode');

const visualizeModeIcon = document.getElementById('visualize-mode');
const predictionModeIcon = document.getElementById('prediction-mode');
const maintenanceModeIcon = document.getElementById('maintenance-mode');
const optimizationModeIcon = document.getElementById('optimization-mode');


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

function setChart(road) {
    performance_indicators.innerHTML = "";
    createChart('performanceChart', [], [], 'Year', '', road['Section_Name']);
    
    const mapModeToChart = {'visualize': setChartVizualizeMode,
                         'prediction': setChartPredictionMode,
                         'maintenance': setChartVizualizeMode,
                         'optimization': setChartVizualizeMode
                         };
    
    mode = current_mode.innerHTML.split(' ')[2].split('<')[0];
    mapModeToChart[mode](road);
    
}

function setChartVizualizeMode(road) {
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
    });

    performance_indicators.addEventListener('change', () => {
        const performance_indicator = document.getElementById("indicator").value;
        
        let dates =  road['inspections'].map(obj => obj.Date)//.map(date => new Date(date));
        let performance =  road['inspections'].map(obj => obj[performance_indicator]);
        
        createChart('performanceChart', dates, performance, 'Year', performance_indicator, road['Section_Name']);
    });
};

async function setChartPredictionMode(road) {    
    // Fetch request for prediction based on road properties
	const formData = new FormData();
    formData.append('road', JSON.stringify(road));
    const response = await fetch('/markov/road', {method: 'POST',
                                                        body: formData});
    const prediction = await response.json();
              
    PIList = Object.keys(prediction)
    
    // Create a selection which the user can select if he wants to see the EDP or transformed indicators.
    const indicator = document.createElement("select");
    indicator.name = "indicator";
    indicator.id = "indicator";
    
    const option_1 = document.createElement("option");
    option_1.value = 'Select';
    option_1.text = 'Select';
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
        
        let dates =  prediction[performance_indicator]['Time'];
        let performance =  prediction[performance_indicator]['IC']
        
        // Use a loop to add the constant value to each element
        const new_dates = [];
        for (let i = 0; i < dates.length; i++) {
            new_dates.push(parseInt(dates[i]) + parseInt(year));
        }
        console.log(prediction[performance_indicator])
        createChart('performanceChart', new_dates, performance, 'Year', performance_indicator, road['Section_Name']);
    });
};


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
    
    // Function to send data to the server via a POST request
    function postDataToServer() {
        const numActions = parseInt(numMaintenanceSelect.value);

        // Create an array to store the form data
        const formData = {};

        for (let i = 0; i < numActions; i++) {
            const timeSelect = document.querySelector(`#timeSelect${i}`);
            const actionSelect = document.querySelector(`#actionSelect${i}`);

            // Get the selected time and action values
            const timeValue = timeSelect.value;
            const actionValue = actionSelect.value;

            // Push the data for each action to the formData array
            formData[time] = actionValue;
        }

        // Send the formData to the server via a POST request (you need to implement this part)
        // Example of a POST request using the fetch API:
        // fetch('/your-server-endpoint', {
            // method: 'POST',
            // headers: {
                // 'Content-Type': 'application/json',
            // },
            // body: JSON.stringify(formData), // Send the form data as JSON
        // })
        // .then(response => response.json()) // Process the server response if needed
        // .then(data => {
            // // Handle the response data from the server
            // console.log(data);
        // })
        // .catch(error => {
            // // Handle any errors that occurred during the fetch request
            // console.error('Error:', error);
        // });
    }
    
}