from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
     path("editprofile/<int:user_id>", views.editprofile, name="editprofile"),
    path("openbook/<str:isbn>",views.openbook, name="openbook"),
    path("opengbook/<str:gId>",views.opengbook, name="opengbook"),
    path("author/<str:authorid>",views.author, name="author"),
    path('open_review/<int:review_id>',views.open_review,name="open_review"),
    path('see_more/<str:topic>/<str:field>/<str:isbn>',views.see_more,name="see_more"),
    path("searchresults/<str:keyword>",views.searchresults, name="searchresults"),
    path('profile/<int:user_id>',views.profile,name="profile"),
     path('settings',views.settings,name="settings"),


    #API Routes
    path("compose",views.compose,name="compose"),
    path("favorite",views.favorite,name="favorite"),
    path("NYtimes/<str:category>",views.NYtimes,name="NYtimes"),
    path("reviewfeed/<str:isbn>",views.reviewfeed,name="reviewfeed"),
    path("like/<int:review_id>",views.like,name="like"),
    path("reviewdetails/<int:review_id>",views.reviewdetails,name="reviewdetails"),
    path("profiledetails/<int:profile_id>",views.profiledetails,name="profiledetails"),
    path("editsave/<int:review_id>",views.editsave,name="editsave"),
    path("post/<int:review_id>",views.comment_post,name="comment_post"),
    path("comments/<int:review_id>",views.comments,name="comments"),
    path("follow/<int:user_id>",views.follow,name="follow"),
    path('deletereview/<int:review_id>',views.deletereview,name="deletereview"),
    path("deletecomment/<int:comment_id>",views.deletecomment,name="deletecomment")






]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

