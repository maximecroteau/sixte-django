from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic.edit import UpdateView

from .forms import CreateAd
from .forms import SignUpForm

from .models import Ad


def home(request):
    ads = Ad.objects.all()
    return render(request, 'menu/home.html', {
        'ads': ads
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            ads = Ad.objects.all()
            return render(request, 'menu/home.html',{
                'ads': ads
            })
    else:
        form = SignUpForm()
    return render(request, 'signup/signup.html', {
        'form': form
    })


def create_ad(request):
    form = CreateAd(request.POST)
    if form.is_valid():
            form.save()
            ads = Ad.objects.all()
            return render(request, 'menu/home.html', {
                'ads': ads
                })
    else:
        form = CreateAd()
    return render(request, 'menu/createad.html', {
        'form': form,
        })


def del_ad(request, id):
    ad_del = Ad.objects.get(id=id)
    ad_del.delete()
    ads = Ad.objects.all()
    return render(request, 'menu/myad.html', {
        'ads': ads
        })


def edit_ad(request, id):
    ads_edits = Ad.objects.get(id=id)
    form = CreateAd(request.POST, instance=ads_edits)
    if form.is_valid():
            form.save()
            ads = Ad.objects.all()
            return render(request, 'menu/home.html', {
                'ads': ads
                })
    else:
        form = CreateAd()
    return render(request, 'menu/editad.html', {
        'ads_edits': ads_edits,
        'form': form,
        })


def my_ad(request):
    user = request.user
    ads = Ad.objects.filter(creator=user)
    return render(request, 'menu/myad.html', {
        'ads': ads,
    })