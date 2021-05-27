from django.db import models
import re
# Create your models here.

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['firstName']) < 2:
            errors['firstName'] = "First name must have at least 2 characters"
        
        if len(form['lastName']) < 2:
            errors['lastName'] = "Last name must have at least 2 characters"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Format'
        
        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email address is already in use'

        usernameCheck = self.filter(username=form['username'])
        if usernameCheck:
            errors['username'] = 'Sorry that username is already in use'

        if len(form['password']) < 5:
            errors['password'] = 'Password must be atleast 5 characters in length'

        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        
        return errors

# def authenticate(self, email, password):
#     users = self.filter(email=email)
#     if not users:
#         return False
    
#     user = users[0]
#     return bcrypt.checkpw(password.encode(), user.password.encode())

# def register(self, form):
#     pw = bcrypt.ha  

class User(models.Model):
        firstName = models.CharField(max_length=45)
        lastName = models.CharField(max_length=45)
        email = models.EmailField(unique=True)
        username = models.CharField(max_length=45)
        password = models.CharField(max_length=45)
        objects = UserManager()

class Note(models.Model):
        noteTitle = models.CharField(max_length=45)
        noteText = models.CharField(max_length=300)
        user = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)

class Wall_Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name="post_comments", on_delete=models.CASCADE)


         
 

