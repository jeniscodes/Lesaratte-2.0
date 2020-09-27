
document.addEventListener('DOMContentLoaded', function() {

  
    document.querySelector('.icon-1').addEventListener("click", function() {
      document.querySelector('.input').classList.toggle("active");
      document.querySelector('.input_').classList.toggle("active");
      document.querySelector('#search-icon').classList.toggle("fa-search");
      document.querySelector('#search-icon').classList.toggle("fa-times");
    

     

      
    
    });
    

    const search1=document.getElementById('bsearch1');
    
    const search2=document.getElementById('bsearch2');


    const searchtab=document.querySelector('#bsearch');
    

    document.getElementById('bsearch1').addEventListener("keyup", function(search) {
        // Number 13 is the "Enter" key on the keyboard
        if ( search1.value.length > 0)
        {
        if (search.keyCode === 13) {

         keyword=search1.value;
         console.log(keyword);
         location.href = `/searchresults/${keyword}`;
        
        }
      }
      });

      document.getElementById('bsearch2').addEventListener("keyup", function(search) {
        if ( search2.value.length > 0)
        {
        // Number 13 is the "Enter" key on the keyboard

        if (search.keyCode === 13) {

         keyword=search2.value;
         console.log(keyword);
         location.href = `/searchresults/${keyword}`;
        
        }
      }
      });

   
    

   
    
});