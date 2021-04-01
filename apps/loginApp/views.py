from apps.dashboardApp.models import UserMoreInfo
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User
import bcrypt
from django.contrib import messages

DATE_FORMAT = "%Y-%m-%d"
SESSION_KEYS = [
    'id',
]


#SESSION
def resetSession(request):
    for key in SESSION_KEYS:
        if key in request.session:
            del request.session[key]
    request.session["id"] = 0 #initialize

#CRUD

def updateUserOnDB(user_id,user_data):
    user = User.objects.get(id = user_id)
    if "first_name" in user_data:
        user.first_name = user_data["first_name"]
    if "last_name" in user_data:
        user.last_name = user_data["last_name"]
    if "email" in user_data:
        user.email = user_data["email"]
    if "password" in user_data:
        user.password = passEncryptDecoded(user_data["password"])
    user.save()

def addToDB(email,first_name,last_name,password):

    user = User.objects.create(
        email = email,
        first_name = first_name,
        last_name = last_name,
        password = passEncryptDecoded(password),
    )

    #create userMoreInfo
    if User.objects.all().count() == 1:
        user_level = 9
    else:
        user_level = 1

    print(f"user_level:{user_level}")

    user_proxy = UserMoreInfo.objects.create(
        user = user,
        user_level = user_level,
        description = '',
    )

    return user.id, user_proxy.id

#MISC FUNCTIONS
def passEncryptDecoded(passwd):
    return bcrypt.hashpw(passwd.encode(),bcrypt.gensalt()).decode()

#ROUTES
def gotoIndex(request):
    return render(request,'index.html')

def gotoLogin(request):

    if "id" not in request.session:
        request.session["id"] = 0

    if request.session["id"] > 0:
        return showSuccess(request)

    elif request.method == 'POST': #esto para evitar que se entre directo a esta ruta
            
            errors = User.objects.login_validator(request.POST)
            
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)

                    context = {
                        'email' : request.POST['email'],
                        'password' : request.POST['password']
                    }

                return render(request,'login.html',context)

            else:
                request.session["id"] = User.objects.get(email = request.POST["email"]).id

                print(f"login! {request.session['id']}")

                return showSuccess(request)

    return render(request,'login.html') #GET method, i.e. first time in login


def showSuccess(request):

    if "id" not in request.session:
        request.session["id"] = 0

    if request.session["id"] > 0:

        if UserMoreInfo.objects.get(user_id = request.session["id"]).user_level == 9:
            return redirect('dashboard_admin') #goto dashboardApp as Admin
        else:
            return redirect('dashboard') #goto dashboardApp as Normal

    else:
        return redirect('signin')


def gotoRegister(request):

    if request.session["id"] > 0: #en caso de entrar directo, usuario logeado se va al success
        return showSuccess(request)

    if request.method == 'POST': #esto para evitar que se entre directo a esta ruta
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value) 

            context = {
                'email' : request.POST['email'],
                'first_name' : request.POST['first_name'],
                'last_name' : request.POST['last_name'],
                'password' : request.POST['password'],
                'confirm_password' : request.POST['confirm_password'],
            }
            
            return render(request,'register.html',context) #go back to "register" keeping data

        else:
            id_user, id_more = addToDB(
                request.POST['email'],
                request.POST['first_name'],
                request.POST['last_name'],
                request.POST['password'],
            )
            messages.success(request, f"User {request.POST['first_name']} {request.POST['last_name']} successfully created!")
            
            request.session['id'] = id_user

            return showSuccess(request)
    
    return render(request,'register.html') #Es GET (primera entrada)

def signOut(request):
    resetSession(request)
    return redirect('home')

def checkEmail(request):

    if "id" in request.POST and int(request.POST["id"]) > 0:
        errors = User.objects.email_validator(request.POST["email"],"register",request.POST["id"])
    else:
        errors = User.objects.email_validator(request.POST["email"],"register")

    return JsonResponse(errors)