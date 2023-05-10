document.addEventListener("DOMContentLoaded", function (event) {
  const passwordRegisterInput = document.getElementById("passwordRegister");

  // Has minimum 8 characters in length
  // At least one uppercase English letter
  // At least one lowercase English letter
  // At least one digit
  // At least one special character
  const passwordRegex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/;
  passwordRegisterInput.addEventListener('input', function () {

    const isValid = passwordRegex.test(this.value);

    // If the input value is valid, set the input field's background color to green
    if (isValid) {
      passwordRegisterInput.style.backgroundColor = 'lightgreen !important';
      console.log('Input is valid');
    }
    // Otherwise, set the input field's background color to red
    else {
      passwordRegisterInput.style.backgroundColor = 'lightred !important';
      console.log('Input is not valid');
    }
  });
});