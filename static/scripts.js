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

  for (let i = 0; i < xAxisNodes.length; i++) {
    let item = xAxisNodes[i];
    item.addEventListener('click', function() {
  
          chartHeader = item.value;
          loadChart(chartHeader);

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
  
  const xAxisNodes = document.getElementsByName("flexRadioCompare");
  if (xAxisNodes.length !=0) {
    chartHeader = xAxisNodes[0].value;
  }
  else {
    chartHeader = "Distance";
  };

  dt.addEventListener('click', function() {
    loadChart(chartHeader, dt.value);
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

function loadChart(chartHeader = "Distance", date = new Date()) {

  let xyValues = getChartData(chartHeader, date); 

  let ctx = document.getElementById("myChartId").getContext("2d");
  // rdestroy previous chart if created before re-creating
  if (myChart) {
    myChart.clear();
    myChart.destroy();
  };

  myChart = new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [{
        label: chartHeader,
        pointRadius: 4,
        pointBackgroundColor: "rgb(0,0,255)",
        data: xyValues
      }]
    },
    options: {
      legend: { display: false },
      responsive: true,
      maintainAspectRatio: false
    }
  });
};

function getChartData(chartHeader, date) {

  return [
    { x: 50, y: 7 },
    { x: 60, y: 8 },
    { x: 70, y: 8 },
    { x: 80, y: 9 },
    { x: 90, y: 9 }
  ];

  let httpreq = new XMLHttpRequest();

  httpreq.open("GET", "/api/compare", true);
  httpreq.setRequestHeader("Content-Type", "application/json");
  
  let params = {
    "chartType": chartHeader,
    "date": date,
  };
  httpreq.send(JSON.stringify(params));
  httpreq.onreadystatechange = function() {
      if (httpreq.readyState === XMLHttpRequest.DONE && httpreq.status === 200) {
        // TODO: decide if we need it
      }
    };
  httpreq.send();

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