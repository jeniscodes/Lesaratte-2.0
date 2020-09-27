document.addEventListener('DOMContentLoaded', function() {


    rateclasses=document.getElementsByClassName('ratestar');
    for ( rate of rateclasses)
    {
        console.log(rate);
        var num=rate.getAttribute('data-rate');
        id=rate.getAttribute('data-id');
        
        var star = parseFloat(num);

        const starPercentage = (star / 5) * 100;

        // Round to nearest 10
        const starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;

        console.log(starPercentageRounded );

        // Set width of stars-inner to percentage
        elements=document.querySelectorAll(`.r${id} .stars-inner`)
        for (element of elements)
        {
            element .style.width = starPercentageRounded;

        }
        
       
     

    }

    console.log(window.innerWidth);
 
    document.querySelector('#edit-content').style.display = 'none';
    document.querySelector('#temporary').style.display = 'none';


    let textarea1 = document.querySelector(".resize-ta");
    textarea1.addEventListener("keyup", () => {
      textarea1.style.height = calcHeight(textarea1.value) + "px";
    });


    function calcHeight(value) {
        let numberOfLineBreaks = (value.match(/\n/g) || []).length;
        // min-height + lines x line-height + padding + border
        let newHeight = 20 + numberOfLineBreaks * 20 + 12 + 2;
        return newHeight;
      }

      let textarea2 = document.querySelector(".resize-tab");
      textarea2.addEventListener("keyup", () => {
        textarea2.style.height = calcHeight(textarea2.value) + "px";
      });
  
  
    
    


   

  

   


    const comment_btn=document.querySelector('#comment_submit');
    const comment=document.querySelector('#commentedtext');
  
    comment_btn.disabled=true;

    comment.onkeyup= function(){
  
    if (comment.value.length > 0)
    {
    
        comment_btn.disabled=false;
    }
    else {
        comment_btn.disabled=true;
    }
}
 
    
});


function load_comment(){
    const commentelement=document.createElement('div');

    const user=document.querySelector('#user').getAttribute('data-user');
   
    const reviewer=document.querySelector('#user').getAttribute('data-reviewer');
    
    const review_id=document.querySelector('#user').getAttribute('data-id');
  
    fetch(`/comments/${review_id}`)
    .then(response=>response.json())
    .then(comments=>{
        comments.comments.forEach(function(comments){
            
            id=comments['id'];
            commenter=comments['commenter'];
            comment=comments['content'];
            image=comments['image'];
            username=comments['commenterusername'];
            commenterid=comments['commenterid']
            const element = document.createElement('div');
            if ( user == username || reviewer == user )
            {
               
                del=`<i class="fa fa-trash trashicon my-0 py-0 " 
                data-toggle="modal" data-target="#exampleModal2" aria-hidden="true" data-id=${id} onclick="deletethis(this)"></i>`
            }
            else{
              
                del=''
            }
            element.innerHTML=`

            <div class="row">

            <div class="col-lg-3 pt-0 mt-1  ">

  <img class=" avatar py-0 my-0" alt="100x100" onerror="this.onerror=null;this.src='https://designstudio.com/wp-content/themes/designstudio/assets/img/defaultAvatar.jpg;'" onclick="location.href='/profile/${commenterid}'" data-holder-rendered="true" src='/media/images/${image}'> 
 <span class=" comment-user ml-md-3 ml-1 mt-0 pt-0  " onclick="location.href='/profile/${commenterid}'"> ${commenter}  @${username} </span> 

</div>
<div class="col-lg-9 comment-text pl-3 pb-0  ">
<pre class="mt-0 pl-0 py-0 ml-0  mt-3    commenttext">${comment}</pre> 

${del}


</div>

</div>

<hr class="mb-1 lines mt-1 ">


            
            
        `
            commentelement.append(element);

        })
        var commentsnum =document.getElementById('commentsnum ');
        console.log(document.querySelector('#commentsnum '));
        commentsnum .innerHTML=comments.n_comments;
        document.querySelector('#commentfeed').innerHTML= commentelement.innerHTML
    });


}

function like(review){
    const likelist= document.createElement('div');
    element=document.getElementById(`like${review.dataset.id}`)
    console.log(review.dataset.id);
    fetch(`/like/${review.dataset.id}`)
    .then(response=>response.json())
    .then(result=>{
        console.log(result.message);
        if (result.like_create==="yes"){
        element.innerHTML=` <i class="fa fa-heart heart" style="color:teal"></i>`   
    
        }
        else{
            element.innerHTML=` <i  class="fa heart">&#xf08a;</i>`
            
        }

        document.getElementById('num_like').innerHTML=`${result.likes}`;
        document.querySelector('#modalbody').innerHTML=''
        result.l_likes.forEach(function(like){
            
            id=like['id']
            likerid=like['likerid']
            liker=like['liker']
            name=like['name']
            image=like['image']
            const element = document.createElement('div');
            element.innerHTML=`
          <img class=" avatar py-0 my-0"  onerror="this.onerror=null;this.src='https://designstudio.com/wp-content/themes/designstudio/assets/img/defaultAvatar.jpg;'"  alt="100x100" onclick="location.href='/profile/${likerid}'" data-holder-rendered="true" src='/media/images/${image}'> 
            <span onclick="location.href='/profile/${likerid}'" class=" comment-user ml-md-3 ml-1 mt-0 pt-0 "> ${name}
    
            @${liker} </span> 
    
            <hr class="lines">
           
            `
            likelist.append(element);


        });

        document.querySelector('#modalbody').innerHTML=likelist.innerHTML
        
          
    });
}




function post_comment(review){
    const commentsnum =document.getElementById('commentsnum ');
    
     
    const content=document.querySelector('#commentedtext').value;
    
    document.querySelector('#temporary').style.display = 'block';
   

  
    document.querySelector('#tempcontent').innerHTML= `<p class="tempcontent">${content}</p>`;
    
       
        fetch(`/post/${review.dataset.id}`,{
            method:'POST',
            body:JSON.stringify({
                content:`${content}`
            })
        })
        .then(response=>response.json())
        .then(result=>{
            console.log(result.message);
            commentsnum .innerHTML=`${result.comments}`
        });

        document.querySelector('#commentedtext').value='';
        document.querySelector('#comment_submit').disabled=true;
        setTimeout(load_comment,3000);
        setTimeout(function(){document.querySelector('#temporary').style.display = 'none';},3000);


    return false;

    
    }

function edit(review){
        
        document.querySelector('#edit-content').style.display = 'block';
       
        
        document.querySelector('#review-box').style.display = 'none';
        document.querySelector('#edit_btn').style.display = 'none';
        console.log( document.querySelector('#review-box'));
        document.querySelector('#edit-content').style.display = 'block';
        
        fetch(`/reviewdetails/${review.dataset.id}`)
    .then(response=>response.json())
    .then(result=>{
        

        document.querySelector('#reviewedit').value=result.content;
        

    });
}

    function edit_save (review){
        const content=document.querySelector('#reviewedit').value;
        console.log(review.dataset.id);
        
        fetch(`/editsave/${review.dataset.id}`,{
            method:'POST',
            body:JSON.stringify({
                content:`${content}`,
                
            })
        })
        .then(response=>response.json())
        .then(result=>{
            console.log(result.message);
        });

        setTimeout(() => {location.reload()
            
        }, 2000);
        return false;  
      
    }

  

    function deletethis(comment){
        window.id=comment.dataset.id;
        console.log(id);
    }
    

    function deletecomment (){
        commentcard=document.getElementById(`comment${id}`);
        //commentcard.style.animationPlayState = 'running';

        
        fetch(`/deletecomment/${id}`)
        .then(response=>response.json())
        .then(result=>{
            console.log(result.message);
        });

        setTimeout(load_comment,3000);
      

        return false;  
    }


    function deletereview (review){
        
        console.log(review.dataset.id)
        fetch(`/deletereview/${review.dataset.id}`)
        .then(response=>response.json())
        .then(result= setTimeout(function()
        {
            console.log(result.message);
        },3000)
        );

        
        setTimeout(function(){
            location.href='/';
        },3000);

        return false;



    }

  


   

   
   
    

    


    
    
   
    
    

    





        
