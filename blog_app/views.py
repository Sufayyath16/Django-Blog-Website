from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages,auth
from django.contrib.auth.models import User
from.models import *
from django.core.mail import send_mail
from django.conf import settings

from django.core.validators import EmailValidator,RegexValidator
from django.core.exceptions import ValidationError



# Create your views here.
#SIGN IN
def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,"Successfully Signed In")
            return redirect('/home/')
           
        else:
            messages.error(request,"Invalid details")
            return redirect('/')
    return render(request,"login.html")
    

# for validation
def validate_username(value):
    if not value:
        raise ValidationError("Username cannot be empty.")
    if len(value)<3 or len(value)>30:
        raise ValidationError("Username must be between 3 and 30 characters.")
    

    
def validate_email(value):
    if not value:
        raise ValidationError("Email cannot be empty.")
    email_validator=EmailValidator("Enter a valid email address.[Hint: abc@gmail.com]")
    email_validator(value)

#SIGNUP
def signup(request):
    if request.method=="POST":
        user_name=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password']
        password2=request.POST['confirmpwd']

        try:
            validate_username(user_name)
            validate_email(email)
        except ValidationError as e:
            messages.error(request,e.message)
            return redirect('/signup/')

        if password1==password2:
            if User.objects.filter(username=user_name).exists():
                messages.error(request,"Username already taken")
                return redirect('/signup/')
            elif User.objects.filter(email=email).exists():
                messages.error(request,"Email already taken")
                return redirect('/signup/')
            else:
                user=User.objects.create_user(username=user_name,email=email,password=password1)
                user.save()
        else:
            messages.error(request,"Password not matched")
            return redirect('/signup/')
        return redirect('/')
    return render(request,"signup.html")


def home(request):
    blog=Blog.objects.all()
    return render(request,"home.html",{'blog':blog})

def about(request):
    return render(request,"aboutus.html")

#send the details entered by user in contact form to mail of admin
def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        contact=request.POST['contact']
        message=request.POST['comments']

        send_mail('Comments',
                  f'Name: {name}\nEmail: {email} \nContact No: {contact} \nMessage: {message}',
                  settings.EMAIL_HOST_USER,
                  ['sufayyasufi16@gmail.com'],
                  fail_silently=False)
        messages.success(request,"Message sent successfully")
    return render(request,"contact.html")

def logout(request):
    return render(request,"login.html")
  

def blogcontent(request,id):
    blog=get_object_or_404(Blog,id=id)
    comment=Comment.objects.filter(blog=blog).order_by("-id")
    reply=Reply.objects.filter(commentParent__blog=blog)
    return render(request,"blogcontent.html",{'blog':blog,'comment':comment,'reply':reply})


#comments under blog
def comment(request):
    if request.method=="POST":
        name=request.user
        blogid=request.POST.get('blogid')
        comment=request.POST.get('comment')
        blog=Blog.objects.get(id=blogid)
        comment=Comment(blog=blog,name=name,comment=comment)
        comment.save()
        messages.success(request,"Comment successfully added")
        # print(comment)
    return redirect(f"/blogcontent/{blogid}")


#replies of each comment
def reply(request):
    if request.method=="POST":
        name=request.user
        blogid=request.POST.get('blogid')
        reply=request.POST.get('reply')
        commentParent=request.POST.get('commentparent')
        print(name,commentParent,reply,blogid)
        comment=Comment.objects.get(id=commentParent)
        
        reply=Reply(commentParent=comment,name=name,reply=reply)
        reply.save()
        messages.success(request,"Reply successfully added")
    return redirect(f"/blogcontent/{blogid}")
        




