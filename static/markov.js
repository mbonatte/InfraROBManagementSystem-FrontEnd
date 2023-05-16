const runBtn = document.getElementById('runBtn');
const inspectionsFile = document.getElementById('inspectionsFile');
const responseDiv = document.getElementById('response');
const institution = document.getElementById('institution');

function getInstitution(){
	return institution.value
}

function getTimeBlock(){
	return document.getElementById('time-block').value
}

function getTimeHorizon(){
	return parseInt(document.getElementById('time-horizon').value)
}

institution.addEventListener('change', function() {
	const worst_best_IC_div = document.getElementById('worst-best-IC-div');
	worst_best_IC_div.style.display = 'none';
	if (this.value === 'Generic') {
		worst_best_IC_div.style.display = 'block';
	}
});

function getWorstBestIC(){
	const institution = getInstitution();
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
	formData.append('inspectionsFile', inspectionsFile.files[0]);
	formData.append('worst_best_IC', JSON.stringify(getWorstBestIC()));
	formData.append('time_block', JSON.stringify(getTimeBlock()));
	formData.append('time_horizon', JSON.stringify(getTimeHorizon()));
	
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
	console.log(JSON.stringify(data))
	if (window.location.pathname !== '/optimization'){
		createChart('myChart', data.Year, data.IC, getTimeBlock(), 'IC', 'Markov prediction');
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
				  title: {
					display: true,
					text: x_label,
				  }
				},
				y: {
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