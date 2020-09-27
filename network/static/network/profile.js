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
    const profile_id=document.querySelector('#follow').getAttribute('data-id');
  
    //document.getElementById('follow').addEventListener('click', ()=>follow(profile_id));
    

   
    

   
    
});

function changeText()
{
    document.getElementById('follow').innerHTML='Unfollow';
};

function defaultText()
{
    document.getElementById('follow').innerHTML='Following';
};

function follow(){
    const  followerlist= document.createElement('div');
    const  followedlist= document.createElement('div');

    const profile_id=document.querySelector('#follow').getAttribute('data-id');
   
    fetch(`/follow/${profile_id}`)
    .then(response=>response.json())
    .then(result=>{
        console.log(result.message);
        

        if ( result.followed === 'yes'){
            


            document.getElementById('follow-func').innerHTML=` <button  class="follow-btn following-class ml-5" onmouseover="changeText(this)" 
             onmouseout="defaultText(this)"  onclick="follow(this)" data-id=${profile_id} id="follow" >  Following  </button>`
           
         

        }
        else
        {
        
            document.getElementById('follow-func').innerHTML=` <button 
             class="follow-btn follow-class ml-5" onclick="follow(this)"  data-id=${profile_id} id="follow" >  Follow  </button> `
          
        }
        
        console.log('a');
        document.getElementById("following_num").innerHTML=` ${result.followings} `;
        document.getElementById("followers_num").innerHTML=` ${result.followers} `;

        result.followerslist.forEach(function(follower){
            
            id=follower['id']
          
            followerid=follower['followerid']
            followerusername=follower['follower']
            name=follower['name']
            image=follower['image']
            const element = document.createElement('div');
            element.innerHTML=`
          <img class=" avatar ml-2 py-0 my-0" alt="100x100" onerror="this.onerror=null;this.src='https://designstudio.com/wp-content/themes/designstudio/assets/img/defaultAvatar.jpg;'" onclick="location.href='/profile/${followerid}'" data-holder-rendered="true" src='/media/images/${image}'> 
            <span onclick="location.href='/profile/${followerid}'" class=" comment-user ml-md-3 ml-1 mt-0 pt-0 "> ${name}
    
            @${followerusername} </span> 
    
            <hr class="lines">
           
            `
            followerlist.append(element);


        });

        document.querySelector('#modalbodyfollowers').innerHTML=followerlist.innerHTML;

        result.followingslist.forEach(function(followed){
            
            id=followed['id']
            followedid=followed['followedid']
            followedusername=followed['followed']
            name=followed['name']
            image=followed['image']
           
            const element = document.createElement('div');
            element.innerHTML=`
          <img class=" avatar ml-2 py-0 my-0" alt="100x100"  onerror="this.onerror=null;this.src='https://designstudio.com/wp-content/themes/designstudio/assets/img/defaultAvatar.jpg;'" onclick="location.href='/profile/${followedid}'" data-holder-rendered="true" src='/media/images/${image}'> 
            <span onclick="location.href='/profile/${followedid}'" class=" comment-user ml-md-3 ml-1 mt-0 pt-0 "> ${name}
    
            @${followedusername} </span> 
    
            <hr class="lines">
           
            `
            followedlist.append(element);


        });

        document.querySelector('#modalbodyfollowed').innerHTML=followedlist.innerHTML;
        
          
    });
         
        

    

}





function like(review){
    element=document.getElementById(`like${review.dataset.id}`)
    console.log(review.dataset.id);
    fetch(`/like/${review.dataset.id}`)
    .then(response=>response.json())
    .then(result=>{
        console.log(result.message);
        if (result.like_create==="yes"){
        element.innerHTML=` <i class="fa fa-heart heart" style="color:teal"></i> ${result.likes} `
        }
        else{
            element.innerHTML=`<i  class="fa heart">&#xf08a;</i>  ${result.likes}`
        }
    });
}



    
    
    
   
    
    

    





        
