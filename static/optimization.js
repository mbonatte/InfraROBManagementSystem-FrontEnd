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

function sendHash() {
  const result_id = document.getElementById("hash").value;
  fetch(`/get_optimization_result?result_id=${result_id}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
	  createNewChart(data);
    })
    .catch((error) => {
      console.error(error);
    });
}

function createNewChart(data) {
	// Create a Chart.js chart
	let myChart = Chart.getChart('newChart');
	if (myChart) {
		// If the chart already exists, update it with new data
		myChart.data.labels = data.Year;
		myChart.data.datasets[0].data = data.IC;
		myChart.update();
	} else {
		// If the chart doesn't exist, create a new one
		const ctx = document.getElementById('newChart').getContext('2d');
		const myChart = new Chart(ctx, {
			type: 'line',
			data: {
			  labels: data.Year,
			  datasets: [{
				label: 'Markov prediction',
				data: data.IC,
				backgroundColor: 'rgba(255, 99, 132, 0.2)',
				borderColor: 'rgba(255, 99, 132, 1)',
				borderWidth: 1
			  }]
			},
			options: {
			  responsive: true,
			  scales: {
				x: {
				  title: {
					display: true,
					text: getTimeBlock(),
				  }
				},
				y: {
				  title: {
					display: true,
					text: 'IC',
				  }
				},
			  },
			  //maintainAspectRatio: false
			}
		}
	)};
}
