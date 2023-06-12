const runBtn = document.getElementById('runBtn');
const inspectionsFile = document.getElementById('inspectionsFile');
const propertiesFile = document.getElementById('propertiesFile');
const responseDiv = document.getElementById('response');
let markovResponse = ''

institution.addEventListener('change', function() {
	const worst_best_IC_div = document.getElementById('worst-best-IC-div');
	const importContent = document.getElementById('importContent');
	const divProperties = document.getElementById('divProperties');
	
	importContent.innerHTML = "Import inpections";
	worst_best_IC_div.style.display = 'none';
	divProperties.style.display = 'none';
	
	if (this.value === 'Generic') {
		worst_best_IC_div.style.display = 'block';
	}
	else {
		importContent.innerHTML = "Import inpections and properties";
		divProperties.style.display = 'block';
	}
});

function getWorstBestIC(){
	const institution = document.getElementById('institution').value;
	if (institution === 'ASFiNAG') {
		return {worst_IC: 5,
				best_IC: 1
				}
	}
	if (institution === 'COST_354') {
		return {worst_IC: 5,
				best_IC: 1
				}
	}
	if (institution === 'Generic') {
		const worst = document.getElementById('worst-IC');
		const best = document.getElementById('best-IC');
		return {worst_IC: parseInt(worst.value),
				best_IC: parseInt(best.value)
				}
	}
}


runBtn.addEventListener('click', () => {
	const result_id = Math.random().toString(36).substr(2, 8);
	const formData = new FormData();
	const institution = document.getElementById('institution').value;
	const time_block = document.getElementById('time-block').value
	const time_horizon = parseInt(document.getElementById('time-horizon').value)
	formData.append('inspectionsFile', inspectionsFile.files[0]);
	if (institution === 'ASFiNAG'){
		formData.append('propertiesFile', propertiesFile.files[0]);
	}
	formData.append('institution', JSON.stringify(institution));
	formData.append('worst_best_IC', JSON.stringify(getWorstBestIC()));
	formData.append('time_block', JSON.stringify(time_block));
	formData.append('time_horizon', JSON.stringify(time_horizon));
	
	if (window.location.pathname === '/maintenance'){
		const maintenanceFile = document.getElementById('maintenanceFile');
		formData.append('maintenanceFile', maintenanceFile.files[0]);
		formData.append('maintenanceScenario', JSON.stringify(getMaintenanceScenario()));
	}
	
	if (window.location.pathname === '/optimization'){
		const maintenanceFile = document.getElementById('maintenanceFile');
		formData.append('maintenanceFile', maintenanceFile.files[0]);
		changeDivResponse(result_id)
		formData.append('result_id', JSON.stringify(result_id));
	}

	fetch(window.location.pathname, {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
	// Display the JSON response in the result div
	markovResponse = data
	if (window.location.pathname !== '/optimization'){
		if (institution !== 'ASFiNAG'){
			createChart('myChart', data.Year, data.IC, time_block, 'IC', 'Markov prediction');
		}
		else {
			addSelectFields(data);
		}
	}
	else {
		createChart('myChart', data.Performance, data.Cost, 'Performance', 'Cost', `Pareto curve - ${result_id}`);
	}
	})
	.catch(error => console.error(error));
});


function changeDivResponse(result_id){
	warning = "This request my take several minutes.<br> ";
	warning = warning + "In case you do not want to wait, please use the following hash to access the result when it's done.<br>";
	warning = warning + `HASH = <b>${result_id}</b>`
	responseDiv.innerHTML = warning
};

function createChart(canvas_name, data_x, data_y, x_label, y_label, data_title) {
	// Create a Chart.js chart
	let myChart = Chart.getChart(canvas_name);
	if (myChart) {
		// If the chart already exists, update it with new data
		myChart.data.labels = data_x;
		myChart.data.datasets[0].data = data_y;
		myChart.data.datasets[0].label = data_title;
		myChart.options.scales.y.title.text = y_label;
		myChart.update();
	} else {
		// If the chart doesn't exist, create a new one
		const ctx = document.getElementById(canvas_name).getContext('2d');
		const myChart = new Chart(ctx, {
			type: 'line',
			data: {
			  labels: data_x,
			  datasets: [{
				label: data_title,
				data: data_y,
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
					text: x_label,
				  }
				},
				y: {
				  type: 'linear',
				  title: {
					display: true,
					text: y_label,
				  }
				},
			  },
			  //maintainAspectRatio: false
			}
		}
	)};
}

function addSelectFields(content) {
	const response = document.getElementById("response");
	response.innerHTML = "";
	
	uniqueNames = Object.keys(content);
	const indicator = document.createElement("select");
	indicator.name = "indicator";
	indicator.id = "indicator";
	
	const option_ = document.createElement("option");
	option_.value = 'Select indicator';
	option_.text = 'Select indicator';
	
	indicator.add(option_);
	for (let i = 0; i < uniqueNames.length; i++) {
		const option1 = document.createElement("option");
		option1.value = uniqueNames[i];
		option1.text = uniqueNames[i];
		indicator.add(option1);
		response.appendChild(indicator);
	}
}

responseDiv.addEventListener('change', () => {
	const indicator = document.getElementById("indicator").value;
	createChart('myChart', markovResponse[indicator].Time, markovResponse[indicator].IC, 'Year', 'IC', indicator);
});