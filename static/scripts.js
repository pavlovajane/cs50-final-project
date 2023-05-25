let myChart = null;

const checkPassword = (name) => { 
  const passwordInput = document.getElementById(name);

  // Has minimum 8 characters in length
  // At least one uppercase English letter
  // At least one lowercase English letter
  // At least one digit
  // At least one special character
  const passwordRegex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/;
  passwordInput.addEventListener('input', function (event) {    
    const isValid = passwordRegex.test(this.value);

    // If the input value is valid, set the input field's background color to green
    if (isValid) {
      event.target.style.backgroundColor = '#b8f5c8';
    }
    // Otherwise, set the input field's background color to red
    else {
      event.target.style.backgroundColor = '#f5c9d1';
    }
  });
};

const checkDistance = (name) => {
 
  const distanceInput = document.getElementById("distance");
  
  distanceInput.addEventListener('input', function (event) {
    let prevVal = "";
    const isValid = Number(this.value)>=0;
    if (isValid) {
      prevVal = this.value;
    } else {
      this.value = prevVal;
    }
  });
};

const registerAddRunInput = () => {
  let inputs = document.querySelectorAll('#addrunForm input');

  inputs.forEach(function (input) {
    input.addEventListener('keydown', function (event) {
      if (event.key === 'Enter') {
        event.preventDefault();
      }
    });
  });
}

function intializePlaces() {
  let input = document.getElementById('city');
  let autocomplete = new google.maps.places.Autocomplete(input);
  
  autocomplete.addListener('place_changed', function () {
    let place = autocomplete.getPlace();
    let lat = document.getElementById('lat');
  
    lat.value = place.geometry['location'].lat();
    let long = document.getElementById('lang'); 
    long.value = place.geometry['location'].lng();
  });
};

const registerMeasurementSwitcher = () => {
  
  const switchInput = document.getElementById('flexSwitchCheckDefault');
  const switchLabel = document.getElementById('switchLabel');

  switchInput.addEventListener('click', function() {
    if (switchInput.checked) {
      switchLabel.textContent = 'mi';
      switchInput.value = 'mi';
    } else {
      switchLabel.textContent = 'km';
      switchInput.value = 'km';
    }
  });
};

const registerMeasurementSwitcherChart = () => {
  
  const xAxisNodes = document.getElementsByName("flexRadioCompare");
  const dt = document.getElementById("datecompare");

  for (let i = 0; i < xAxisNodes.length; i++) {
    let item = xAxisNodes[i];
    item.addEventListener('click', function() {
  
          chartHeader = item.value;
          loadChart(chartHeader, dt.value);

      });
  };
};

const registerCompareDateSwitcher = () => {

  const dt = document.getElementById("datecompare");

  // if value is empty - set current date
  if (!dt.value) {
    date = new Date();
    
    // format current date to YYYY-MM-DD

    let dateFormat = date.getFullYear() + "-" +((date.getMonth()+1).toString().length != 2 ? "0" 
    + (date.getMonth() + 1) : (date.getMonth()+1)) + "-" + (date.getDate().toString().length != 2 ?"0" 
    + date.getDate() : date.getDate());

    dt.value = dateFormat;
  
  };
  
  let chartHeader = getMesaurmenetsValue();

  dt.addEventListener('change', function() {
    loadChart(chartHeader, this.value);
  });
};

function deleteTableRow(rowid) {

  if (confirm("Confirm row deletion") != true) {
    return;
  }
  // if row delete button was clicked - intiate row deletion
  let httpreq = new XMLHttpRequest();

  httpreq.open("DELETE", "/" + rowid, true);
  httpreq.setRequestHeader("Content-Type", "application/json");
  httpreq.onreadystatechange = function() {
      if (httpreq.readyState === XMLHttpRequest.DONE && httpreq.status === 200) {
        // Handle the response from the server if needed
        window.location.reload();
      }
    };
  httpreq.send();

};

function loadChart(chartHeader = "Distance", datereport = new Date().toISOString()) {

  // convert date to ISO format it is in YYYY-MM-DD
  datereport = convert_to_iso_date(datereport);
  // set chosen type of chart - distance/speed
  chartHeader = getChartHeader();
  // set axis labels - based on if user uses imperial/metric values
  let measurement = getMesaurmenetsValue(chartHeader);
  
  // get data for the chart
  let xyValues = getChartData(chartHeader, datereport); 

  let ctx = document.getElementById("myChartId").getContext("2d");
  // rdestroy previous chart if created before re-creating
  if (myChart) {
    myChart.clear();
    myChart.destroy();
  };

  myChart = new Chart(ctx, {
    type: "bubble",
    labels: xyValues,
    data: {
      datasets: [{
        label: chartHeader + "/Time",
        data: xyValues
      }]
    },
    options: {
      legend: { display: false },
      scales: {
        x: {
          title: {
            display: true,
            text: chartHeader + measurement
          }
        },
        y: {
          title: {
            display: true,
            text: "Time, h"
          }
        }
      },
      responsive: true,
      maintainAspectRatio: false
    }
  });
};

function returnImperial() {
  // return settings of the user imperial = 1/0 received from backend
  return imperial==1 ? true : false;
};

function convert_to_iso_date(datecheck) {
  // conver date from YYYY-MM-DD to ISO strin format
  return new Date(datecheck).toISOString();

};

function getMesaurmenetsValue(chartHeader, measurement = ", kmh") {
  if (chartHeader == "Speed") {
    if (returnImperial()) {
      measurement = ", mph";
    } else { measurement = ", kmh" };
  }
  else {
    if (returnImperial()) {
      measurement = ", mi";
    } else { measurement = ", km" };
  };
  return measurement
}

function getChartHeader(header = "Distance") {
    
    const xAxisNodes = document.getElementsByName("flexRadioCompare");
    
    for (i = 0; i < xAxisNodes.length; i++) {
      if (xAxisNodes[i].checked)
          return header = xAxisNodes[i].value;
    }

    return header
  
};

function getChartData(chartHeader, datereport) {

  let httpreq = new XMLHttpRequest();

  httpreq.open("POST", "/api/compare", false);
  httpreq.setRequestHeader("Content-Type", "application/json");
  
  let params = {
    "chartType": chartHeader,
    "datereport": datereport,
  };
  
  httpreq.onreadystatechange = function() {
      if (httpreq.readyState === XMLHttpRequest.DONE && httpreq.status === 200) {
        result = httpreq.responseText;
       }
    };
  httpreq.send(JSON.stringify(params));

  return JSON.parse(result)
  
};

function createPointsColorArray(dataObj){
  let colorArray = [];
  for (let i = 0; i < dataObj.length; i++) {
    if (dataObj[i].hasOwnProperty("user") && dataObj[i]["user"]==1) {
      // color red for users' value
      colorArray.push("rgb(245, 162, 177)")
    } else {
      colorArray.push("rgb(54, 162, 235)")
    };
  };
  return colorArray;
};

const router = (event) => {
  switch(window.location.pathname) {
    case "/":
      break;
    case "/addrun":
      intializePlaces();
      registerAddRunInput();
      checkDistance("distance");
      registerMeasurementSwitcher();
      break
    case "/compare":
      registerMeasurementSwitcherChart();
      registerCompareDateSwitcher();
      loadChart();
      break
    case "/settings":
      break
    case "/register":
      checkPassword("passwordRegister"); 
      checkPassword("confirmationRegister");
      break        
  }
}

document.addEventListener("DOMContentLoaded", router);