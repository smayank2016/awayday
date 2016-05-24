# Create your views here.
from AwayDayApp.models import *  
from django.shortcuts import render, HttpResponse
import json
import httplib2
    
def add(request,):

    params = request.POST;
    # print params;
    name = params.get("name");
    email = params.get("emailid");
    
    user = User(email=email, first_name=name);
    user.save();
    
    
    return render(request, "home.html", {"message" : "User added", "users":User.objects()});
    
def view(request,):
    credentials = request.session['credentials'];
    # print user_info;
    return render(request, "home.html", {"users":User.objects.all()})

def delete(request,):
    params = request.GET;
    name = params.get("name");
    User.objects(first_name=name).delete();
    return render(request, "home.html", {"message" : "User deleted", "users":User.objects()});

def users(request,):
    userlist = [];
    userslist = User.objects.all();
    for user in userslist:
        userlist.append({"name":str(user.first_name), "emailid":str(user.email)});
    return HttpResponse(json.dumps(userlist), content_type="application/json")
