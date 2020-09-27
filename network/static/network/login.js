const signUpButtons = document.getElementsByClassName('signUp');
const signInButtons = document.getElementsByClassName('signIn');
const container = document.getElementById('container');

console.log(window.innerWidth);
console.log(document.querySelector('#alert').textContent.length);
if (document.querySelector('#alert').textContent.length == 70)
{
        document.querySelector('#alert').style.display='none';  
}

else{
        document.querySelector('#alert').style.display='block';
}

setTimeout(function(){
    document.querySelector('#alert').style.display='none';
    
},3000);

for (signUpButton of signUpButtons){
signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});
}

for (signInButton of signInButtons){
    console.log(signInButton);
    signInButton.addEventListener('click', () => {
        
            container.classList.remove("right-panel-active");
        
    });
    }

