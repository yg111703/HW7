from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from .models import * # Post 모델을 불러온다 

def home(request):
    posts = FreePost.objects.all()
    return render(request,'index.html', {'posts': posts})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        userid = request.POST['username']
        userpw = request.POST['password']

        user = auth.authenticate(request, username=userid, password=userpw)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html')
        
def logout(request):
    auth.logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    else:
        userid = request.POST['username'] # input의 name 값 
        userpw = request.POST['password']
        # 회원가입 
        new_user = User.objects.create_user(username=userid, password=userpw)
        # 로그인 
        auth.login(request, new_user) # 파라미터: request와 유저 객체 
        return redirect('home')

def create(request):
    # 1. GET 요청
    if request.method == 'GET':
        return render(request, 'create.html')
    # 2. POST 요청 
    else:
        # Post 객체 생성
        post = FreePost()  
        # 속성 할당 
        post.title = request.POST['title']
        post.body = request.POST['body']
        post.author = request.user
        post.save()
        # 홈화면으로 redirect
        return redirect('home')

def detail(request, id):
    freepost = get_object_or_404(FreePost, pk = id)
    return render(request, 'detail.html', {'freepost': freepost})

def edit(request):
    edit_freepost = FreePost.objects.get(id=id)
    return render(request, 'edit.html', {'freepost':edit_freepost})

def update(request, id):
    update_freepost = FreePost.ojbects.get(id = id)
    update_freepost.title = request.POST['title']
    update_freepost.author = request.POST['writer']
    update_freepost.body = request.POST['body']
    update_freepost.save()
    return redirect('detail', update_freepost.id)

def delete(request, id):
    delete_freepost = FreePost.objects.get(id = id)
    delete_freepost.delete()
    return redirect('home')