from django.shortcuts import render, redirect

from chat_app.models import UserChat


def index(request):
    if request.user.is_authenticated:
        return render(request, "chat/index.html", {"user": request.user})
    return redirect('login')


def room(request, room_name):
    if request.user.is_authenticated:
        messages = UserChat.objects.filter(group_name=room_name)

        return render(request, "chat/room.html", {"message": messages,
                                                  "room_name": room_name,
                                                  "user": request.user.username
                                                  })
    return redirect('login')
