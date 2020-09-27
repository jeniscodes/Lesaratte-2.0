




document.addEventListener('DOMContentLoaded', function() {

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
        var rates=document.querySelectorAll(`.ratestar .stars-inner`);
        for (star of rates)
        {
            star.style.width = starPercentageRounded;
        }

     

    }
  
    const NYselect=document.querySelector('#NYlist_select');
    NYselect.addEventListener("change", NYtopic);

    
    
    

  


   
   
    

});




function NYtopic ()
{
    const NYselect=document.querySelector('#NYlist_select');
    
    const feedelement=document.createElement('div');
    document.querySelector('#NY-best').style.display="none";
    document.querySelector('#loading').style.display="flex";

    document.querySelector('#NY-best').innerHTML='';
    category=NYselect.value
    setTimeout( function() {
    fetch(`/NYtimes/${category}`)
    .then(response=>response.json())
    .then(books=>{
        books.forEach(function(book){

            title=book['title'],
            image=book['image']
            isbn=book['isbn']
            const element = document.createElement('div');
            element.classList.add('col-sm-2', 'col-3','book-col-fav');
            element.innerHTML=` 
        <div class="tooltipt">
  
        
        
        <img src="${image}"  class="img-fluid  img-open books-prof mt-1  mb-1" onclick="location.href='/opengbook/${isbn}'"> 
    
        <span class="tooltiptext d-none d-md-block">  
            ${title} 
            </span>
    </div>



  
  `

            
 
  document.querySelector('#NY-best').append(element);
        })

        
        

    });

  
    document.querySelector('#NY-best').style.display="flex";
   
    

}, 3000);
setTimeout( function(){

    document.querySelector('#loading').style.display="none";},4550);
}


function like(tweet){
    element=document.getElementById(`like${tweet.dataset.id}`)
    console.log(tweet.dataset.id);
    fetch(`/like/${tweet.dataset.id}`)
    .then(response=>response.json())
    .then(result=>{
        console.log(result.message);
        if (result.like_create==="yes"){
        element.innerHTML=` <i class="fa heart fa-heart" style="color:teal"></i> ${result.likes} `
        }
        else{
            element.innerHTML=`<i class="fa heart">&#xf08a;</i>  ${result.likes}`
        }
    });
}



 
        




