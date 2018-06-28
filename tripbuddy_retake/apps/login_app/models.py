from django.db import models
import bcrypt, re, datetime
from django.core.validators import MinLengthValidator

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def validateRegistration(self, postData):
        errors = []
        existing_user = User.objects.filter(email=postData['email'])
        if len(postData['first_name']) < 1:
            errors.append("first name is too short")
        if len(postData['last_name']) < 1:
            errors.append('Last name is too short')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Please enter a valid email')
        if len(existing_user):
            errors.append('This email already exists')
        if len(postData['pw']) < 8:
            errors.append("Password must be at least 8 characters")
        if postData['pw'] != postData['cpw']:
            errors.append('Passwords don"t match')
        if len(errors):
            return errors
        me = User.objects.create(
            first_name=postData['first_name'],
            last_name=postData['last_name'],
            email=postData['email'],
            password= bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt())
            )
        return me

    def validateLogin(self, postData):
        errors = []
        existing_user_list = User.objects.filter(email=postData['email'])
        if len(existing_user_list):
            if bcrypt.checkpw(postData['pw'].encode(), existing_user_list[0].password.encode()):
                return existing_user_list[0]
        return 'invalid email / password combination'

class TripManager(models.Manager):
    def validateDestination(self, postData):
        errors = []
        print(postData)
        if len(postData['destination']) < 1:
            errors.append('Must have an entry!')
        if len(postData['desc']) < 1:
            errors.append('Must have an entry!')
        if postData['travel_from'] < str(datetime.datetime.now()):
            errors.append('Start date must be in the future')
        if postData['travel_from'] > postData['travel_to']:
            errors.append('End date must be after start date')
        return errors
        
        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    travel_from = models.DateTimeField()
    travel_to = models.DateTimeField()
    uploader = models.ForeignKey(User, related_name='uploaded_trips')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    joined_by = models.ManyToManyField(User, related_name='joined_trips')
    objects = TripManager()



