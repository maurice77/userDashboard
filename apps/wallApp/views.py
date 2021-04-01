from apps.wallApp.models import Comment, Message
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
#from .models import Message, Comment
from datetime import datetime, timedelta
from ..loginApp.models import User
from django.utils import timezone
import math


def created_at_msg(miDateTime):
    timeDiff = timezone.now()-miDateTime #es un timedelta que tiene .days, .seconds, .microseconds
    if timeDiff.seconds < 120:
        return f"Posteado hace 1 minuto"
    elif timeDiff.seconds < 3600:
        minutos, resto = divmod(timeDiff.total_seconds(),60)
        return f"Posteado hace {round(minutos)} minutos"
    elif timeDiff.total_seconds() < 3600*24:
        horas, resto = divmod(timeDiff.seconds,3600)
        minutos = math.floor(resto/60)
        if horas == 1:
            if minutos > 0:
                return f"Posteado hace 1 hora y {minutos} minutos"
            else:
                return "Posteado hace 1 hora"
        elif (horas < 4):
            if minutos > 0:
                return f"Posteado hace {horas} horas y {minutos} minutos"
            else:
                return f"Posteado hace {horas} horas"
        else:
            return f"Posteado hace {round(horas)} horas"
    else:
        return f"Posteado el {miDateTime.strftime('%d-%m-%Y')} a las {miDateTime.strftime('%H:%M')}"

def minutesElapsed(miDateTime):
    return secondsElapsed(miDateTime)/60

def secondsElapsed(miDateTime):
    #miTimePostgres = User.objects.raw("SELECT NOW()")[0]
    #print(f"postgres NOW: {miTimePostgres}")
    #print(f"postgres: {miDateTime}")
    #print(f"now: {datetime.now()}")
    
    #now = timezone.now()

    timeDiff = timezone.now()-miDateTime #es un timedelta que tiene .days, .seconds, .microseconds
    return timeDiff.total_seconds()

def wallIndex(request,id):

    if ("id" not in request.session) or (request.session["id"] <= 0):
        return redirect('signin')

    context = {
        "messages" : Message.objects.filter(user_for_id = id).order_by('-created_at'),
        "user" : User.objects.get(id = id),
        #"user_poster" : User.objects.get(id = request.session["id"]),
    }
    return render(request,'wall.html',context)

def postMessage(request):
    
    message = request.POST["message"]

    createdMessage = {}

    if message != "":    
        newmessage = Message.objects.create(
            message = message,
            user_id = request.session["id"],
            user_for_id = request.POST["id_for"],
        )
        print("new message posted!")
        if "tipo" in request.POST: #armar el createdMessage
            createdMessage["id"] = newmessage.id
            createdMessage["message"] = (newmessage.message).replace("<","&lt").replace(">","&gt")
            user = {
                "first_name":newmessage.user.first_name,
                "last_name":newmessage.user.last_name,
                "full_name":newmessage.user.full_name,
                "id":newmessage.user.id,
            }
            createdMessage["user"] = user
            createdMessage["created_at"] = newmessage.created_at
            createdMessage["created_at_text"] = "Hace menos de 1 minuto"

    if "tipo" in request.POST: #js
        print("by ajax")
        return JsonResponse(createdMessage)
    else:
        print("by server")
        return redirect(f"/users/show/{request.POST['id_for']}")


def postComment(request):

    comment = request.POST["comment"]
    
    createdComment = {}

    if comment != "":    
        newcomment = Comment.objects.create(
            comment = comment,
            user_id = request.session["id"],
            message_id = request.POST["message_id"]
        )
        print("new comment posted!")
        if "tipo" in request.POST: #armar el createdComment
            createdComment["id"] = newcomment.id
            
            createdComment["comment"] = (newcomment.comment).replace("<","&lt").replace(">","&gt")
            user = {
                "first_name":newcomment.user.first_name,
                "last_name":newcomment.user.last_name,
                "full_name":newcomment.user.full_name,
                "id":newcomment.user.id,
            }
            createdComment["user"] = user
            createdComment["created_at"] = newcomment.created_at
            createdComment["created_at_text"] = "Hace menos de 1 minuto"

    if "tipo" in request.POST: #js
        print("by ajax")
        return JsonResponse(createdComment)
    else:
        print("by server")
        url = f"/users/show/{request.POST['id_for']}#divcomment-{newcomment.id}"
        return redirect(url)

def delMessage(request):
    
    idMsg = request.POST["message_id"]
    message = Message.objects.get(id = idMsg)

    response = {}

    if secondsElapsed(message.created_at) > 30*60:
        #quit because it is not possible to erase comment after 30mins
        print("Didn't erase message (posted more than 30mins ago!)")
        if "tipo" in request.POST: #js
            response["deleted"] = False
            return JsonResponse(response)
        else:
            url = f"/wall#divmessage-{idMsg}"
            return redirect(url)

    if message.user.id == int(request.session["id"]): #chk que mensaje corresponde al usuario loggeado
        message.delete()
        print(f"Message {idMsg} deleted!")
        response["deleted"] = True

    if "tipo" in request.POST: #js
        print("by ajax")
        return JsonResponse(response)
    else:
        print("by server")
        return redirect(f"/users/show/{request.POST['id_for']}")
        

def delComment(request):
    
    idCom = request.POST["comment_id"]
    comment = Comment.objects.get(id = idCom)

    response = {}

    if secondsElapsed(comment.created_at) > 30*60:
        #quit because it is not possible to erase comment after 30mins
        print("Didn't erased comment (posted more than 30mins ago!)")
        if "tipo" in request.POST: #js
            response["deleted"] = False
            return JsonResponse(response)
        else:
            url = f"/wall#divcomment-{idCom}"
            return redirect(url)

    if comment.user.id == int(request.session["id"]): #chk que mensaje corresponde al usuario loggeado
        comment.delete()
        print(f"Comment {idCom} deleted!")
        response["deleted"] = True

    if "tipo" in request.POST: #js
        print("by ajax")
        return JsonResponse(response)
    else:
        print("by server")
        return redirect(f"/users/show/{request.POST['id_for']}")

def getMsgComCreatedAt(request):
    #necesito: la diferencia de created_at, username
    response = {}
    response["comments"] = {}
    response["messages"] = {}

    messages = Message.objects.all()
    for msg in messages:
        response["messages"][str(msg.id)] = {
            "created_at" : created_at_msg(msg.created_at),
            "minutes" : minutesElapsed(msg.created_at),
        }

    comments = Comment.objects.all()
    for com in comments:
        response["comments"][str(com.id)] = {
            "created_at" : created_at_msg(com.created_at),
            "minutes" : minutesElapsed(com.created_at),
        }

    return JsonResponse(response)

