const form = document.getElementById('form');
    /* username ids */
  const usernameInput = document.getElementById('Username');
  const usernameLabel = document.getElementById('username');
    /* email ids */
  const emailInput = document.getElementById('Email');
  const emailLabel = document.getElementById('email');
    /* password ids */
  const passwordInput = document.getElementById('Password');
  const passwordLabel = document.getElementById('password');
    /* Validation ids */
  const confirmedPasswordInput = document.getElementById('Password_2');
  const confirmedPasswordLabel = document.getElementById('password_2');
    /* Validation ids */
  const usernameValidation = document.getElementById('username-Validation');
  const emailValidation = document.getElementById('email-Validation');
  const passwordValidation = document.getElementById('password-Validation');
  const passwordValidation_2 = document.getElementById('password_2-Validation');
    // button id 
  const buttonLogin = document.getElementById('Login-Button');

   //media query for mobiels 
  const mediaQuery = window.matchMedia('(min-width:481px) and (max-width:961px)')




  const usernameChecked = usernameInput.addEventListener(
    'keyup', function(){
      const checkUsernames = (checkUsername(usernameInput.value)) ? usernameLabel.style.color ="#048e00" : usernameLabel.style.color ="#000000";
      return checkUsernames;
      });

  const emailIsChecked = emailInput.addEventListener('keyup', function(){
        const emailChecked =  (checkEmail(emailInput.value)) ? emailLabel.style.color ="#048e00": emailLabel.style.color ="#000000";  
        return emailChecked;
      })
      


  const passwordIsChecked = passwordInput.addEventListener('keyup', function(){
      const checkpasswords = (checkPassword(passwordInput.value)) ? passwordLabel.style.color ="#048e00" : passwordLabel.style.color ="#000000";

      return checkpasswords
    });

  const checkConfirmedPassword = confirmedPasswordInput.addEventListener('keyup', function(){
    const confirmpasswords = (confirmedsecondPassword(confirmedPasswordInput.value)) ? confirmedPasswordLabel.style.color ="#048e00" : confirmedPasswordLabel.style.color ="#000000";

    return confirmpasswords
    }
    );


  function checkUsername(username) {
    const pattern =  /^(?=.*[A-Za-z])(?=.*\d)(?=.*[._])[A-Za-z\d._]{4,15}$/.test(
      username)

      form.addEventListener('keyup', (e) => {
        if (pattern){
          usernameValidation.textContent = '';
        } else {
            e.preventDefault();
            usernameValidation.textContent = 'Take your time to choose a special username by using _ or .';
            }

            if (mediaQuery.matches) {
              // Then trigger an alert
              usernameValidation.style.color ="#3b64b7";
            } else {
              usernameValidation.style.color ="#e84c4c";
            }
        })

    return pattern;
    
    };

  function checkEmail(email) {
    const pattern =  /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email)


    form.addEventListener('keyup', (e)=>{
      if(pattern){
        emailValidation.textContent = ''
        //emailValidation.style.display = 'none';

      } else {
          e.preventDefault();
          emailValidation.textContent='Get closer to S2alle by using your correct E-mail Adresse.'
          //emailValidation.style.display = 'block';
          if (mediaQuery.matches) {
            // Then trigger an alert
            emailValidation.style.color ="#3b64b7";
          } else {
            usernameValidation.style.color ="#e84c4c";
          }


        }
      
    })
      

    return pattern
  }

  function checkPassword(password){
    const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@_$!%*?&])[A-Za-z\d@$!%*-_?&]{8,}$/.test(password);
    
    form.addEventListener('keyup', (e) => {
      if (pattern){
        passwordValidation.textContent = '';
      } else{
          e.preventDefault();
          passwordValidation.textContent = "Emboss your password with [@,-,_,?] and Uppercase letter to make it stronger as your forhead";
          if (mediaQuery.matches) {
            // Then trigger an alert
            passwordValidation.style.color ="#3b64b7";
          } else {
            usernameValidation.style.color ="#e84c4c";
          }
        }
      })
      return pattern
    }


  function confirmedsecondPassword(secondpassword){
    const condition = (secondpassword == passwordInput.value);

      if (!condition){
        passwordValidation_2.textContent = "Blind or stupid, which one are you?";
        if (mediaQuery.matches) {
          // Then trigger an alert
          passwordValidation_2.style.color ="#3b64b7";
        } else {
          usernameValidation.style.color ="#e84c4c";
        }
        
      } else {
        passwordValidation_2.textContent = '';
        return condition
      }


  }


  function checkingBox(){
    const checkBox = document.getElementById('check').checked;
    if(checkBox){
      return true
    }else{ 
      return false
    }
  }

  




  form.addEventListener('submit', (e) => {
    console.log(checkUsername(usernameInput.value));
    console.log(checkEmail(emailInput.value));
    console.log(checkPassword(passwordInput.value));
    console.log(confirmedsecondPassword(confirmedPasswordInput.value));
    console.log(checkingBox())
    e.preventDefault();
    if(checkUsername(usernameInput.value) && checkEmail(emailInput.value) && checkPassword(passwordInput.value) && confirmedsecondPassword(confirmedPasswordInput.value) === checkPassword(passwordInput.value) && checkingBox()){
      form.submit()
    } else {
      console.log('Try again')
    }
  })
