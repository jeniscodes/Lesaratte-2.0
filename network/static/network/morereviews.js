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

        console.log(starPercentageRounded );

        // Set width of stars-inner to percentage
        document.querySelector(`.r${id} .stars-inner`).style.width = starPercentageRounded;

     

    }
      
});

function like(tweet){
    element=document.getElementById(`like${tweet.dataset.id}`)
    console.log(tweet.dataset.id);
    fetch(`/like/${tweet.dataset.id}`)
    .then(response=>response.json())
    .then(result=>{
        console.log(result.message);
        if (result.like_create==="yes"){
        element.innerHTML=` <i class="fa fa-heart heart" style="color:teal"></i> ${result.likes} `
        }
        else{
            element.innerHTML=`<i class="fa heart">&#xf08a;</i>  ${result.likes}`
        }
    });
}