const uname = document.getElementById('username');
const email = document.getElementById('exampleInputEmail1');
const pass1 = document.getElementById('exampleInputPassword1');
const pass2 = document.getElementById('exampleInputPassword2');
const form = document.getElementById('signUpForm');
const btn = document.getElementById('signUpBtn');
const message = document.getElementById('message');

form.addEventListener('submit',(e)=>{
  if(pass1.value !== pass2.value){
    console.log('Invalid Passwords');
    message.attributes.removeNamedItem('hidden');
        e.preventDefault();
        window.location.href('#');
  }else{
    message.attributes.setNamedItem('hidden');
  }
});

