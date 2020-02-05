from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .models import Notification
from .forms import LoginForm


def show_notification(request, notification_id):
    n = Notification.objects.get(id=notification_id)
    return render_to_response('notification.html', {'notification': n})


def delete_notification(request, notification_id):
    n = Notification.objects.get(id=notification_id)
    n.viewed = True
    n.save()

    return HttpResponseRedirect('/loggedin')


def loggedin(request):
    n = Notification.objects.filter(user=request.user, viewed=False)
    return render_to_response('loggedin.html',
                              {
                                  'full_name': request.user,
                                  'notifications': n,
                              })

def loginView(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        print(request.POST)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/loggedin')

    return render(request, 'login.html', context={'form': form})


def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/login')
    