const resultSelection = document.getElementById('result-selection');
let results = ''

function plotGraphByHash() {
  document.getElementById('result-warning').innerHTML = '';
  const result_id = document.getElementById("hash").value;
  fetch(`/get_optimization_result?result_id=${result_id}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
	  if (data.hasOwnProperty('error')) {
		  throw Error(response.statusText);
        }
	  results = data
	  createChart('newChart', data.Performance, data.Cost, 'Area under curve', 'Cost', `Pareto curve - ${result_id}`);
	  addResultFields(data);
    })
    .catch((error) => {
		console.log(error)
	  changeDivWarning(result_id);
    });
}

function changeDivWarning(result_id){
	const warningDiv = document.getElementById('result-warning');
	warning = "It was not possible to find the result, please check the spelling.<br>";
	warning = warning + `HASH = <b>${result_id}</b>`
	warningDiv.innerHTML = warning
};

function addResultFields(content) {
	const results = document.getElementById("result-selection");
	results.innerHTML = ""
	
	const result = document.createElement("select");
	result.name = "result";
	result.id = "result";
	
	const option_ = document.createElement("option");
	option_.value = 'Select result';
	option_.text = 'Select result';
	result.add(option_);
	
	for (let i = 0; i < content.Performance.length; i++) {
		const option1 = document.createElement("option");
		option1.value = i;
		option1.text = `Result ${i+1}`;
		result.add(option1);
		results.appendChild(result);
	}
}

resultSelection.addEventListener('change', () => {
	const result = document.getElementById("result")
	if (result.value !== 'Select result'){
		addNewPointGraph(result);
		changeActionsText(result);
		addNewGraph(result);
		
	};
});

function addNewPointGraph(result){
	new_chart = Chart.getChart(newChart);
	
	// Get the chart data
	const chartData = new_chart.data;
	
	// Add a new dataset
		const selectedResult = {
		  type: 'scatter',
		  label: result.options[result.selectedIndex].text,
		  data: [{	x: results.Performance[result.value],
					y: results.Cost[result.value]
				}],
		  backgroundColor: 'rgba(0, 0, 0, 1)',
		  borderColor: 'rgba(0, 0, 0, 1)',
		  borderWidth: 4
		};
	
	if (chartData.datasets.length < 2){
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
	const actions_text = document.getElementById("actions-text");
	actions_text.innerHTML = `Actions = ${JSON.stringify(results.Actions_schedule[result.value])}`;
	
}


function addNewGraph(resut) {
	
	x = results.Markov[result.value].Time
	y = results.Markov[result.value].IC
	
	createChart('performanceChart', x, y, 'Time', 'IC', result.options[result.selectedIndex].text);
};