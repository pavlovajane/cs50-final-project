const checkPassword=(name)=>(event)=>{
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

const checkDistance=(name)=>(event)=>{
  // only positive floats or integers
  // const distanceRegex = /^[-+]?[0-9]+\.[0-9]+$/;
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


document.addEventListener('DOMContentLoaded', function () {
  intializePlaces();

  let inputs = document.querySelectorAll('#addrunForm input');
  inputs.forEach(function (input) {
    input.addEventListener('keydown', function (event) {
      if (event.key === 'Enter') {
        event.preventDefault();
      }
    });
  });

});

function intializePlaces() {

  let input = document.getElementById('city');
  let autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.addListener('place_changed', function () {
    let place = autocomplete.getPlace();

    let lat = document.getElementById('lat');
    lat.value = place.geometry['location'].lat();
    let long = document.getElementById('lang'); 
    long.value = place.geometry['location'].lng();

    console.log(lat.value)
    console.log(lang.value)

  });
};

document.addEventListener('DOMContentLoaded', function() {
  // Your JavaScript code here
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
});

function deleteTableRow(rowid) {

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

document.addEventListener("DOMContentLoaded", checkPassword("passwordRegister")); 
document.addEventListener("DOMContentLoaded", checkPassword("confirmationRegister")); 
document.addEventListener("DOMContentLoaded", checkDistance("distance"));

