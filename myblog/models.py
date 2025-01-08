from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Datas(models.Model):
    no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, blank=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    dob = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50, blank=True)
    pincode = models.IntegerField(blank=True, null=True)
    profimg = models.ImageField(upload_to="User_Profile_Images/", blank=True, null=True)

    def __str__(self):
        return self.email

class PostDatas(models.Model):
    idpost = models.AutoField(primary_key=True)
    namepost = models.CharField(unique=True, max_length=200)
    datepost = models.DateTimeField(default=now)
    imagepost = models.ImageField(upload_to="Post_Images/", blank=True, null=True)
    contpost = models.TextField()
    email = models.EmailField()
    data = models.ForeignKey(Datas, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.namepost

class FriendList(models.Model):
    S_no = models.AutoField(primary_key=True)
    me = models.ForeignKey(Datas, on_delete=models.CASCADE, related_name="friends")
    frnd = models.ForeignKey(Datas, on_delete=models.CASCADE, related_name="friend_of")
    frnd_img = models.ImageField(upload_to="Friends_Images/", blank=True, null=True)
    frnd_email = models.EmailField(max_length=200, null=True)
    my_email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return f"{self.me.email} - {self.frnd.email}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(PostDatas, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.namepost}"
    