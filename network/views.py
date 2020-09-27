from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt



from .models import User, Review, Comment, Like, Follow, Favorite

import os
import requests
from bs4 import BeautifulSoup

import xmltodict
import json
import operator
from operator import itemgetter
from random import randrange

NYtimes_dict={'Fiction':'combined-print-and-e-book-fiction',
'Nonfiction':'combined-print-and-e-book-nonfiction',
'Children':'childrens-middle-grade',
'Science':'science',
'Crime':'crime-and-punishment',
'Advice':'hardcover-advice',
'Miscellaneous':'advice-how-to-and-miscellaneous',
'Education':'education',
'Adult':'young-adult',

'Graphics & Manga':'graphic-books-and-manga',
'Series Books':'series-books',
'Picture books':'picture-books',
'Business':'business-books'}

NYtimes_list=['Fiction',
'Nonfiction',
'Children',
'Science',
'Miscellaneous',

'Graphics & Manga',
'Series Books',
'Picture books',
'Crime',
'Advice',
'Education',
'Adult',
'Business']



def index(request):
    radomnum=randrange(0,13,1)
    randomcategory=NYtimes_list[radomnum]


    
    response=requests.get(f"https://api.nytimes.com/svc/books/v3/lists/current/{NYtimes_dict[randomcategory]}.json?api-key=2L8LYUGBRtWnM9AtZVG5xZE6BwO8GWMu")
    books=response.json()['results']['books']
    topratedbooks=[]

    for book in books:


      
        book_details={"title":book['title'],
          
           "author":book['author'],
           "isbn":book['primary_isbn10'],
           "image":book['book_image']}
        topratedbooks.append(book_details)

    
    
    if request.user.id is not  None:
        
       #get the following feed
        user=User.objects.get(pk=request.user.id)
        
        #get the following list of the user
        
        following=user.followinglist.all()
       
        if len(following) > 0:
            # add the user and followers in a list
            
            following=[person.following.id for person in following]
            following.append(request.user.id)
           
        
            #get the list of reviews made by followers and the user
            reviews=(Review.objects.filter(reviewer__in=following))
            if len(reviews)>0:

                reviewcount = 'yes'
            else:
                reviews=(Review.objects.all())
                reviewcount = 'no'

        
        else:
            reviews=(Review.objects.filter(reviewer=request.user))
            if len(reviews)>0:

                reviewcount = 'yes'
            else:
                 reviewcount = 'no'




    else:
         reviews=(Review.objects.all())
         reviewcount = 'yes'


   
    reviews=reviews.order_by("timestamp").all()

    rereviews=(Review.objects.all())

    rereviews = [rereviews.filter(bookisbn=item['bookisbn']).last() for item in Review.objects.values('bookisbn').distinct()]
   
    topratedbooks=topratedbooks[0:12]

   

   
    recentreviews=reviewdict(rereviews,request.user)
    popreviews=reviewdict(reviews,request.user)
    recentreviews=sorted(recentreviews, key=itemgetter('id'),reverse=True) 
    
    popularreviews = sorted(popreviews, key=itemgetter('order'),reverse=True) 
    if len(recentreviews)>6:
        
        recentreviews=recentreviews[0:12]
    if len(popularreviews)>3:

        morereview='yes'

        popularreviews=popularreviews[0:3]
    else:
        morereview='no'
        
  
    if len(Review.objects.all())> 12:
       morerecent='yes'
    else:
        morerecent='no'

    

    
    

    return render(request, "network/index.html",{"NY_list":NYtimes_list,"books":topratedbooks,'category':randomcategory,
    "recentreviews":recentreviews,"popularreviews":popularreviews,"more":morereview,'recent':morerecent, 'reviewcount':reviewcount})


def NYtimes(request,category):
    #function to select categories in NY times list 
    response=requests.get(f"https://api.nytimes.com/svc/books/v3/lists/current/{NYtimes_dict[category]}.json?api-key=2L8LYUGBRtWnM9AtZVG5xZE6BwO8GWMu")
    books=response.json()['results']['books']
    topratedbooks=[]

    for book in books:
        book_details={"title":book['title'],
          
           "author":book['author'],
           "isbn":book['primary_isbn10'],
           "image":book['book_image']}
        topratedbooks.append(book_details)
    topratedbooks=topratedbooks[0:12]
    return JsonResponse(topratedbooks,safe=False)

    
def see_more(request,topic,field,isbn):
    current_user= request.user
    if topic == 'yes':
        reviews=(Review.objects.all())
        reviews=reviews.order_by("-timestamp").all()
        
        if field == 'popular':

            if request.user.id is not  None:
        
       #get the following feed
                user=User.objects.get(pk=request.user.id)
            
            #get the following list of the user
            
                following=user.followinglist.all()
        
                if len(following) > 0:
                # add the user and followers in a list
                
                    following=[person.following.id for person in following]
                    following.append(request.user.id)
                    reviews=(Review.objects.filter(reviewer__in=following))
                    if len(reviews)<0:
                        reviews=(Review.objects.all())
                else:
                    reviews=(Review.objects.filter(reviewer=request.user))
            else:
                reviews=reviews.order_by("-timestamp").all()

        
         
            recentreviews=reviewdict(reviews, current_user)   
            popularreviews = sorted(recentreviews, key=itemgetter('order'),reverse=True)
            paginator = Paginator(popularreviews, 6)
            sort='POPULAR'
            book= 'no'
        else:
            recentreviews=reviewdict(reviews, current_user) 
            paginator = Paginator(recentreviews, 6)
            sort='RECENT'
            book= 'no'

        
         # Show 6 reviews per page.

    elif topic == 'book':
        reviews=(Review.objects.filter(bookisbn=isbn))
        reviews=reviews.order_by("-timestamp").all()
        recentreviews=reviewdict(reviews, current_user)
        popularreviews = sorted(recentreviews, key=itemgetter('order'),reverse=True)
        if field == 'popular':
            paginator = Paginator(popularreviews, 6) # Show 6 reviews per page.
            sort='POPULAR'
            book= 'yes'
        else:
            paginator = Paginator(recentreviews, 6) # Show 6 reviews per page.
            sort='RECENT'
            book = 'yes'
    else:
        user=User.objects.get(username=isbn)
        reviews=(Review.objects.filter(reviewer=user))
        reviews=reviews.order_by("-timestamp").all()
        recentreviews=reviewdict(reviews, current_user)
        popularreviews = sorted(recentreviews, key=itemgetter('order'),reverse=True)

        if field == 'popular':
            paginator = Paginator(popularreviews, 6) # Show 6 reviews per page.
            sort='POPULAR'
            book= 'no'
        else:
            paginator = Paginator(recentreviews, 6) # Show 6 reviews per page.
            sort='RECENT'
            book= 'no'

    
   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

   
   
#render the page with review details  
    return render(request, "network/morereviews.html",{'page_obj': page_obj, 'sort':sort, 'book':book})
    




def reviewdict(reviewset,current_user):
    reviews_list=[]
    for review in reviewset:
       
        likes=review.likes.all()
    
        
        try:
            liked=review.likes.filter(liker=current_user)
            if len(liked)>0:

                liked="yes"
            else:
                liked="no"
        except:
            liked="no"
          
        comments=review.comments.all()
        number_likes=len(likes)
        number_comments=len(comments)
        order=0.5*number_likes+number_comments+1
        try:

            image=os.path.basename(os.path.normpath(review.reviewer.imagefile.path))
        except:
            image='notavailable'
        

        review_details={

            "id": review.id,
            "reviewer":review.reviewer.name,
            "reviewerid":review.reviewer.id,
            "reviewername":review.reviewer.name,
            "reviewerusername":review.reviewer.username,
            "content":review.content,
            "liked":liked,
            "timestamp":review.timestamp.strftime(" %d %b, %Y"),
            "likes":number_likes,
            "comments":number_comments,
            "image":image,
            "bookrating":review.bookrating,
            "title":review.booktitle,
            "img":image,
            "img_book":review.bookimg,
            "order":order,
            "isbn":review.bookisbn,
            "year":review.bookyear
           
            
        }
        reviews_list.append(review_details)
    return (reviews_list)






def openbook(request,isbn):
    book=requests.get(f'https://www.goodreads.com/book/isbn/{isbn}?key=1uUqGfvQqH8149G1Up3g')
    
    current_user = request.user
     
    
   
       
    try:
        bookdetails=json.loads((json.dumps(xmltodict.parse(book.content))))['GoodreadsResponse']['book']
        try:

            res = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
           
            google=res.json()
            

            
            imgsrc=google['items'][0]['volumeInfo']['imageLinks']['thumbnail']
            img=imgsrc
           
           
                

        except:
            img= bookdetails ['image_url']

        reviews=Review.objects.filter(bookisbn=isbn)
        
        ratings_list=(reviews.values_list('bookrating', flat=True))
        total=0
        avgstar=0
        for rating in ratings_list:
            total=float(rating)+total
        if (len(ratings_list) == 0):
            rating_count=1
        else:
            rating_count=len(ratings_list)
        avgstar=total/rating_count

        reviews=reviews.order_by("-timestamp").all()
        recentreviews=reviewdict(reviews,request.user)
        popularreviews = sorted(recentreviews, key=itemgetter('order'),reverse=True)
        if request.user.id is not  None:
            favorited=Favorite.objects.filter(lover=request.user,bookisbn=isbn)
            if len(favorited)>0:
                favorited ='yes'
            else:
                favorited = 'no'
        else:
            favorited='no'
        

        

        if len(recentreviews)>3:
        
            recentreviews=recentreviews[0:3]
            popularreviews=popularreviews[0:3]
            morereview='yes'
   
        else:
            morereview='no'
        
        
        try:

            description = BeautifulSoup(bookdetails['description'], "lxml").text
        except:
            description="NA"
  
        try:
           
           
            imgsrc=bookdetails['authors']['author']['image_url']['#text']
            authorid=bookdetails  ['authors'] ['author']['id'] 
        
        
            return render(request, "network/openbook.html",{"bookdetails":bookdetails,"img":img,"description":description,'imgsrc':imgsrc,'favorited':favorited,
            'authorid':authorid,"bookisbn":isbn,"rating":avgstar,"popularreviews":popularreviews,'recentreviews':recentreviews,'more':morereview})
        except:
            authors=[]
        
            for author in bookdetails['authors']['author']:
                authors.append({'image':author ['image_url']['#text'],
                'name':author['name'],
                'id':author['id'] })
            return render(request, "network/openbook.html",{"bookdetails":bookdetails,"img":img,'favorited':favorited,"description":description,
            'authors':authors,"bookisbn":isbn,"rating":avgstar,"popularreviews":popularreviews,'recentreviews':recentreviews,'more':morereview})
    except:
            return render(request, "network/openbook.html",{"update":"need to be updated","bookisbn":isbn})



def opengbook(request,gId):
    book=requests.get(f'https://www.goodreads.com/book/isbn/{gId}?key=1uUqGfvQqH8149G1Up3g')
    
    try:
        
   
        bookdetails=json.loads((json.dumps(xmltodict.parse(book.content))))['GoodreadsResponse']['book']
        isbn=bookdetails ['isbn']
        try:

            res = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
            
            google=res.json()
            

            
            imgsrc=google['items'][0]['volumeInfo']['imageLinks']['thumbnail']
            img=imgsrc
        
            
                    

        except:
            img= bookdetails ['image_url']

        current_user= request.user
        isbn=bookdetails ['isbn']
        reviews=(Review.objects.filter(bookisbn=isbn))
        ratings_list=(reviews.values_list('bookrating', flat=True))
        total=0
        avgstar=0
        for rating in ratings_list:
            total=float(rating)+total
        if (len(ratings_list) == 0):
            rating_count=1
        else:
            rating_count=len(ratings_list)
        avgstar=total/rating_count

        recentreviews=reviewdict(reviews,current_user)
        popularreviews = sorted(recentreviews, key=itemgetter('order'),reverse=True)
        if request.user.id is not  None:
            favorited=Favorite.objects.filter(lover=request.user,bookisbn=isbn)
            if len(favorited)>0:
                favorited ='yes'
            else:
                favorited = 'no'
        else:
            favorited='no'
        if len(recentreviews)>3:
            
            recentreviews=recentreviews[0:3]
            popularreviews=popularreviews[0:3]
            morereview='yes'

        else:
            morereview='no'
        try:

            description = BeautifulSoup(bookdetails['description'], "lxml").text
        except:
            description="NA"
        
    
        try:
            imgsrc=bookdetails['authors']['author']['image_url']['#text']
            authorid=bookdetails  ['authors'] ['author']['id'] 
            
            
            return render(request, "network/openbook.html",{"bookdetails":bookdetails,"img":img,"description":description,'imgsrc':imgsrc,'favorited':favorited,
            'authorid':authorid,"bookisbn":isbn,"rating":avgstar,"recentreviews":recentreviews,"popularreviews":popularreviews,'more':morereview})
        except:
            authors=[]
        
            for author in bookdetails['authors']['author']:
                authors.append({'image':author ['image_url']['#text'],
                'name':author['name'],
                'id':author['id'] })
            return render(request, "network/openbook.html",{"bookdetails":bookdetails,"img":img,"description":description,'favorited':favorited,
            'authors':authors,"bookisbn":isbn,"popularreviews":popularreviews,"rating":avgstar,"recentreviews":recentreviews,'more':morereview})
    except:
        return render(request, "network/openbook.html",{"update":"need to be updated"})

        
def author(request,authorid):

    authordetails=requests.get(f'https://www.goodreads.com/author/show/{authorid}?format=xml&key=1uUqGfvQqH8149G1Up3g')
    books=json.loads((json.dumps(xmltodict.parse(authordetails.content))))['GoodreadsResponse']['author']['books']['book']
    author=json.loads((json.dumps(xmltodict.parse(authordetails.content))))['GoodreadsResponse']['author']
    try:

        description = BeautifulSoup( author ['about'] , "lxml").text
    except:
        description='NA'
    



    return render (request,"network/author.html",{"author":author,"books":books, "description":description})

   
def searchresults(request,keyword):


        
   
    searchreq=requests.get(f'https://www.goodreads.com/search/index.xml?key=1uUqGfvQqH8149G1Up3g&q={keyword}')
    try:
        results=json.loads((json.dumps(xmltodict.parse(searchreq.content))))['GoodreadsResponse']['search']['results'] ['work']
      
        value='yes'
        results_list=[]
        for result in results:
            try:
                year=result ['original_publication_year'] ['#text']
            except:
                year=""
            results_list.append( {'title':result ['best_book'] ['title'],
            'year':year,

            'id':result ['best_book'] ['id'] ['#text'],
            'author':result ['best_book'] ['author'] ['name'],
            'imageurl':result ['best_book'] ['image_url']})

        results_number=len(results_list)
        paginator = Paginator(results_list, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

            
        return render(request, "network/searchresults.html",{"keyword":keyword,'result':value,"page_obj":page_obj,'results_num':results_number})
    except:
        value='no'
        return render(request, "network/searchresults.html",{"keyword":keyword,'result':value})

   

def open_review(request,review_id):
    #get the review the likes, comments on it
    review=Review.objects.get(pk=review_id)
    likes=review.likes.all()
    bookdetails={
    "isbn":review.bookisbn,
    "title":review.booktitle,
    "year":review.bookyear,
    "img":review.bookimg,
    "timestamp":review.timestamp.strftime(" %d %b, %Y")}
    comments=review.comments.all()
    comments=comments.order_by("-pk").all()
    number_likes=len(likes)
    number_comments=len(comments)
    #whether the review is liked by logged in user or not
  
    if request.user.id is not  None:
        
 

        liked=review.likes.filter(liker=request.user)

        if len(liked)>0:
            liked = 'yes'
        else:
            liked = 'no'
    else:
        liked = 'no'


    return render(request, "network/review.html",{'review':review,'likes':likes,'comments':comments,'num_likes':
    number_likes,'num_comments':number_comments,'liked':liked,'bookdetails':bookdetails})


@csrf_exempt
def compose(request):
    #function to compose a review
    if request.method!="POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    content=data.get("content","")
    booktitle=data.get("booktitle","")
    bookyear=data.get("bookyear","")
    bookisbn=data.get("bookisbn","")
    bookimg=data.get("bookimg","")
    bookrating=data.get("bookrating","")
    #create the review
 
    review=Review(
    reviewer=request.user,
    content=content,
    bookisbn=str(bookisbn),
    bookimg=bookimg,
    booktitle=str(booktitle),
    bookyear=bookyear,
    bookrating=str(bookrating)
    )
    review.save()

    return JsonResponse({"message":"Review sucessfully created."}, status=201)


@csrf_exempt
def favorite(request):
    #function to add book to fav list
    if request.method!="POST":
        return JsonResponse({"error": "POST request required."}, status=400)

   

    data = json.loads(request.body)
    bookisbn=data.get("bookisbn","")

    booktitle=data.get("booktitle","")
    bookimg=data.get("bookimg","")

    #whether the list has already 12 times or not
    Favlist=Favorite.objects.filter(lover=request.user)
   

    
    
    check=Favorite.objects.filter(bookisbn=bookisbn,lover=request.user)
    if len(check)<1:
        if len(Favlist)>11:

            return JsonResponse({"message":"The favorite list is full.","fav_added":"no"}, status=201)
        else:

            addtofav=Favorite(
            bookisbn=bookisbn,
            booktitle=booktitle,
            bookimg=bookimg,
            lover=request.user)
            addtofav.save()
            return JsonResponse({"message":" Book added to the favorite list.","fav_added":"Yes"}, status=201)
    else:
        check.delete()
        return JsonResponse({"message":"Book removed from the favorite list","fav_added":"no"}, status=201)






def reviewdetails(request,review_id):

    #fetch the particular review
    review=Review.objects.get(pk=review_id)
    content=review.content

    return JsonResponse({"content":content}, status=201)

def profiledetails(request,profile_id):

    #fetch the particular profile
    profile=User.objects.get(pk=profile_id)
    name=profile.name

    return JsonResponse({"name":content}, status=201)

@csrf_exempt
def editsave(request,review_id):
    if request.method!="POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    content=data.get("content","")
    review=Review.objects.get(pk=review_id)
    review.content=content
    review.save()

    return JsonResponse({"message":"review sucessfully edited."}, status=201)



def reviewfeed(request, isbn):
    
    reviews=Review.objects.filter(bookisbn=isbn)
     
   

    reviews=reviews.order_by("-timestamp").all()
    recentreviews=reviewdict(reviews,request.user)
    recentreviews= recentreviews[0:3]
    
    popularreviews = sorted(recentreviews, key=itemgetter('order'),reverse=True) 
    
   
    return JsonResponse(recentreviews,safe=False)




#function to like or unlike a review

def like(request,review_id):
    
#get thereview which is liked or unliked
    review=Review.objects.get(pk=review_id)
   
    #check whether the review is like by loginuser
    check=Like.objects.filter(likedreview=review,liker=request.user)
    likes_list=[]
    #if user is liking thereview
    if len(check)<1:
        likereview=Like(
        liker=request.user,
        likedreview=review)
        likereview.save()
        likes=review.likes.all()
        comments=review.comments.all()
        number_likes=len(likes)
        number_comments=len(comments)
        #list of all user who has liked thereview
        for like in likes:

            try:

                image=os.path.basename(os.path.normpath(like.liker.imagefile.path))
            except:
                image='notavailable'
    
            like_details={
                "id": like.id,
                "liker":like.liker.username,
                "likerid":like.liker.id,
                "name":like.liker.name,
                "image":image
                
            }
            likes_list.append(like_details)


        #send the updated likes list and liked numbers 
        return JsonResponse({"message":"review sucessfully liked.", "likes":f'{number_likes}',
        "comments":f'{number_comments}',"l_likes" :likes_list,"like_create":"yes"},
        status=201)
        
    else:
        # if user is unliking thereview delete the liked object
        check.delete()
        likes=review.likes.all()
        comments=review.comments.all()
        number_likes=len(likes)
        number_comments=len(comments)
        for like in likes:
            for like in likes:
                try:

                    image=os.path.basename(os.path.normpath(like.liker.imagefile.path))
                except:
                    image='notavailable'
            
    
            like_details={
               "id": like.id,
                "liker":like.liker.username,
                "likerid":like.liker.id,
                "name":like.liker.name,
                "image":image
                
            }
            likes_list.append(like_details)

            #send the updated likes list and liked numbers 
        
        return JsonResponse({"message":"review sucessfully disliked.","likes":f'{number_likes}',
        "comments":f'{number_comments}',"l_likes" :likes_list,"like_create":"no"}, status=201)

@csrf_exempt
def comment_post(request,review_id):

    #comment to a review
 

    data = json.loads(request.body)
    review=Review.objects.get(pk=review_id)
    
    content=data.get("content","")
    #create the comment object

    comment=Comment(
    commenter=request.user,
    comment=content,
    commentedreview=review

    )
    comment.save()
    #updated number of comments and likes
    likes=review.likes.all()
    comments=review.comments.all()
    number_likes=len(likes)
    number_comments=len(comments)

     #send the updated number of comments and likes
    return JsonResponse({"message":"Comment sucessfully created.","likes":f'{number_likes}',"comments":f'{number_comments}'}, status=201)

def settings(request):
    if  request.method=="GET":
        try:

            message = request.GET["status"]
            return render(request,"network/settings.html",{'message':message})
        except:
             return render(request,"network/settings.html")

        
    

def profile(request,user_id):
   
    #get the profile of the user requested
    user=User.objects.get(pk=user_id)
    #get the followers and following list of the user
    followers=user.followedbylist.all()
    followings=user.followinglist.all()
    #check whether the logged in user has followed the profile or not
   
    if request.user.id is not  None:
        if request.user.id != user.id:

            follow_='yes'
        else:
            follow_='no'
          
        
        followed=Follow.objects.filter(following=user,follower=request.user)
        if len(followed)>0:

            followed ='yes'
         
        else:
            followed = 'no'
           
    else:
        followed='no'
        follow_='no'
   
    number_followers=len(followers)
    number_followings=len(followings)
    #filter the reviews by the user
    reviews=(Review.objects.filter(reviewer=user_id))
    reviews=reviews.order_by("-timestamp").all()
    recentreviews=reviewdict(reviews,user)
    popularreviews = sorted(recentreviews, key=itemgetter('order'),reverse=True)
    
    if len(recentreviews)>3:
    
        recentreviews=recentreviews[0:6]
        popularreviews=popularreviews[0:3]
        morereview='yes'

    else:
        morereview='no'
    favlist=Favorite.objects.filter(lover=user)
    listfav=[]
    for book in favlist:
        listdetail={
        "isbn":book.bookisbn,
        "img":book.bookimg,
        "title":book.booktitle
        }
        listfav.append(listdetail)
#send details of number of followers , followings, reviews and followed by the logged in user or not
    return render(request,"network/profile.html",{'user':user,'following':followings,'followerslist':followers,"followed":followed,
    "followers":f'{number_followers}',"followings":f'{number_followings}','follow_': follow_,
    'recentreviews':recentreviews,'popularreviews':popularreviews,'favlist':listfav,'more':morereview})




def follow(request, user_id):

    #get the profilw of user

    profile=User.objects.get(pk=user_id)
   #check whether the user has been followed or not
    check=Follow.objects.filter(following=profile,follower=request.user)
    followerslist=[]
    followinglist=[]

    if len(check)<1:
        #follow the user
        followprofile=Follow(
        follower=request.user,
        following=profile)
        followprofile.save()
        followers=profile.followedbylist.all()
        followings=profile.followinglist.all()
        #update the number of followings and unfollowers
        number_followers=len(followers)
        number_followings=len(followings)
        followed='yes'
        for follow in followers:
            try:

                image=os.path.basename(os.path.normpath(follow.follower.imagefile.path))
            except:
                image='notavailable'
        
    
            follow_details={
                "id": follow.id,
                "follower":follow.follower.username,
                "followerid":follow.follower.id,
                "name":follow.follower.name,
                "image":image
                
            }
            followerslist.append(follow_details)
        for follow in followings:
            try:

                image=os.path.basename(os.path.normpath(follow.following.imagefile.path))
            except:
                image='notavailable'
    
            following_details={
                "id": follow.id,
                "followed":follow.following.username,
                "followedid":follow.following.id,
                "name":follow.following.name,
                "image":image
                
            }
            followinglist.append(following_details)

        
        return JsonResponse({"message":"profile sucessfully followed.", "followers":f'{number_followers}',"followings":f'{number_followings}', 
        "followed":followed,'followerslist':followerslist,'followingslist':followinglist},status=201)
        
    else:
        #unfollow the user
        check.delete()
        
        followers=profile.followedbylist.all()
        followings=profile.followinglist.all()
        for follow in followers:
            try:

                image=os.path.basename(os.path.normpath(follow.follower.imagefile.path))
            except:
                image='notavailable'
    

            follow_details={
                "id": follow.id,
                "follower":follow.follower.username,
                "followerid":follow.follower.id,
                "name":follow.follower.name,
                "image":image
                
            }
            followerslist.append(follow_details)
        for follow in followings:
                try:

                    image=os.path.basename(os.path.normpath(follow.following.imagefile.path))
                except:
                    image='notavailable'

                following_details={
                    "id": follow.id,
                    "followed":follow.following.username,
                    "followedid":follow.following.id,
                    "name":follow.following.name,
                    "image":image
                    
                }
                followinglist.append(following_details)

        #update the number of followings and unfollowers
        number_followers=len(followers)
        number_followings=len(followings)
        followed='no'

        
        return JsonResponse({"message":"profile sucessfully unfollowed.", "followers":f'{number_followers}','followerslist':followerslist,'followingslist':followinglist,"followed":followed,"followings":f'{number_followings}'}, status=201)


def comments(request,review_id):

    #api to get list of comments
    review=Review.objects.get(pk=review_id)
    #get comments in the review
    comments=review.comments.all()
    n_comments=len(comments)
    comments=comments.order_by("pk").all()
    comment_list=[]
    for comment in comments:
        try:

            image=os.path.basename(os.path.normpath(comment.commenter.imagefile.path))
        except:
            image='notavailable'
        comment_details={
            "id": comment.id,
            "commenter":comment.commenter.name,
            "commenterusername":comment.commenter.username,
            "content":comment.comment,
            "image":image,
            "commenterid":comment.commenter.id

        }
       
        comment_list.append(comment_details)

        #send the comment details 

    return JsonResponse({'comments':comment_list,'n_comments':n_comments},safe=False)


def deletereview(request,review_id):
    #get the review to be deleted
    review=Review.objects.get(pk=review_id)
    review.delete()
    return JsonResponse({"message":"review sucessfully deleted."}, status=201)



def deletecomment(request,comment_id):
    #get the comment to be deleted
    comment=Comment.objects.get(pk=comment_id)
    comment.delete()
    return JsonResponse({"message":"comment sucessfully deleted."}, status=201)
    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
      
     
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if  request.method=="POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name=request.POST["name"]
        
       
        # try:
            
        
        #     imagefile =request.FILES["imagefile"]

        # except:
        #     user=User.objects.get(username='anon')

        #     imagefile=user.imagefile
        
    
        
        

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
       
    
        if password != confirmation:
            return render(request, "network/login.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            #user = User.objects.create_user(username, email, password, imagefile=imagefile, name=name)
            user = User.objects.create_user(username, email, password, name=name)

            user.save()
        except IntegrityError:
            return render(request, "network/login.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/login.html")

@csrf_exempt

def editprofile(request,user_id):
    if  request.method=="POST":
        username = request.POST["username"]
        email = request.POST["email"]
        name=request.POST["name"]
        try:
            
        
            imagefile =request.FILES["imagefile"]
          

        except:
           
            user = User.objects.get(pk=user_id)
            imagefile= user.imagefile
        
    
        
        

        

        # Attempt to create new user
        try:
            #user = User.objects.create_user(username, email, password, imagefile=imagefile, name=name)
            user = User.objects.get(pk=user_id)

            user.username=username
            user.email=email
            user.name=name
            user.imagefile=imagefile
            user.password=request.user.password
           

            user.save()
            
          
        except IntegrityError:
            return HttpResponseRedirect("/settings?status=Username already taken.")
            
        login(request, user)
        return HttpResponseRedirect("/settings?status=Profile details has been  updated.")
        
    else:
         return HttpResponseRedirect("/settings?status=Profile details has been  updated.")




