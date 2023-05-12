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
	const asfinag_download_div = document.getElementById('asfinag-download-div');
	
	worst_best_IC_div.style.display = 'none';
	asfinag_download_div.style.display = 'none';
	if (this.value === 'Generic') {
		worst_best_IC_div.style.display = 'block';
	}
	else if (this.value === 'ASFiNAG') {
		asfinag_download_div.style.display = 'block';		
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
	}

	fetch(window.location.pathname, {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
	// Display the JSON response in the result div
	//responseDiv.innerHTML = JSON.stringify(data);
	console.log(JSON.stringify(data))
	createChart(data);
	})
	.catch(error => console.error(error));
});


function createChart(data) {
	// Create a Chart.js chart
	let myChart = Chart.getChart('myChart');
	if (myChart) {
		// If the chart already exists, update it with new data
		myChart.data.labels = data.Year;
		myChart.data.datasets[0].data = data.IC;
		myChart.update();
	} else {
		// If the chart doesn't exist, create a new one
		const ctx = document.getElementById('myChart').getContext('2d');
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