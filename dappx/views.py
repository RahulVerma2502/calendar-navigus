from django.shortcuts import render, redirect
from dappx.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm


def index(request):
    return render(request, 'dappx/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        # profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid(): # and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors) # , profile_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'dappx/registration.html',
                  {'user_form': user_form,
                   # 'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'dappx/login.html', {})


@login_required
def list_appointment(request):  # this section for my appointment
    user_name = request.user.get_username()  # Getting Username

    # Getting all Post and Filter By Logged UserName
    appointment_list = Appointment.objects.all().order_by("-id").filter(appointment_with=user_name)
    q = request.GET.get("q")  # search start
    if q:
        appointment_list = appointment_list.filter(appointment_with__icontains=q)
    else:
        appointment_list = appointment_list  # search end

    appointments = {
        "query": appointment_list,
        "user_name": user_name
    }
    return render(request, 'dappx/list_appointment.html', appointments)


@login_required
def create_appointment(request):
    user_name = request.user.get_username()  # Getting Username

    # Getting all Post and Filter By Logged UserName
    appointment_list = Appointment.objects.all().order_by("-id").filter(user=request.user)
    q = request.GET.get("q")  # search start
    if q:
        appointment_list = appointment_list.filter(date__icontains=q)
    else:
        appointment_list = appointment_list  # search end

    appointments = {
        "query": appointment_list,
        "user_name": user_name,
        "form": AppointmentForm(),
    }
    form = AppointmentForm(request.POST or None)
    if form.is_valid():
        saving = form.save(commit=False)
        saving.user = request.user
        saving.save()
        messages.success(request, 'Post Created Sucessfully')
    return render(request, 'dappx/create_appointment.html', appointments)


@login_required
def get_appointment(request):
    user_name = request.user.get_username()
    appointment_list = Appointment.objects.all().order_by("-user").exclude(user=request.user)
    q = request.GET.get("q")  # search start
    if q:
        appointment_list = appointment_list.filter(user__first_name__icontains=q)
    else:
        appointment_list = appointment_list  # search end

    appointments = {
        "query": appointment_list,
        "user_name": user_name
    }
    return render(request, 'dappx/get_appointment.html', appointments)


@login_required
def appointment_book(request, id):  # activate after clicking book now button
    user_name = request.user.get_username()
    single_appointment = Appointment.objects.get(id=id)
    form = single_appointment
    form.appointment_with = user_name
    form.save()
    # return HttpResponseRedirect (instance.get_absolute_url())
    # messages.success(request, 'Your profile was updated.')
    return redirect('/dappx/get_appointment/')
