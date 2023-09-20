// map.js

// The roads variable is passed from Flask

const canvas = document.getElementById('map_canvas');
const context = canvas.getContext('2d');
const infoDiv = document.getElementById('road_info');
const showNamesCheckbox = document.getElementById('show-section-names');
const showGradesCheckbox = document.getElementById('show-grades');
const performance_indicators = document.getElementById("performance_indicators");


// Call the function to draw roads when the page loads
window.addEventListener('load', drawRoads);
window.addEventListener('load', displayRoadInfo);
createChart('performanceChart', [], [], 'Year', '', '');

// Event listener for the "Show Names" checkbox
showNamesCheckbox.addEventListener('change', drawRoads);

// Event listener for the "Show Grades" checkbox
showGradesCheckbox.addEventListener('change', function () {
    drawRoads();
    
    const legendNoFOS = document.getElementById('legend-no-fos');
    const legendGradeScale = document.getElementById('legend-grade-scale');

    if (showGradesCheckbox.checked) {
        // If checkbox is checked, show the grade scale legend and hide the No FOS legend
        legendNoFOS.style.display = 'none';
        legendGradeScale.style.display = 'block';
    } else {
        // If checkbox is unchecked, show the No FOS legend and hide the grade scale legend
        legendNoFOS.style.display = 'block';
        legendGradeScale.style.display = 'none';
    }
});


// Function to check if a point (x, y) is close to a line segment defined by (x1, y1) and (x2, y2)
function isPointNearLine(x, y, x1, y1, x2, y2, tolerance = 5) {
    const length = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
    if (length === 0) return false;

    const t = ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / (length ** 2);

    if (t < 0) return false; // Closest point is before the start of the segment
    if (t > 1) return false; // Closest point is after the end of the segment

    const closestX = x1 + t * (x2 - x1);
    const closestY = y1 + t * (y2 - y1);

    const distance = Math.sqrt((x - closestX) ** 2 + (y - closestY) ** 2);

    return distance <= tolerance;
}

// Function to display road information in a table within the infoDiv
function displayRoadInfo(road) {
    const table = document.createElement('table');
    
    let last_inspection = {}
    if (Array.isArray(road['inspections'])) {
        last_inspection = road['inspections'].slice(-1)[0];
    };

    table.innerHTML = `
        <tr>
            <th colspan="2">${road.Section_Name}</th>
        </tr>
        <tr>
            <th colspan="2">Properties</th>
        </tr>
        <tr>
            <th>Property</th>
            <th>Value</th>
        </tr>
        <tr>
            <td>hasFOS</td>
            <td>${road.hasFOS}</td>
        </tr>
        <tr>
            <td>Category</td>
            <td>${road.Road_Category}</td>
        </tr>
        <tr>
            <td>Construction type</td>
            <td>${road.Construction_Type}</td>
        </tr>
        <tr>
            <th colspan="2">Condition</th>
        </tr>
        <tr>
            <td>Date</td>
            <td>${last_inspection.Date}</td>
        </tr>
        <tr>
            <td>Grade</td>
            <td>${last_inspection.Global_ASFiNAG}</td>
        </tr>`;
        
    // Clear previous content and append the table to the infoDiv
    infoDiv.innerHTML = '';
    infoDiv.appendChild(table);
}

// Function to highlight the selected road
function highlightSelectedRoad(road) {
    context.clearRect(0, 0, canvas.width, canvas.height);
    drawRoads(); // Redraw all roads
    context.strokeStyle = 'cyan';
    context.lineWidth = road.category === 'primary' ? 5 : 4; // Adjust line width for highlight
    context.beginPath();
    context.moveTo(road.xi * 50, road.yi * 50);
    context.lineTo(road.xf * 50, road.yf * 50);
    context.stroke();
}

// Function to handle canvas click event
canvas.addEventListener('click', (e) => {
    const mouseX = e.clientX - canvas.getBoundingClientRect().left;
    const mouseY = e.clientY - canvas.getBoundingClientRect().top;

    // Check if the click point is near any road
    for (const road of roads) {
        if (isPointNearLine(mouseX, mouseY, road.xi * 50, road.yi * 50, road.xf * 50, road.yf * 50, 10)) {
            // Highlight the selected road
            highlightSelectedRoad(road)
            
            // Display the road information
            displayRoadInfo(road); 
            
            // Set the chart for the road
            setChart(road);
            
            break; // Stop checking if a road is found
        }
    }
});

// Function to set the road color based on the grade
function setRoadColorByGrade(context, road) {
    const grade = road['inspections'].slice(-1)[0].Global_ASFiNAG;
    switch (grade) {
        case 1:
            context.strokeStyle = 'green';
            break;
        case 2:
            context.strokeStyle = '#9ACD32';
            break;
        case 3:
            context.strokeStyle = 'yellow';
            break;
        case 4:
            context.strokeStyle = 'orange';
            break;
        case 5:
            context.strokeStyle = 'red';
            break;
        default:
            break;
    }
}

//function to display the names of the roads on canvas
function displayRoadsNames (context, road){
    context.save();
        
    // Calculate the angle of the line
    const angle = Math.atan2((road.yf - road.yi) * 50, (road.xf - road.xi) * 50);
    
    context.translate((road.xi + road.xf) * 50 / 2, (road.yi + road.yf) * 50 / 2);
    context.rotate(angle);
    
    // Add road names as text labels aligned with the lines
    context.fillStyle = 'black';
    context.font = '10px Arial';
    context.textAlign = 'center';
    
    // Calculate the text position along the line
    const textX = 0//(road.xi * 50 + road.xf * 50) / 2 + Math.cos(angle) * 15; // Offset by 15 pixels along the line
    const textY = 0//(road.yi * 50 + road.yf * 50) / 2 + Math.sin(angle) * 15; // Offset by 15 pixels along the line
    
    context.fillText(road.Section_Name, 0, 10);
    
    context.restore();
}

// Function to draw roads on the canvas
function drawRoads() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    roads.forEach((road, index) => {
        context.strokeStyle = road.hasFOS ? 'gray' : 'black';
        
        // Set road color based on grade using the setRoadColorByGrade function
        if (showGradesCheckbox.checked) {
            setRoadColorByGrade(context, road);
        };
        
        context.lineWidth = road.Road_Category === 'primary' ? 5 : 2;
        context.beginPath();
        context.moveTo(road.xi * 50, road.yi * 50);
        context.lineTo(road.xf * 50, road.yf * 50);
        context.stroke();
        
        // Draw dots at the beginning and end
        const dotRadius = 5;
        context.fillStyle = 'black'; // Dot color
        context.beginPath();
        context.arc(road.xi * 50, road.yi * 50, dotRadius, 0, Math.PI * 2);
        context.fill();
        context.beginPath();
        context.arc(road.xf * 50, road.yf * 50, dotRadius, 0, Math.PI * 2);
        context.fill();
        
        if (showNamesCheckbox.checked){
            displayRoadsNames(context, road);
        };
    });
}

function setChart(road) {
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
