from apps.dashboardApp.models import UserMoreInfo
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from datetime import datetime, timedelta
from ..loginApp.models import User
from ..loginApp.views import addToDB, updateUserOnDB
from django.contrib import messages
from django.utils import timezone
import math


#CRUD

def updateUserMoreInfoOnDB(user_id,user_data):
    user = UserMoreInfo.objects.get(user_id = user_id)
    if "description" in user_data:
        user.description = user_data["description"]
    if "user_level" in user_data:
        user.user_level = user_data['user_level']
    user.save()

#ROUTES:

def gotoDashboard(request):

    if ("id" not in request.session) or (request.session["id"] <= 0):
        request.session["id"] = 0
        return redirect('/signin')

    level_name = User.objects.get(id = request.session["id"]).user_proxy.level_name

    #check path user or admin (por si se pone a mano en el navegador)
    if (request.path == "/dashboard/admin" and level_name == "normal"):
        return redirect('dashboard')
    elif (request.path == "/dashboard" and level_name == "admin"):
        return redirect('dashboard_admin')

    context = {
        'tipo' : level_name,
        'users' : User.objects.all(),
    }
    return render(request,"dashboard.html",context)


def editUser(request):

    if ("id" not in request.session) or (request.session["id"] <= 0):
        return redirect('signin')

    return renderUser(request,User.objects.get(id = request.session["id"]))


def editUserByAdmin(request,user_id):

    if ("id" not in request.session) or (request.session["id"] <= 0):
        return redirect('signin')

    return renderUser(request,User.objects.get(id = user_id))


def renderUser(request,user):

    context = {
        "tipo" : User.objects.get(id = request.session["id"]).user_proxy.level_name,
        "user" : user,
    }

    return render(request,"user_edit.html",context)


def updateUser(request): 

    if ("id" not in request.session) or (request.session["id"] <= 0):
        return redirect('signin')

    logged_user = User.objects.get(id = request.session["id"])
    user_level = logged_user.user_proxy.user_level

    user_to_update = User.objects.get(id = int(request.POST["id"]))

    if user_level < 9 and ( int(request.POST["id"]) != request.session["id"] ):
        return redirect('dashboard') 
    
    tipo = request.POST["tipo"] #tipo: datagral, pass, descrip
    if tipo == "descrip" and request.POST["description"] != user_to_update.user_proxy.description:

        user_data = {
            'description' : request.POST["description"]
        }
        updateUserMoreInfoOnDB(user_to_update.id,user_data)

        messages.success(request, f"User {user_to_update.full_name} Description updated!")

    elif tipo == "pass":

        errors = User.objects.password_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

            return renderUser(request,user_to_update) #do not put password...

        else:

            user_data = {
                'password' : request.POST["password"]
            }
            updateUserOnDB(user_to_update.id,user_data)

            messages.success(request, f"User {user_to_update.full_name} Password updated!")

    elif tipo == "datagral":

        print("DATA GRAL!")

        stError = False

        errors = User.objects.datagral_validator(request.POST)
        if len(errors) > 0:
            stError = True
            for key, value in errors.items():
                messages.error(request, value)

        if user_level == 9:
            errors = UserMoreInfo.objects.user_level_validator(request.POST)
            if len(errors) > 0:
                stError = True
                for key, value in errors.items():
                    messages.error(request, value)

        if stError:        
            user_to_update.first_name = request.POST["first_name"]
            user_to_update.last_name = request.POST["last_name"]
            user_to_update.email = request.POST["email"]
            if user_level == 9:
                user_to_update.user_proxy.user_level = int(request.POST["user_level"])
            #nothing has been saved/updates, this is just for rendering with current values on the form

            return renderUser(request,user_to_update)
    
        else:

            user_data = {
                'first_name' : request.POST["first_name"],
                'last_name' : request.POST["last_name"],
                'email' : request.POST["email"],
            }

            if user_level == 9:
                user_data['user_level'] = int(request.POST["user_level"])

            print(f"userdata: {user_data}")

            updateUserOnDB(user_to_update.id,user_data)
            updateUserMoreInfoOnDB(user_to_update.id,user_data)

            messages.success(request, f"User {user_to_update.full_name} General Info updated!")

    else:

        return redirect("dashboard")

    updated_user = User.objects.get(id = request.POST["id"])
    return renderUser(request,updated_user)


def removeUserByAdmin(request,user_id):

    response = {}

    if ("id" not in request.session) or (request.session["id"] <= 0):
        response["deleted"] = False
        response["message"] = "No permission!"
        return JsonResponse(response)

    if User.objects.get(id = request.session["id"]).user_proxy.user_level < 9:
        response["deleted"] = False
        response["message"] = "No permission!"
        return JsonResponse(response)

    if user_id == request.session["id"]:
        response["deleted"] = False
        response["message"] = "Cannot delete yourself!"
        return JsonResponse(response)

    user_to_delete = User.objects.get(id = user_id)
    user_to_delete.delete()
    response["deleted"] = True
    print(f"User {user_id} deleted!")
    return JsonResponse(response)
        

def newUser(request):

    if ("id" not in request.session) or (request.session["id"] <= 0):
        request.session["id"] = 0
        return redirect('signin')

    user_level = User.objects.get(id = request.session["id"]).user_proxy.user_level
    if user_level < 9:
        return redirect('dashboard') 

    context = {
        'tipo' : 'create_user',
    }

    if request.method == 'POST': #esto para evitar que se entre directo a esta ruta
        
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value) 

            context.update({
                'email' : request.POST['email'],
                'first_name' : request.POST['first_name'],
                'last_name' : request.POST['last_name'],
                'password' : request.POST['password'],
                'confirm_password' : request.POST['confirm_password'],
            })

        else:
            id_user, id_more = addToDB(
                request.POST['email'],
                request.POST['first_name'],
                request.POST['last_name'],
                request.POST['password']
            )

            #en este caso no se agrega nada al context para mantenerse creando más usuarios nuevos en la misma página

            messages.success(request, f"User {request.POST['first_name']} {request.POST['last_name']} successfully created! [Id:{ id_user }]")
    
    return render(request,'register.html',context)

