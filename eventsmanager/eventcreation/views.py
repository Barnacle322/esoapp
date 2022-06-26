from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

from .models import Event
from .forms import EventForm
# Create your views here.

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('event_manager')
        else:
            messages.error(request, "Invalid credentials")

    context = {'page': page}
    return render(request, 'eventcreation/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('event_manager')
        else:
            messages.error(request, "Registration error")

    context = {'form': form}
    return render(request, 'eventcreation/login_register.html', context)

def event_create(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_manager')
    context = {'form': form}
    return render(request, 'eventcreation/event_create.html', context)

@login_required(login_url='login')
def event_update(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_manager')
    context = {'form': form, 'event': event}
    return render(request, 'eventcreation/event_update.html', context)

@login_required(login_url='login')
def event_delete(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_manager')
    context = {'event': event}
    return render(request, 'eventcreation/event_delete.html', context)

def event_manager(request):
    events = Event.objects.all().order_by('-start_time')
    context = {'events': events}
    return render(request, 'eventcreation/event_manager.html', context)