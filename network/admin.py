from django.contrib import admin
from .models import User, Like , Comment , Review, Follow , Favorite


# Register your models here.
admin.site.register(User)
admin.site.register(Like)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Favorite)