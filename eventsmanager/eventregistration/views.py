from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

from eventcreation.models import Event

from .models import Registration


from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def home(request):
    return render(request, 'eventregistration/home.html')

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
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")

    context = {'page': page}
    return render(request, 'eventregistration/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Registration error")

    context = {'form': form}
    return render(request, 'eventregistration/login_register.html', context)

@login_required(login_url='userLogin')
def event_manager(request):
    events = Event.objects.all().order_by('-start_time')
    registrations = Registration.objects.filter(user=request.user)
    registrations = {registration.event_id:registration.user_id for registration in registrations}
    print(registrations)
    context = {'events': events, 'registrations': registrations}
    return render(request, 'eventregistration/event_manager.html', context)


@login_required(login_url='userLogin')
def event_register(request, pk):
    event = Event.objects.get(pk=pk)
    if request.user.is_authenticated:
        if Registration.objects.filter(event=event, user=request.user).exists():
            messages.error(request, "You have already registered for this event")
            return redirect('home')
        else:
            Registration.objects.create(event=event, user=request.user)
            messages.success(request, "You have successfully registered for this event")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to register for an event")
        return redirect('home')


@login_required(login_url='userLogin')
def event_unregister(request, pk):
    event = Event.objects.get(pk=pk)
    if request.user.is_authenticated:
        if Registration.objects.filter(event=event, user=request.user).exists():
            Registration.objects.filter(event=event, user=request.user).delete()
            messages.success(request, "You have successfully unregistered for this event")
            return redirect('home')
        else:
            messages.error(request, "You have not registered for this event")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to unregister for an event")
        return redirect('home')

@login_required(login_url='userLogin')
def profile(request):
    registrations = Registration.objects.filter(user=request.user)
    context = {'registrations': registrations}
    print(registrations)
    return render(request, 'eventregistration/profile.html', context)