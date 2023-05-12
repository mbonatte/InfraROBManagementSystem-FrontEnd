const maintenanceFile = document.getElementById('maintenanceFile');
let maintenanceActions = ''


maintenanceFile.addEventListener('change', (event) => {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.readAsText(file);
  reader.onload = () => {
    const content = JSON.parse(reader.result);
    maintenanceActions = content;
  };
});



function addSelectFields() {
  const numMaintenance = document.getElementById("number-maintenance").value;
  const maintenance_scenarios = document.getElementById("maintenance-scenarios");
  const time_horizon = parseInt(document.getElementById('time-horizon').value);
  
  maintenance_scenarios.innerHTML = ""; // Clear any previously added fields
  
  for (let i = 0; i < numMaintenance; i++) {
	const scenario = document.createElement("div");
    scenario.name = "scenario-maintenance-" + (i+1);
    scenario.id = "scenario-maintenance-" + (i+1);
	  
    const maintenance_action = document.createElement("select");
    maintenance_action.name = "maintenance-action-" + (i+1);
    maintenance_action.id = "maintenance-action-" + (i+1);
	
	const time_maintenance = document.createElement("select");
    time_maintenance.name = "time-maintenance-" + (i+1);
    time_maintenance.id = "time-maintenance-" + (i+1);
	
    const option1 = document.createElement("option");
    option1.value = "";
    option1.text = "Select time:";
	time_maintenance.add(option1);
	
	const option3 = document.createElement("option");
    option3.value = "";
    option3.text = "Select action:";
	maintenance_action.add(option3);
	
	for (let j = 0; j < time_horizon; j++) {
		const option_ = document.createElement("option");
		option_.value = (j+1);
		option_.text = (j+1);
		time_maintenance.add(option_);
	}
	
	for (let j = 0; j < maintenanceActions.length; j++) {
		const option_ = document.createElement("option");
		option_.value = maintenanceActions[j].name;
		option_.text = maintenanceActions[j].name;
		maintenance_action.add(option_);
	}
	
	scenario.appendChild(time_maintenance);
	scenario.appendChild(maintenance_action);
    maintenance_scenarios.appendChild(scenario);
  }
}

function getMaintenanceScenario(){
	const numMaintenance = document.getElementById("number-maintenance").value;
	var scenario = {}
	for (let i = 0; i < numMaintenance; i++) {
		const time = document.getElementById("time-maintenance-" + (i+1)).value;
		const action = document.getElementById("maintenance-action-" + (i+1)).value;
		if (time !== '' && action !== ''){
			scenario[time] = action;
		}
	}
	return scenario
}