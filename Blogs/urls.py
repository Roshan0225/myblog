"""
URL configuration for Blogs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myblog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path( 'admin/', admin.site.urls ),
    path( '', views.home, name="" ),
    path( 'register/' , views.register , name="register" ), 
    path( "login/" , views.login , name="login" ),
    path( 'uview/', views.u_view, name='uview'),
    path( "view/", views.postview, name="view"),
    path( "postreg/", views.postreg , name="postreg" ),
    path( 'follow/', views.follow, name='follow' ),
    path( 'follow_frd/', views.follow_frd, name='follow_frd' ),
    path( 'friends/<int:S_no>/', views.friends_list, name='friends' ),
    path( 'user_blog/', views.user_blog, name='user_blog' ),
    path( "update/", views.update, name="update"),
    path( 'b_update/<int:id>/', views.b_update, name="b_update"),
    path( "img_view/<int:id>/", views.img_view, name="img_view"),
    path( 'ur_delete/', views.ur_delete, name="ur_delete"),
    path( 'bl_delete/<int:id>/', views.bl_delete, name="bl_delete"),
    path( "logout/" , views.logout , name="logout" ),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)