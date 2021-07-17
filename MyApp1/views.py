from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from . models import Blog
from  . Forms import Edit_Blog

# Create your views here.
def index(request):
        blog = Blog.objects.all()
        context = { 'blogs' : blog }
        return render(request,'Home.html',context)

def user_register(request):
        if request.method == "POST" :
                        fname = request.POST.get('firstname')
                        lname = request.POST.get('lastname')
                        uname = request.POST.get('username')
                        email = request.POST.get('email')
                        pass1 = request.POST.get('password1')
                        pass2 = request.POST.get('password2')


                        if pass1!=pass2:
                                messages.warning(request,'Password does not matched')
                                return redirect('register')
                        elif User.objects.filter(username=uname).exists():
                                messages.warning(request,'Username is allready exists')
                                return redirect('register')
                        elif User.objects.filter(email=email).exists():
                                messages.warning(request,'Email is allready exists')
                                return redirect('register')
                        else:
                                user = User.objects.create_user(first_name=fname,last_name=lname,username=uname,email=email,password=pass1)
                                user.save()
                                messages.success(request,'User has been Registered successfully...')
                                return redirect('login')

        return render(request,'Register.html')

def user_login(request):
        if request.method == "POST" :
                        username = request.POST.get('username')
                        password = request.POST.get('password')
                        user = authenticate(request,username=username,password=password)
                        if user is not None:
                                login(request,user)
                                return redirect('/')
                        else:
                                messages.warning(request,'Invalid Credentials has been entered')
                                return redirect('login')


        return render(request,'Login.html')

def user_logout(request):
        logout(request)
        return redirect('/')

def post_blog(request):

        if request.method == 'POST':
                title = request.POST.get('title')
                desc = request.POST.get('description')
                blog = Blog(title=title, dsc=desc, user_id=request.user)
                blog.save()
                messages.success(request,'Post has been stored successfully...')
                return redirect('post_blog')

        return render(request,'Posts.html')

def blog_detail(request,id):
        blog = Blog.objects.get(id = id)
        context = {'blog':blog}
        return render(request,'Blog Details.html',context)

def delete(request,id):
        blog = Blog.objects.get(id = id)
        blog.delete()
        messages.success(request,'Post has been deleted successfully...')
        return redirect('/')

def edit(request,id):
        blog = Blog.objects.get(id = id)
        editblog = Edit_Blog(instance = blog)
        if request.method=='POST':
                form = Edit_Blog(request.POST,instance = blog)
                if form.is_valid():
                        form.save()
                        messages.success(request,'Post has been updated successfully...')
                        return redirect('/')
        return render(request,'Edit Blog.html',{'edit_blog':editblog})
       