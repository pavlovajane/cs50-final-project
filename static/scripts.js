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


google.maps.event.addDomListener(window, 'load', initialize);
  function initialize() {

    let input = document.getElementById('city');
    let autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.addListener('place_changed', function () {
      let place = autocomplete.getPlace();
      
      $('#lat').val(place.geometry['location'].lat());
      $('#long').val(place.geometry['location'].lng());

  });

}

document.addEventListener("DOMContentLoaded", checkPassword("passwordRegister")); 
document.addEventListener("DOMContentLoaded", checkPassword("confirmationRegister")); 
document.addEventListener("DOMContentLoaded", checkDistance("distance"));
