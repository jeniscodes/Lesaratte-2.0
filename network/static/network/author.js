document.addEventListener('DOMContentLoaded', function() {
var count=0;

var text = document.getElementsByClassName('author-description');

for ( des of text )

{




var par = des.textContent;
if ( par.length > 250 )

{
    var front= par.substring(0,250);
   
  
   

    const element = document.createElement('span');

    element.innerHTML= par;

   

    element.id='text' + count;



    element.style.display="none";

    document.getElementById('read-more').append(element);

    des.id= 'par' + count;


    des.innerHTML=  ` ${front}   <span class="expand" onclick='expand(this)' data-count=${count}> ... Read More   </span> `;
    count=count+1;
}


}
});



function expand(rest)
{
i= rest.dataset.count;
var r=document.querySelector(`#par${i}`);
r.innerHTML= document.querySelector(`#text${i}`).textContent;


}
