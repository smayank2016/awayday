# Create your views here.
from AwayDayApp.models import *  
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
import json
from AwayDay.settings import flow
from apiclient.discovery import build
import httplib2
import os

def login(request,):  
    auth_uri = flow.step1_get_authorize_url();
    return redirect(auth_uri);

def home(request,):  
    params = request.GET;
    code = params.get("code");
    credentials = flow.step2_exchange(code);
    
    request.session['credentials'] = credentials;
    return redirect("/AwayDayApp/view");
    
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
    http_auth = credentials.authorize(httplib2.Http());
    # print credentials;
    user_info_service = build(
      serviceName='oauth2', version='v2',
      http=http_auth);
    user_info = user_info_service.userinfo().get().execute();
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
