# Create your views here.
from django.shortcuts import render, redirect
from AwayDay.settings import flow
from apiclient.discovery import build
import httplib2

def login(request,):  
    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)

def home(request,):  
    params = request.GET
    code = params.get("code")
    error = params.get("error")
    if(error != None):
        return redirect("/?message=loginfailed")
    credentials = flow.step2_exchange(code)
    if(credentials == None):
        return redirect("/?message=loginfailed")
    http_auth = credentials.authorize(httplib2.Http())
    # print credentials
    user_info_service = build(
      serviceName='oauth2', version='v2',
      http=http_auth)
    user_info = user_info_service.userinfo().get().execute()
    if(not user_info.get("email").endswith("@thoughtworks.com")):
        return redirect("/?message=notthoughtworks")
    request.session['user_info'] = user_info
    return redirect("/")

def index(request,):
    message = ""
    if(request.GET.get("message")=="notthoughtworks"):
        message = "You need a thoughtworks id"
    elif(request.GET.get("message")=="loginfailed"):
        message = "Your login failed. Please try again!"
    return render(request, "home.html", {"message":message})

def logout(request,):
    del request.session['user_info']
    
    return redirect("/")
    

