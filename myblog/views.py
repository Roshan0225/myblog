from django.shortcuts import render
from django.http import HttpResponseForbidden
from .models import Datas,PostDatas,FriendList,Comment
from django.contrib.auth.models import User
from django.core.mail import send_mail 
from django.contrib import messages
from django.conf import settings
import datetime
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.


#Home Page Of Application.
def home(request):
    return render(request,"home.html")


#Register Your Data.
def register(request):

    # Check Request Method.
    if request.method == "POST":

        #Extract Form Data.
        name = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        dob = request.POST.get("dob")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        profimg = request.FILES.get("profimg")

        #Check for Duplicate Email.
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("/register/")

        # Create a New User.
        user = User.objects.create_user(username=email, password=password, email=email)
        
        #Save Additional User Data.
        obj = Datas.objects.create(
            name=name,
            password=password,
            email=email,
            dob=dob,
            phone=phone,
            city=city,
            pincode=pincode,
            profimg=profimg
        )

        #Send Welcome Email.

        subject = "Welcome to Our Service"
        message = f"""
        Hearty Welcome...!
        Your Details Have Been Registered Successfully...!
        You Can Login Using Your Email and Password...!
        """
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        except Exception as e:
            print(f"Error sending email: {e}")
        
        #Add Success Message and Redirect to Login.
        messages.success(request, "Registration successful! Please login.")
        return redirect("/login/")
    
    #Render Registration Page for GET Requests.
    return render(request, "register.html")


#Login Page Authentication Process.
def login(request):
    if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome {user.username}, you are now logged in.")

            # Send login notification email
            subject = "Login Notification"
            message = f"Hello {user.username}, you have successfully logged in."
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            except Exception as e:
                print(f"Error sending email: {e}")

            # Redirect to the user's dashboard or other pages
            return redirect('view')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect("/login/")
    
    return render(request, "login.html")

otp_store = {}
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(username=email)
            print(user)
            otp = random.randint(100000, 999999)
            otp_store[email] = otp

            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is {otp}.',
                f'For {email}',
                [email],
                fail_silently=False,
            )
            messages.success(request, "OTP sent to your email successfully.")
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
    return render(request, "forgot_password.html")

def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print(email)
        otp = int(request.POST.get('otp', 0))

        if otp_store.get(email) == otp:
            messages.success(request, "OTP verified successfully.")
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid email or OTP.")
    return render(request, "verify_otp.html")


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            try:
                user = User.objects.get(username=email)
                user.set_password(new_password)  # Securely hash the new password
                print(user)
                user.save()
                messages.success(request, "Password reset successfully. You can log in now.")
                return redirect("login")
            except User.DoesNotExist:
                messages.error(request, "No account found with this email.")
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, "reset_password.html")

@login_required(login_url="/login/")
def postview(request):
    # Use the authenticated user's email
    email = request.user.email
    mine = get_object_or_404(Datas, email=email)
    
    # Fetch all posts and shuffle them
    po = PostDatas.objects.all()
    post_list = list(po)
    random.shuffle(post_list)

    return render(request, "view.html", {"mine": mine, "po": post_list})

#To View User Personal Details.
@login_required(login_url="/login/")
def u_view(request):
    #Getting Email From Datas And Filtering Email 
    email=request.user.email

    gd = Datas.objects.filter(email=email)
    #Printing the variable.
    print(gd)
    #Returning User View To Get User Details.
    return render(request,"uview.html",{"gd":gd})


#Registering Your Post.
@login_required(login_url="/login/")
def postreg(request):
    #Getting Object From Datas Database And Filtering Email.
    email=request.user.email
    mydata=get_object_or_404(Datas,email = email)

    #Checkin Data Is Post Method Or Not.
    if request.method=="POST":
        namepost = request.POST.get("namepost")
        imagepost = request.FILES.get("imagepost")
        email=request.POST.get("email")
        contpost = request.POST.get("contpost")
        
        #Filtering Datas From PostDatas Databases For Data Intergerity Issue.
        #If Any Post With Same Title It Will Throw An Error Message 
        if PostDatas.objects.filter(email=email,namepost=namepost).exists():
            error_message = "A post with this title already exists. Please choose a different title."
            return render(request, "postreg.html", {"error_message": error_message})  
        # If New Post Creating Required Datas Using Email.      
        obj=PostDatas.objects.create(
            namepost=namepost,
            imagepost=imagepost,
            email=mydata.email,
            contpost=contpost,
            data=mydata
            )

        #Rendering To Post View Html Page With Sending All Postdatas .
        return redirect("view")
    
    #Rendering Datas From To Post Registration Page For New Registration.
    return render(request,"postreg.html",{"mydata":mydata})


#Getting to follow page and seeing new friends.
@login_required(login_url="/login/")
def follow(request):
    
    my=request.user.email
    # Get the logged-in user's data
    mydata = get_object_or_404(Datas, email=my)
    
    # Get the IDs of friends already followed by the user
    followed_friends = FriendList.objects.filter(me=mydata.no).values_list('frnd', flat=True)
    
    # Fetch all users except the logged-in user and those already followed
    dt = Datas.objects.exclude(no__in=followed_friends).exclude(no=mydata.no)
    
    # Rendering Html Page For Rendering 
    # mydata = Logged in user          -----        dt = Friends user available to follow
    return render(request, "follow.html", {"mydata": mydata, "dt": dt})


#Adding New friends into friendlist.
@login_required(login_url="/login/")
def follow_frd(request):
    # Getting the logged-in user's data
    mydata = get_object_or_404(Datas, email=request.user.email)

    if request.method == "POST":
        # Extracting the new friend's email from POST data
        newfr_email = request.POST.get('newfr_email')

        # Validating the new friend's email exists in the database
        frdata = get_object_or_404(Datas, email=newfr_email)

        # Checking if the friend is already in the friend list
        alr_frd = FriendList.objects.filter(me=mydata.no, frnd=frdata.no).exists()

        # Fetching all data from the main database
        dt = Datas.objects.all()

        if not alr_frd:
            # Adding the new friend to the friend list
            FriendList.objects.create(
                me=mydata,
                frnd=frdata,
                frnd_img=frdata.profimg,
                frnd_email=frdata.email,
                my_email=mydata.email
            )
            # Success response
            # return render(request, "follow.html", {"mydata": mydata, "alr_frd": alr_frd, "dt": dt})
            return redirect("follow")
        else:
            # Handling duplicate friend entries
            messages.info(request, "User Already In Your Friends List")
    else:
        # Handling non-POST requests
        return render(request, "follow.html")


#Logged in user blog only visible.
@login_required(login_url="/login/")
def user_blog(request):

    email = request.user.email
    #Getting Datas From Database Using Email.
    bl = get_object_or_404(Datas, email=email) 

    #Filtering PostDatas Using Bl.email To View Only User Posted Datas.   
    us = PostDatas.objects.filter(email=bl.email) 

    #Rendering For Succes Template.
    return render(request, "user_blog.html", {"us": us, "bl": bl})

#Seeing new friends and making unfollow for the user and counting friends list.
@login_required(login_url="/login/")
def friends_list(request, S_no):
    #Getting Datas From Datas Table.
    mis = get_object_or_404(Datas, no=S_no)

    #Checking POST Method Or Not.
    #Handling Unfollow Request.
    if request.method == "POST" and "unfollow" in request.POST:
        friend_id = request.POST.get("friend_id")
        #Attempt Of Removing Friend From FriendList
        try:
            friend_instance = get_object_or_404(FriendList, me=mis, frnd_id=friend_id)
            friend_instance.delete()
            messages.success(request, "Friend unfollowed successfully.")
        except FriendList.DoesNotExist:
            messages.error(request, "Friend not found in your list.")

    #Fetch Friends To Count Total Count And Display.
    friends = FriendList.objects.filter(me=mis)
    friends_count = friends.count()

    #Rendering Template To Friends List 
    return render(request, "f_list.html", {"friends": friends,"friends_count": friends_count,})


#Updating a user who logged in updating personal datas.
@login_required(login_url="/login/")
def update(request):

    email=request.user.email
    #Checking Data is post method or not
    if request.method == "POST":
        # Retrieve the user data to update
        upd = get_object_or_404(Datas, email=email)
        
        # Update fields with new data from the form
        upd.name = request.POST.get("name")
        upd.password = request.POST.get("password")  # Consider hashing the password
        upd.phone = request.POST.get("phone")
        upd.city = request.POST.get("city")
        upd.pincode = request.POST.get("pincode")
        
        # Check For Uploaded Profile Image
        profimg = request.FILES.get("profimg")
        if profimg:
            upd.profimg = profimg
        
        # Save the updated data
        try:
            upd.save()
            messages.success(request, "Profile updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating profile: {e}")
        
        # Redirect to the user's view page
        return redirect("uview")  

    # For GET requests, retrieve the current user data and render the update page
    sr = get_object_or_404(Datas, email=email)
    return render(request, "update.html", {"sr": sr})


#User can delete their own account.
@login_required(login_url="/login/")
def ur_delete(request):
    email = request.user.email
    # Get the user data object
    user_data = get_object_or_404(Datas, email=email)
    if request.method == "POST":
        # Delete the user data
        user_data.delete()
        # Optionally, delete the associated Django user account
        try:
            user_account = User.objects.get(email=email)
            user_account.delete()
        except User.DoesNotExist:
            messages.error(request, "Associated user account not found.")
        # Show success message and redirect to the home page
        messages.success(request, "Account and associated data deleted successfully.")
        return redirect("")
    # Render a confirmation page before deletion
    return render(request, "delete.html", {"user_data": user_data})

@login_required(login_url="/login/")
def bl_delete(request, id):
    # Fetch the PostDatas details using the post ID
    bl = get_object_or_404(PostDatas, idpost=id)

    # Perform deletion
    bl.delete()

    # Redirect after deletion
    return redirect("view")

#To update user blog.
@login_required(login_url="/login/")
def b_update(request,id):
    
    #Fetching Datas POST Method Or Not.
    if request.method == "POST":
        #Fetching Datas From PostDatas Using postid
        br = get_object_or_404(PostDatas, idpost=id)

        #Update Fields With New Datas.
        br.namepost = request.POST.get("namepost")
        br.contpost = request.POST.get("contpost")
        br.email = request.POST.get("email")
        datepost = request.POST.get("datepost")
        #To Update Date
        if datepost:
            br.datepost=datepost

        #To Update Image Files.
        imagepost = request.FILES.get("imagepost")
        if imagepost:
            br.imagepost=imagepost
        
        #To Save Files.
        br.save()

        #Redirecting To a function to get the data
        return redirect("view")
    sr = get_object_or_404(PostDatas, idpost=id)
    
    # For GET requests, retrieve the current post data and render the update page
    return render(request, "bupdate.html",{"sr":sr})


#Handling Comment section.
@login_required(login_url="/login/")
def img_view(request, id):
    # Fetch the post or return a 404 error
    post = get_object_or_404(PostDatas, idpost=id)

    # Handle comment submission
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        if comment_text:
            # Create a new comment linked to the post and logged-in user
            Comment.objects.create(post=post, user=request.user, text=comment_text)
        # Redirect back to the same page to reload it without resubmitting the form
        return redirect("img_view", id=id)

    # Fetch all comments for the post, ordered by creation time (latest first)
    comments = post.comments.all().order_by("-created_at")

    # Render the template with post details and comments
    return render(request, "imgview.html", {"post": post, "comments": comments})


#Logout page
@login_required(login_url="/login/")
def logout(request):

    email=request.user.email
    #Getting Datas From Database.
    user_data = get_object_or_404(Datas, email=email)
    
    #Getting Logout Request
    auth_logout(request)
    
    #Getting Logout Time
    current_time = datetime.datetime.now().strftime("%d %A %b %Y %I:%M:%S %p")
    
    subject = "Logout Notification"
    message = f"""
    Hi {user_data.name},
    
    You have been logged out successfully...!!!
    
    Logout Time: {current_time}

    You can log in again using your email and password.

    Best regards,
    Your Team
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  
            [email], 
            fail_silently=False,
        )

        #Sending Success Message.
        messages.success(request, "Logout successful! An email notification has been sent.")
    #Exception Handling Method.
    except Exception as e:
        messages.error(request, f"Logout successful but failed to send email: {e}")
    
    #Redirecting Page To Login.
    return redirect('/login/')