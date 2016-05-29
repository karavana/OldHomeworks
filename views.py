import json
import socket
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User

from .forms import AddPlaceForm, AddEventForm, LoginForm, CreateForm, ChangeRegionForm
#TODO: Add and Change functions wil be Form Submit
#TODO: Createuser function with Django user id - server side debug

HOST = 'localhost'
PORT = 5001
# Create your views here.
users = []
user_count = 0
def createview(request):
	global user_count
	global users
	if request.method == 'POST':
		form = CreateForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			print str(username),str(password)
			command = "createuser enduser" + " " + str(username) + " " + str(password)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	                s.connect((HOST,PORT))
			s.send(command)
			uid = user_count
			print str(uid)
			user_count += 1
			s.close()
			users.append((username,password,uid))
			try:
				user = User.objects.create_user(username=username,password=password)
			except:
				print "exist on db"
			return HttpResponseRedirect("/hood/login/")
		else:
			return render(request,"create.html",{'form':form,'state':'fail'})
	else:
		form = CreateForm()
		return render(request,"create.html",{'form':form})

def loginview(request):
	global users
	if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']
			print str(users)
                        for utuple in users:
				if utuple[0] == username and utuple[1] == password:
					user = authenticate(username=username,password=password)
					login(request,user)
					return HttpResponseRedirect("/hood")
                        return HttpResponseRedirect("/hood/login/")
                else:
                        return render(request,"login.html",{'form':form,'state':'fail'})
        else:
                form = LoginForm()
                return render(request,"login.html",{'form':form})

def logoutview(request):
	logout(request)
	return HttpResponseRedirect("/hood/login/")

@login_required(login_url="/hood/login/")
def places(request):
	global users
	user   = request.user
	places = ""
	if request.method == 'POST':
		form = AddPlaceForm(request.POST)
		if form.is_valid():
			xcoord = form.cleaned_data['xcoord']
			ycoord = form.cleaned_data['ycoord']
			addr   = form.cleaned_data['address']
			name   = form.cleaned_data['name']
			for utuple in users:
				if utuple[0] == user.username:
					u_id = utuple[2]
					command = "addplace" + " " + str(xcoord) + "," + str(ycoord) + " " + str(addr) + " " + str(name) + " " + str(u_id)
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        		s.connect((HOST,PORT))
                        		s.send(command)
					s.close()
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.connect((HOST,PORT))
					command = "getplaces" + " " + str(u_id)
					s.send(command)
					places = s.recv(1024).split()
					s.close()
			return render(request,"places.html",{'form':form,'message':'success','places':places,'user':user.username})
		else:
			return render(request,"places.html",{'form':form,'message':'fail','places':places,'user':user.username})
	else:
		form = AddPlaceForm()
		for utuple in users:
				if utuple[0] == user.username:
					u_id = utuple[2]
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.connect((HOST,PORT))
					command = "getplaces" + " " + str(u_id)
					s.send(command)
					places = s.recv(1024).split()
					print places
					s.close()
		return render(request,"places.html",{'form':form, 'places':places, 'user':user.username});

@login_required(login_url="/hood/login/")
def events(request):
	user = request.user
	if request.method == 'POST':
                form = AddEventForm(request.POST)
                if form.is_valid():
                        # Process
                        return render(request,"events.html",{'form':form,'message':'success','user':user.username})
                else:
                        return render(request,"events.html",{'form':form,'message':'fail','user':user.username})
        else:
                form = AddEventForm()
                return render(request,"events.html",{'form':form,'user':user.username});

@login_required(login_url="/hood/login/")
def home(request):
	global users
	user = request.user
	uname = user.username
	if request.method == 'POST':
		form = ChangeRegionForm(request.POST)
		if form.is_valid():
			xmin = form.cleaned_data['xcoord_min']
			ymin = form.cleaned_data['ycoord_min']
			xmax = form.cleaned_data['xcoord_max']
			ymax = form.cleaned_data['ycoord_max']
			for utuple in users:
				print utuple[0]
                                if utuple[0] == user.username:
                                        u_id = utuple[2]
					command = "changeregion" + " " + str(xmin) + "," + str(ymin) + " " + str(xmax) + "," + str(ymax) + " " + str(u_id)
					print command
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			                s.connect((HOST,PORT))
					s.send(command)
			return render(request, "homepage.html",{'user':uname,'form':form,'state':'success'})
		else:
			return render(request, "homepage.html",{'user':uname,'form':form,'state':'fail'})
	else:
		form = ChangeRegionForm()
		return render(request,"homepage.html",{'user':uname,'form':form});


# AJAX views
def show(request):
	if request.method == "GET":
                print request.GET
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST,PORT))
                s.send("show")
                users = s.recv(1024)
		users_on_map = s.recv(1024)
		places = s.recv(1024)
		events = s.recv(1024)
                s.close()
                return HttpResponse(json.dumps({"users":users,"users_on_map":users_on_map,"events":events,"places":places}),
                                content_type="application/json")
        else:
                return HttpResponse("Cant POST here")

def get_places(request):
	if request.method == "GET":
		print request.GET
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST,PORT))
		command = "getplaces" + str(user_id)
		s.send(command)
		places = s.recv(1024)
		s.close()
		return HttpResponse(json.dumps({"places":places}),
				content_type="application/json")
	else:
		return HttpResponse("Cant POST here")

def get_events(request):
	if request.method == "GET":
                print request.GET
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST,PORT))
                command = "getevents" + str(user_id)
                s.send(command)
                events = s.recv(1024)
                s.close()
                return HttpResponse(json.dumps({"events":events}),
                                content_type="application/json")
        else: 
                return HttpResponse("Cant POST here")
