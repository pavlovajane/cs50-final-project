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
});

function intializePlaces() {

  let input = document.getElementById('city');
  let autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.addListener('place_changed', function () {
    let place = autocomplete.getPlace();

    let lat = document.getElementById('lat');
    lat.innerHTML = place.geometry['location'].lat();
    let long = document.getElementById('lang'); 
    long.innerHTML = place.geometry['location'].lng();

  });
};

document.addEventListener('DOMContentLoaded', function() {
  // Your JavaScript code here
  const switchInput = document.getElementById('flexSwitchCheckDefault');
  const switchLabel = document.getElementById('switchLabel');

  switchInput.addEventListener('click', function() {
    if (switchInput.checked) {
      switchLabel.textContent = 'mi';
    } else {
      switchLabel.textContent = 'km';
    }
  });
});

document.addEventListener("DOMContentLoaded", checkPassword("passwordRegister")); 
document.addEventListener("DOMContentLoaded", checkPassword("confirmationRegister")); 
document.addEventListener("DOMContentLoaded", checkDistance("distance"));
