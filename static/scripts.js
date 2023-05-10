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
      event.target.style.backgroundColor = '#90ee90';
    }
    // Otherwise, set the input field's background color to red
    else {
      event.target.style.backgroundColor = '#f08080';
    }
  });
};

document.addEventListener("DOMContentLoaded", checkPassword("passwordRegister")); 
document.addEventListener("DOMContentLoaded", checkPassword("confirmationRegister")); 
