document.addEventListener('DOMContentLoaded', function() {
   
   var name= document.querySelector('#name').getAttribute('data-name');
   var username= document.querySelector('#username').getAttribute('data-username');
   var email= document.querySelector('#email').getAttribute('data-email');
   
   
   
   
    document.querySelector('#name').value=`${name}`;
    document.querySelector('#username').value=`${username}`;
    document.querySelector('#email').value=`${email}`;

    document.querySelector('#alert').style.display='block';
    setTimeout(function(){
        document.querySelector('#alert').style.display='none';
    },3000);

});


    
function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();

                reader.onload = function (e) {
                    $('#profileimage-setting')
                        .attr('src', e.target.result);
                };

                reader.readAsDataURL(input.files[0]);
            }
        }




