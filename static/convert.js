const runBtn = document.getElementById('runBtn');
const inspectionsFile = document.getElementById('inspectionsFile');
const propertiesFile = document.getElementById('propertiesFile');
const assetsProperty = document.getElementById('assets');

let convertedInspections = ''



function addSelectFields(content) {
	const assets = document.getElementById("assets");
	assets.innerHTML = ""
	const institution = document.getElementById('institution').value;
	let uniqueNames = []
	
	if (institution === 'Generic') {
		uniqueNames = [...new Set(content.map(item => item.Nome))];
	};
	if (institution === 'ASFiNAG') {
		uniqueNames = [...new Set(content.map(item => item['Section_Name']))];
	}
	const asset = document.createElement("select");
	asset.name = "asset";
	asset.id = "asset";
	const option_ = document.createElement("option");
	option_.value = 'Select asset';
	option_.text = 'Select asset';
	asset.add(option_);
	for (let i = 0; i < uniqueNames.length; i++) {
		const option1 = document.createElement("option");
		option1.value = uniqueNames[i];
		option1.text = uniqueNames[i];
		asset.add(option1);
		assets.appendChild(asset);
	}
	if (institution === 'ASFiNAG') {
		indicatorsList = ['Cracking_ASFiNAG', 'Surface_Defects_ASFiNAG', 'Transverse_Evenness_ASFiNAG', 'Longitudinal_Evenness_ASFiNAG', 
		                  'Skid_Resistance_ASFiNAG', 'Macro_Texture_ASFiNAG', 'Bearing_Capacity_ASFiNAG']
		const indicator = document.createElement("select");
		indicator.name = "indicator";
		indicator.id = "indicator";
		const option_ = document.createElement("option");
		option_.value = 'Select indicator';
		option_.text = 'Select indicator';
		indicator.add(option_);
		for (let i = 0; i < indicatorsList.length; i++) {
			const option1 = document.createElement("option");
			option1.value = indicatorsList[i];
			option1.text = indicatorsList[i];
			indicator.add(option1);
			assets.appendChild(indicator);
		}
	}
}

assetsProperty.addEventListener('change', () => {
	const asset = document.getElementById("asset").value;
	const institution = document.getElementById('institution').value;
	
	let dataFiltered = []
	let dates = []
	let EC = []
	let y_label = 'EC'
	if (institution === 'Generic') {
		dataFiltered = convertedInspections.filter(obj => obj['Nome'] === asset);
	}
	if (institution === 'ASFiNAG') {
		dataFiltered = convertedInspections.filter(obj => obj['Section_Name'] === asset);
	}
	if (institution === 'Generic') {
		const dateStrings = dataFiltered.map(obj => obj['Data']);
		dates = dateStrings.map(dateString => {
			const parts = dateString.split('-');
			const date = parts[2]
			return date;
		}).map(Number);
		EC = dataFiltered.map(obj => obj['EC']).map(Number);
	}
	if (institution === 'ASFiNAG') {
		const indicator = document.getElementById("indicator").value;
		dates = dataFiltered.map(obj => obj['Date']).map(Number);
		EC = dataFiltered.map(obj => obj[indicator]).map(Number);
		y_label = indicator
	}
	createChart('myChart', dates, EC, 'Year', y_label, asset);
});


runBtn.addEventListener('click', () => {
	const formData = new FormData();
	formData.append('inspectionsFile', inspectionsFile.files[0]);
	formData.append('propertiesFile', propertiesFile.files[0]);
	const institution = document.getElementById('institution').value;
	formData.append('institution', JSON.stringify(institution));

	fetch(window.location.pathname, {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		convertedInspections = data
		addSelectFields(convertedInspections)
	})
	.catch(error => console.error(error));
});


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