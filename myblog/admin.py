from django.contrib import admin
from .models import Datas,PostDatas,FriendList,Comment

# Register your models here.

admin.site.register(Datas)
admin.site.register(PostDatas)
admin.site.register(FriendList)
admin.site.register(Comment)