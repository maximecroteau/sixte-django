from django.shortcuts import render
from django.contrib.auth import authenticate, login

from .forms import CreateAd
from .forms import SignUpForm
from .forms import CreateTeam

from .models import Ad
from .models import Team


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


def create_team(request, id):
    ad = Ad.objects.get(id=id)
    form = CreateTeam(request.POST)
    if form.is_valid():
            form.save()
            ads = Ad.objects.all()
            return render(request, 'menu/home.html', {
                'ads': ads
                })
    else:
        form = CreateTeam()
    return render(request, 'menu/createteam.html', {
        'form': form,
        'ad': ad,
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


def view_team(request, id):
    teams = Team.objects.filter(ad__id=id)
    return render(request, 'menu/teams.html', {
        'teams': teams,
    })


def my_teams(request):
    user = request.user
    teams = Team.objects.filter(creator=user)
    return render(request, 'menu/myteams.html', {
        'teams': teams,
    })


def edit_team(request, id):
    user = request.user
    edit_team = Team.objects.get(id=id)
    form = CreateTeam(request.POST, instance=edit_team)
    if form.is_valid():
            form.save()
            teams = Team.objects.filter(creator=user)
            return render(request, 'menu/myteams.html', {
                'teams': teams
                })
    else:
        form = CreateTeam()
    return render(request, 'menu/editteam.html', {
        'edit_team': edit_team,
        'form': form,
        })
