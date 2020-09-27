from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    name=models.TextField(null=True)
    imagefile= models.FileField(upload_to='images/', null=True, verbose_name="")

class Review(models.Model):
    reviewer=models.ForeignKey("User",on_delete=models.CASCADE,related_name="reviews")
    bookisbn=models.TextField(blank=False)
    booktitle=models.TextField(blank=True)
    bookimg=models.TextField(blank=True)
    bookyear=models.TextField(blank=True)
    bookrating=models.TextField(blank=True)
    
    content=models.TextField(blank=False)
    timestamp=models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    rater=models.ForeignKey("User",on_delete=models.CASCADE,related_name="ratings")
    bookisbn=models.TextField(blank=False)
    rate=models.IntegerField(blank=False)
 
class Comment(models.Model):
    commenter=models.ForeignKey("User",on_delete=models.CASCADE,related_name="listcomments")
    comment=models.TextField(blank=False)
    commentedreview=models.ForeignKey("Review",on_delete=models.CASCADE,related_name="comments")

class Like(models.Model):
    liker=models.ForeignKey("User",on_delete=models.CASCADE,related_name="listlikes")
    likedreview=models.ForeignKey("Review",on_delete=models.CASCADE,related_name="likes")

class Favorite(models.Model):
    lover=models.ForeignKey("User",on_delete=models.CASCADE,related_name="listloves")
    bookisbn=models.TextField(blank=False)
    booktitle=models.TextField(blank=False)
    bookimg=models.TextField(blank=False)
    



class Follow(models.Model):
    follower=models.ForeignKey("User",on_delete=models.CASCADE,related_name="followinglist")
    following=models.ForeignKey("User",on_delete=models.CASCADE,related_name="followedbylist")        
    
