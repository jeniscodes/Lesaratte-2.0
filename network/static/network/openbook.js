document.addEventListener('DOMContentLoaded', function() {


   //load stars rating values
   stars();


document.getElementById("temporary").style.display = "none";




var count=0;

var text = document.getElementsByClassName('readmore');

for ( des of text )

{




var par = des.textContent;
if ( par.length > 500 )

{
    var front= par.substring(0,500);
    var rest= par.substring(500, par.length + 1);
  
   

    const element = document.createElement('span');

    element.innerHTML= par;

    document.querySelector('#temporary').append(element);

    element.id='text' + count;

    element.style.display="none";

    des.id= 'par' + count;


    des.innerHTML=  ` ${front}   <span class="expand" onclick='expand(this)' data-count=${count}> ... Read More   </span> `;
    count=count+1;
}


}








// Get the left column , footer, right column and lowest element
var wrap = document.getElementById("wrap");
var footer = document.getElementById("footer");
var right= document.getElementById("right");
var scrollht= document.getElementById("scrollht");



// Get the offset position of the left , footer and lowest element
var sticky = wrap.offsetTop;
var foot = footer.offsetTop;
var ht=scrollht.offsetTop;




he=(ht-sticky);

shift= foot - he;
h= shift - 195 ;








           

        // When the user scrolls the page, execute myFunction
if (window.innerWidth >= 1000 )
{
    
window.onscroll = function() {myFunction()};
}



// Add the sticky class and right class to right elemnt when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset >= sticky && window.pageYOffset < ( foot-(he +  65 ) ) ) {
    wrap.classList.add("sticky");
    wrap.style.marginTop = 0 + "px" ;
    right.classList.add("right");
  } else if (window.pageYOffset >  (foot-(he  + 65 ) ) ) {
    wrap.classList.remove("sticky");
    wrap.style.marginTop = foot-(he +  110 ) + "px" ;
    
    right.classList.remove("right");
  }
    else
  {
    wrap.classList.remove("sticky");

    wrap.style.marginTop = 0   + "px";
  
    
    right.classList.remove("right");  
  }
}

  
   
    
    const review_btn=document.querySelector('#post_btn');
    const review=document.querySelector('#review');

    const bookisbn=document.querySelector('#post_btn').getAttribute('data-isbn');
    const title= document.querySelector('#favorite_add').getAttribute('data-title');
    const img= document.querySelector('#favorite_add').getAttribute('data-img');
    const year= document.querySelector('#favorite_add').getAttribute('data-year');

   
    let textarea = document.querySelector(".resize-ta");
    textarea.addEventListener("keyup", () => {
      textarea.style.height = calcHeight(textarea.value) + "px";
    });


    function calcHeight(value) {
        let numberOfLineBreaks = (value.match(/\n/g) || []).length;
        // min-height + lines x line-height + padding + border
        let newHeight = 20 + numberOfLineBreaks * 20 + 12 + 2;
        return newHeight;
      }

 
 
    
    review_btn.disabled=true;

    document.querySelector('#review').onkeyup= function(){
  
    if (review.value.length > 0)
    {
    
        review_btn.disabled=false;
    }
    else {
        review_btn.disabled=true;
    }


    
}





   
    document.querySelector('#post_btn').onclick = function(){
        const content=document.querySelector('#review').value;
       
        
        document.querySelector('#temp').innerHTML= content;
        if (document.querySelector('input[name="rating"]:checked')== null)
        {
           
            document.querySelector('#alert').innerHTML=' Please leave a rating along with the review.';
            document.querySelector('#alert').style.display='block';
        setTimeout(function(){
            document.querySelector('#alert').style.display='none';
        },3000);


        }
        else
        {
        const ratingbook = document.querySelector('input[name="rating"]:checked').value;
        document.querySelector('#temporary').style.display = 'block';
        
        rates=document.getElementsByClassName('rating');
        for ( rate of rates)
        {
           
            rate.checked=false;
           

        }

        
        
        fetch('/compose',{
            method:'POST',
            body:JSON.stringify({
                bookisbn:`${bookisbn}`,
                content:`${content}`,
                bookrating:`${ratingbook}`,
                
                booktitle:`${title}`,
                bookimg:`${img}`,
                bookyear:`${year}`
                
            })
        })
        .then(response=>response.json())
        .then(result=>{
            console.log(result.message);
        });
        setTimeout(function(){
            
            document.querySelector('#temporary').style.display = 'none';
        }, 2500) 
         setTimeout(function(){
            
            load_reviews(bookisbn);
        }, 3000); 
       
        document.querySelector('#review').value='';
        post_btn.disabled=true;
        document.querySelector('#review').placeholder='Add a review ... ';


        


        return false;  
       
    }
}


 
    
});

function stars()
{
   
    rateclasses=document.getElementsByClassName('ratestar');
    for ( rate of rateclasses)
    {
        
        var num=rate.getAttribute('data-rate');
        id=rate.getAttribute('data-id');
        
        var star = parseFloat(num);

        const starPercentage = (star / 5) * 100;

        // Round to nearest 10
        const starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;

  

        // Set width of stars-inner to percentage

        classe=document.querySelectorAll(`.r${id} .stars-inner`);
     
      

        for (element of classe)
        {
        
            element.style.width=starPercentageRounded;
        }



 
     

    }
}

function expand(rest)
{
i= rest.dataset.count;
var r=document.querySelector(`#par${i}`);
r.innerHTML= document.querySelector(`#text${i}`).textContent;


}




function load_reviews(isbn){
     
  
    const feedelement=document.createElement('div');
        fetch(`/reviewfeed/${isbn}`)
        .then(response=>response.json())
        .then(reviews=>{
            reviews.forEach(function(review){
              
                id=review['id'];
              
                reviewer=review['reviewer'];
                contents=review['content'];
                timestamp=review['timestamp'];
                likes=review['likes'];
                comments=review['comments'];
                bookrating=review['bookrating'];
                reviewerid=review['reviewerid'];
                reviewerusername=review['reviewerusername'];
                image=review['image'];
                liked=review['liked'];
                console.log(bookrating);
                if ( liked == 'yes'){

                likey = '<i class="fa heart fa-heart " style="color:teal"></i>'
                }
                else
                {

                likey = '<i class="fa heart">&#xf08a;</i>'
                }
                
                const element = document.createElement('div');
                element.innerHTML=` 
                 <div>
                <img class=" avatar py-0 my-0" onerror="this.onerror=null;this.src='https://designstudio.com/wp-content/themes/designstudio/assets/img/defaultAvatar.jpg;'" alt="100x100" onclick="location.href='/open_review/${id}'" data-holder-rendered="true" src='/media/images/${image}'>   
                <span class="pl-2 reviewby " onclick="location.href='/open_review/${id}'"> <span class="reviewspan"> Review by </span>  <span class="username pl-1">   ${reviewer}
                   @${reviewerusername}</span> </span><span class="ratestar r${id} ml-2 " data-rate= "${bookrating}" data-id= "${id}" > <span class="stars-outer">
                   <span class="stars-inner"></span> </span> </span> <span class="timestamp mt-2" > ${timestamp}  </span> 
               <p> <pre class="content"> ${contents}   </pre> </p>  
                 <div class="likeblock ">
                     <span onclick="like(this)" class="like${id}" data-id="${id}"> 
                     ${likey}
                     ${likes}  
                     </span> <span class="ml-5" onclick="location.href='/open_review/ ${id}'" > 
                     <i class="fa fa-comment-o" aria-hidden="true"></i>  ${comments}
                     </span>
                     </div>

                     <hr class="style14"> `

                        
         









                feedelement.append(element);
    
            })
            document.querySelector('#reviewfeed').innerHTML= feedelement.innerHTML

            stars();

            
    
        }); 
        


}

 
function changeText(){
    var buttons= document.getElementsByClassName('favorite_');

    
    for (button of buttons){
        button.innerHTML= 'Remove from the favorites';
        button.style.backgroundColor= 'orangered';
    }
 }


 function defaultText(){
    var buttons= document.getElementsByClassName('favorite_');

    
    for (button of buttons){
        button.innerHTML= ' <i class="fa fa-bookmark mr-2"></i> Favorited';
        button.style.backgroundColor= 'teal';
    }
 }


function like(review){
    elements=document.getElementsByClassName(`like${review.dataset.id}`)
    console.log(elements);
    
    fetch(`/like/${review.dataset.id}`)
    .then(response=>response.json())
    .then(result=>{
        console.log(result.message);

        for ( const item of elements )
        {
            if (result.like_create === "yes"){
                item.innerHTML=` <i class="fa fa-heart heart" style="color:teal"></i> ${result.likes} `;
               
                }
                else{
                    item.innerHTML=`<i  class="fa heart">&#xf08a;</i>  ${result.likes}`;
                   
                }
        }

       
        
    });
}


function favorite(review){
    elements=document.getElementsByClassName('fav-btn');
    smallbtn=document.getElementById('small-fav');
    
    fetch('/favorite',{
        method:'POST',
        body:JSON.stringify({
        
            bookisbn:`${review.dataset.isbn}`,
            booktitle:`${review.dataset.title}`,
            bookimg:`${review.dataset.img}`

            
        })
    })
    .then(response=>response.json())
    .then(result=>{
       
        
        document.querySelector('#alert').innerHTML=`${result.message}`;
        document.querySelector('#alert').style.display='block';
       
        

        if (result.fav_added==="Yes"){
            for (element of elements )
            {
           
         
            element.innerHTML=` <button  onmouseover="changeText(this)"  onmouseout="defaultText(this)" onclick=favorite(this) id="favorite_add" class=" favorite_   favorited_add mt-3"
            data-isbn="${review.dataset.isbn}" data-year="${review.dataset.year}"  data-title="${review.dataset.title }" data-img="${review.dataset.img}" > 
            <i class="fa fa-bookmark mr-2"></i> Favorited </button>`
            }
            smallbtn.classList.add('favorited');
            smallbtn.classList.remove('add_fav');
            smallbtn.innerHTML=' <i class="fa fa-bookmark mr-2"></i> Favorited'
            }
            else{
                for ( element of elements)
                {
              
               
                element.innerHTML=` <button  onclick=favorite(this) id="favorite_add" class=" favorite_   favorited_ mt-3"
                data-isbn="${review.dataset.isbn}" data-year="${review.dataset.year}"  data-title="${review.dataset.title }" data-img="${review.dataset.img}" > 
                <i class="fa fa-bookmark mr-2"></i> Add to  Favorites</button>`;
                }
                smallbtn.classList.add('add_fav');
                smallbtn.classList.remove('favorited');
                smallbtn.innerHTML=' <i class="fa fa-bookmark mr-2"></i> Add to Favorites'
            }
    });

    setTimeout(function(){
        document.querySelector('#alert').style.display='none';
    },3000);


}






