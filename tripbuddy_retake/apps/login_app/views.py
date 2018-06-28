from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import datetime

def index(request):
    return render(request, 'login_app/index.html')

def createUser(request):
	result = User.objects.validateRegistration(request.POST)
	if type(result) is list:
		for error in result:
			messages.error(request, error)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
	return redirect('/home')

def login(request):
	result = User.objects.validateLogin(request.POST)
	if type(result) is str:
		messages.error(request, result)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		return redirect('/home')

def home(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'trips': Trip.objects.all(),
        'user': user,
        'joined' : Trip.objects.filter(joined_by = user) #join user to their trips, #.exclude shows all the trips you haven't joined
    }
    return render(request, 'login_app/home.html', context)

def addtrip(request): 
    return render(request, 'login_app/add_trip.html')

def post(request):
    errors = Trip.objects.validateDestination(request.POST)
    user = User.objects.get(id=request.session['user_id'])
    if len(errors) > 0:
        for error in errors:
            messages.error(request, errors)
        return redirect('/addtrip')
    
    else:
        
        trips = Trip.objects.create(
            destination=request.POST['destination'],
            desc=request.POST['desc'],
            travel_from = datetime.datetime.strptime(request.POST['travel_from'], '%Y-%m-%d'),
            travel_to = datetime.datetime.strptime(request.POST['travel_to'], '%Y-%m-%d'),
            uploader= User.objects.get(id=request.session['user_id'])
        ).joined_by.add(user)
        return redirect('/home')

def joined(request, trip_id):
    this_trip = Trip.objects.get(id=trip_id)
    this_user= User.objects.get(id=request.session['user_id'])
    this_trip.joined_by.add(this_user)
    this_trip.save()
    return redirect('/home')

def cancel(request, trip_id):
    this_trip = Trip.objects.get(id=trip_id)
    this_user= User.objects.get(id=request.session['user_id'])
    this_trip.joined_by.remove(this_user)
    this_trip.save()
    return redirect('/home')

def user(request, trip_id):
    context = {
        'trips' : Trip.objects.filter(id=trip_id),
    }
    return render(request, 'login_app/user.html', context)

def edit(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'login_app/edit.html', context)

def update(request, user_id):
    user = User.objects.get(id=request.POST['user_id'])
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return redirect('/home')


def delete(request, trip_id):
    this = Trip.objects.get(id=trip_id)
    this.delete()
    return redirect('/home')


def logout(request):
    request.session.clear()
    return redirect('/')


