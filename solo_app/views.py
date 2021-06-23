from django.shortcuts import render, HttpResponse, redirect
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'index.html')

def create_user(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            password_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            print(password_hash)
            user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = password_hash,
            )
            request.session['user_signed_in'] = user.id
            return redirect('/dashboard')

def dashboard(request):
    user = User.objects.get(id=request.session['user_signed_in'])
    context = {
        'user_signed_in': User.objects.get(id=request.session['user_signed_in']),
        'all_messages': Message.objects.all(),
        'comments': Comment.objects.all(),
        'user_liked': Message.objects.filter(liked_by=user)
    }
    return render(request,'board.html', context)

def log_in(request):
    if request.method == 'POST':
        user = User.objects.filter(email = request.POST['email'])
        if user:
            this_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), this_user.password.encode()):
                request.session['user_signed_in'] = this_user.id
                return redirect('/dashboard')    
        messages.error(request,"ACCOUNT NOT FOUND, PLEASE VERIFY EMAIL/PASSWORD FIELDS ARE CORRECT")
        return redirect('/')

def log_out(request):
    request.session.flush()
    return redirect('/')

def post_message(request):
    if request.method == 'POST':
        errors = Message.objects.basic_validator(request.POST, request.FILES)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/dashboard')
        else:
            Message.objects.create(
                message = request.POST['message'], 
                message_image = request.FILES.get('image'),
                user_posting = User.objects.get(id=request.session['user_signed_in'])
                )
            return redirect('/dashboard')

def like_post_from_dashboard (request,id):
    user = User.objects.get(id=request.session['user_signed_in'])
    post = Message.objects.get(id=id)
    post.liked_by.add(user)
    return redirect('/dashboard')

def like_post_from_profile (request,id):
    user = User.objects.get(id=request.session['user_signed_in'])
    post = Message.objects.get(id=id)
    post.liked_by.add(user)
    return redirect(f'/dashboard/user/profile/{id}')

def unlike_post(request,id):
    user = User.objects.get(id=request.session['user_signed_in'])
    post = Message.objects.get(id=id)
    post.liked_by.remove(user)
    return redirect(f"/dashboard")

def this_post(request,id):
    user = User.objects.get(id=request.session['user_signed_in'])
    context = {
        'user': user,
        'message': Message.objects.get(id=id),
        'user_not_liked': Message.objects.exclude(liked_by=user)
    }
    return render(request,'this_post.html',context)

def edit_post (request,id):
    if request.method == 'POST':
        errors = Message.objects.update_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect(f'/dashboard/posts/{id}')
        else:
            post = Message.objects.get(id=id)
            post.message = request.POST['message']
            post.save()
            id = id
        return redirect(f'/dashboard/posts/{id}')

def delete_message(request,id):
    post = Message.objects.get(id=id)
    post.delete()
    return redirect("/dashboard")

def post_comment(request, id):
    if request.method == 'POST':
        errors = Comment.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect(f"/dashboard/posts/{id}")
        else:
            Comment.objects.create(
                comment=request.POST['comment'], 
                user_posting = User.objects.get(id=request.session['user_signed_in']),
                message = Message.objects.get(id=id),
                )
            return redirect(f"/dashboard/posts/{id}")

def delete_comment(request,id):
    comment = Comment.objects.get(id=id)
    message_id = comment.message.id
    comment.delete()
    return redirect(f'/dashboard/posts/{message_id}')

def profile(request,id):
    user = User.objects.get(id=id)
    context = {
        'user': user,
        'user_signed_in':User.objects.get(id=request.session['user_signed_in']),
        'all_messages': Message.objects.all(),
        'user_liked': Message.objects.filter(liked_by=user),
        'liked_by_user_signed_in': Message.objects.filter(liked_by=request.session['user_signed_in']),
    }
    return render(request,'profile.html',context)

def edit_profile(request,id):
    user = User.objects.get(id=id)
    context = {
        'user': user,
        'user_signed_in':User.objects.get(id=request.session['user_signed_in']),
    }
    return render(request,'edit_profile.html',context)

def update_profile (request,id):
    if request.method == 'POST':
        errors = User.objects.update_validator(request.POST, request.FILES)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect(f'/dashboard/user/profile/{id}/edit')
        else:
            user = User.objects.get(id=id)
            user.bio = request.POST['bio']
            user.profile_pic = request.FILES.get('pro_pic') or user.profile_pic
            user.save()
        return redirect(f'/dashboard/user/profile/{id}')

def delete_account (request,id):
        user = User.objects.get(id=id)
        user.delete()
        messages.success(request,"ACCOUNT DELETED")
        return redirect(index)


