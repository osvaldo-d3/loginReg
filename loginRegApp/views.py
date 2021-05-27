from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "index.html")

def success(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'wall_messages': Wall_Message.objects.all()
    }
    return render(request, 'success.html', context)

def login(request):
    user = User.objects.filter(username = request.POST
    ['username'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode()
            , userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            return redirect('/dashboard/')
        messages.error(request, 'Invalid Credentials')
        return redirect('/')
    messages.error(request, 'That Username is not in our system, please register for an account')
    return redirect('/success')

def signup(request):
    return render(request, 'register.html')

def register(request):
    if request.method == "GET":
        return redirect('/signup/')
    errors = User.objects.validate(request.POST)
    if errors:
            for err in errors.values():
                messages.error(request, err)
            return redirect('/signup/')
    hashedPw = bcrypt.hashpw(request.POST['password'].
    encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
            firstName = request.POST['firstName'],
            lastName = request.POST['lastName'],
            email = request.POST['email'],
            username = request.POST['username'],
            password = hashedPw
    )
    request.session['user_id'] = newUser.id
    return redirect('/dashboard/') 

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session
    ['user_id'])
    context = {
        'user': user,
        'notes': Note.objects.all().values()
    }
    return render(request, 'dashboard.html', context)

#log out function to clear the session and go back to the home screen
def logout(request):
    request.session.clear()
    return redirect('/')

def createNote(request):
    Note.objects.create(
        noteTitle = request.POST['noteTitle'],
        noteText = request.POST['noteText'],
        user_id=request.POST['user'],
    )
    return redirect('/dashboard/')

def post_mess(request):
    Wall_Message.objects.create(message=request.POST['mess'], poster=User.objects.get(id=request.session['id']))
    return redirect('/success')

def post_comment(request, id):
    #create
    poster = User.objects.get(id=request.session['id'])
    message = Wall_Message.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, wall_message=message)
    return redirect('/success')

def profile(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def add_like(request, id):
    liked_message = Wall_Message.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/success')

def delete_comment(request, id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/success')

def edit(request, id):
    edit_user = User.objects.get(id=id)
    edit_user.first_name = request.POST['firstName']
    edit_user.last_name = request.POST['lastName']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/success')


# Create your views here.
