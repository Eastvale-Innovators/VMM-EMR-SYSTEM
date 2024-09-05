const firebaseConfig = {
    apiKey: "AIzaSyAcdEd-dzfcmkQ6KGUQykclh1LcbOeitak",
    authDomain: "vmmauth-3c02a.firebaseapp.com",
    projectId: "vmmauth-3c02a",
    storageBucket: "vmmauth-3c02a.appspot.com",
    messagingSenderId: "986128793453",
    appId: "1:986128793453:web:ae295e5f8177c096cf2464"
  };

  // Initialize Firebase
firebase.initializeApp(firebaseConfig);  // Initialize variables
  const auth = firebase.auth()
  const database = firebase.database()

  // set up register function
function register() {
    username = document.getElementById('username').value
    email = document.getElementById('email').value
    password = document.getElementById('password').value


 // Validate input fields
 if (validate_email(email) == false || validate_password(password) == false) {
    alert('Email or Password dont meet verification reqs')
    return
    // Don't continue running the code
  }

  // Move on with auth
  auth.createUserWithEmailAndPassword(email, password)
  .then(function() {
    // Declare user variable
    var user = auth.currentUser

    // Add this user to Firebase Database
    var database_ref = database.ref()

    // Create User data
    var user_data = {
      email : email,
      username : username,
      last_login : Date.now()
    }

    // Push to Firebase Database
    database_ref.child('users/' + user.uid).set(user_data)

    // Done
    alert('User Created')
  })
  .catch(function(error) {
    // Firebase will use this to alert of its errors
    var error_code = error.code
    var error_message = error.message

    alert(error_message)
  })
}

//Set up login function
function login(){
  //Get input fields
  email = document.getElementById('loginEmail').value
  password = document.getElementById('loginPassword').value
  // validate
  if (validate_email(email) == false || validate_password(password) == false) {
    alert('Email or Password dont meet reqs')
    return
    // Don't continue running the code
  }
    auth.signInWithEmailAndPassword(email,password)
    .then(function(){
      // Declare user variable
      var user = auth.currentUser

      // Add this user to Firebase Database
      var database_ref = database.ref()

      // Create User data
      var user_data = {
        last_login : Date.now()
      }

      // Push to Firebase Database
      database_ref.child('users/' + user.uid).update(user_data)

      // Done
      alert('User Logged in')
    })
    .catch(function(error){
    // Firebase will use this to alert of its errors
    var error_code = error.code
    var error_message = error.message

    alert(error_message)
    })

}




 function validate_email(email) {
    expression = /^[^@]+@\w+(\.\w+)+\w$/
    if (expression.test(email) == true) {
      // Email is good
      return true
    } else {
      // Email is not good
      return false
    }
  }
  function validate_password(password) {
    // Firebase only accepts lengths greater than 6
    if (password < 6) {
      return false
    } else {
      return true
    }
  }

  function validate_field(field) {
    if (field == null) {
      return false
    }
  
    if (field.length <= 0) {
      return false
    } else {
      return true
    }
  }