from django.contrib.auth.decorators import login_required
from django.template import loader

from .models import User

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.forms import UserCreationForm


@login_required
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_authenticated:
                    login(request, user)
                    return redirect('main')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'appcoworking/login.html', {'form': form})

def user_logout(redirect):
    logout(redirect)
    return redirect('login')

def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.firstname = form.cleaned_data.get('firstname')
            user.lastname = form.cleaned_data.get('lastname')
            user.phone = form.cleaned_data.get('phone')
            user.joined_date = form.cleaned_data.get('joined_date')
            user.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'appcoworking/registration.html', {'form': form})

def main_view(request):
    return render(request, 'main.html', {'user': request.user})

def users(request):
    myusers = User.objects.all().values()
    template = loader.get_template('all_users.html')
    context = {
        'myusers': myusers,
    }
    return HttpResponse(template.render(context, request))


def details(request, id):
    myuser = User.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'myuser': myuser,
    }
    return HttpResponse(template.render(context, request))


def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())


def testing(request):
    template = loader.get_template('template.html')
    context = {
        'Коворкинг': ['Рабочие места', 'Мини офисы', 'Конференц зал', 'Переговорные', 'Аренда компьютеров', 'Печать', 'Администратор'],
    }
    return HttpResponse(template.render(context, request))



