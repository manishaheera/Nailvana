from django.db import models
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
NAME_REGEX = re.compile(r'^[a-zA-Z ]')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "INVALID FIRST NAME FORMAT"

        if len(postData['first_name']) < 2:
            errors['first_name'] = "FIRST NAME MUST BE ATLEAST 2 CHARACTERS"

        if not NAME_REGEX.match(postData['last_name']):           
            errors['last_name'] = "INVALID LAST NAME FORMAT"
        
        if len(postData['last_name']) < 2:
            errors['last_name'] = "LAST NAME MUST BE ATLEAST 2 CHARACTERS"

        if not EMAIL_REGEX.match(postData['email']):          
            errors['email'] = "EMPTY/INVALID EMAIL ADDRESS FORMAT"
        users_email = User.objects.filter(email=postData['email'])

        if len(users_email) >= 1:
            errors['email_taken'] = 'ACCOUNT WITH EMAIL ALREADY EXISTS'

        if len(postData['password']) < 8:
            errors['password'] = "PASSWORD MUST BE ATLEAST 8 CHARACTERS"
        
        if postData['password'] != postData['confirm_password']:
            errors['match_pw'] = "PASSWORD ENTRIES DO NOT MATCH"
        
        return errors

    def update_validator(self,postData, postFiles):
        errors = {}
        if len(postData['bio']) < 1:
            errors['bio'] = 'USER MUST HAVE BIO'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    profile_pic =models.ImageField(default='default.png', upload_to="images/") 
    bio = models.CharField(null=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class MessageManager(models.Manager):
    def basic_validator(self,postData, postFiles):
        errors = {}
        if len(postData['message']) < 1:
            errors['message'] = 'POST MUST HAVE CONTENT'
        if 'image' not in postFiles:
            errors['image'] = 'POST MUST HAVE IMAGE'
        return errors

    def update_validator(self,postData):
        errors = {}
        if len(postData['message']) < 1:
            errors['message'] = 'POST MUST HAVE CONTENT'
        return errors


class Message(models.Model):
    message = models.CharField(max_length=255)
    message_image =models.ImageField(null=True, blank=True, upload_to="images/") 
    user_posting = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    liked_by= models.ManyToManyField(User, blank=True, related_name="liked_messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class CommentManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData['comment']) < 1:
            errors['comment'] = 'COMMENT CANNOT BE EMPTY'
        return errors

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    user_posting = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='message_comments', on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()




