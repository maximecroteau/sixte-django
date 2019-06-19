from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from friendship.models import Friend
from friendship.models import FriendshipRequest
from django.shortcuts import redirect
from django.db.models import Q
from django.http import HttpResponseRedirect
import datetime

from notifications.signals import notify

from .forms import CreateAd
from .forms import SignUpForm
from .forms import CreateTeam

from .models import Ad
from .models import Team


def notification(request):
    if request.user.is_authenticated:
        user = request.user
        notifs = user.notifications.unread()
    else:
        notifs = ""
    return notifs


def home(request):
    currentdate = datetime.datetime.today().strftime('%Y-%m-%d')
    ads = Ad.objects.all().order_by('-sixte_date').filter(sixte_date__range=[currentdate, "2100-01-01"])
    oldads = Ad.objects.all().order_by('-sixte_date').filter(sixte_date__range=["1900-01-01", currentdate])

    notifs = notification(request)

    return render(request, 'menu/home.html', {
        'ads': ads,
        'oldads': oldads,
        'notifs': notifs,
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup/signup.html', {
        'form': form
    })


def create_ad(request):
    form = CreateAd(request.POST)

    notifs = notification(request)

    if form.is_valid():
        form.save()
        return redirect('home')
    else:
        form = CreateAd()
    return render(request, 'menu/createad.html', {
        'form': form,
        'notifs': notifs,
    })


def create_team(request, id):
    ad = Ad.objects.get(id=id)
    form = CreateTeam(request.POST)

    notifs = notification(request)

    if form.is_valid():
        form.save()
        return redirect('home')

    else:
        form = CreateTeam()
    return render(request, 'menu/createteam.html', {
        'form': form,
        'ad': ad,
        'notifs': notifs,

    })


def del_team(request, id):
    team_del = Team.objects.get(id=id)
    team_del.delete()
    return redirect('my_teams')


def del_ad(request, id):
    ad_del = Ad.objects.get(id=id)
    ad_del.delete()
    return redirect('my_ad')


def edit_ad(request, id):
    ads_edit = Ad.objects.get(id=id)
    form = CreateAd(request.POST, instance=ads_edit)

    notifs = notification(request)

    preset = Ad.objects.get(id=id)
    if form.is_valid():
        form.save()
        return redirect('my_ad')
    else:
        form = CreateAd()
    return render(request, 'menu/editad.html', {
        'ads_edit': ads_edit,
        'preset': preset,
        'form': form,
        'notifs': notifs,
    })


def my_ad(request):
    user = request.user
    notifs = notification(request)

    ads = Ad.objects.filter(creator=user).order_by('-sixte_date')
    return render(request, 'menu/myad.html', {
        'ads': ads,
        'notifs': notifs,
    })


def view_team(request, id):
    teams = Team.objects.filter(ad__id=id)
    notifs = notification(request)

    return render(request, 'menu/teams.html', {
        'teams': teams,
        'notifs': notifs,
    })


def my_teams(request):
    user = request.user
    teams = Team.objects.filter(creator=user)
    notifs = notification(request)

    return render(request, 'menu/myteams.html', {
        'teams': teams,
        'notifs': notifs,
    })


def edit_team(request, id):
    team_edit = Team.objects.get(id=id)
    form = CreateTeam(request.POST, instance=team_edit)
    preset = Team.objects.get(id=id)
    notifs = notification(request)

    if form.is_valid():
        form.save()
        return redirect('my_teams')
    else:
        form = CreateTeam()
    return render(request, 'menu/editteam.html', {
        'notifs': notifs,
        'team_edit': team_edit,
        'preset': preset,
        'form': form,
    })


def friendlist(request):
    # List of this user's friends
    user = request.user
    friends = Friend.objects.friends(user)
    requests = Friend.objects.unread_requests(user=user)
    myasks = Friend.objects.sent_requests(user=user)
    users = User.objects.exclude(friends__from_user=user).exclude(id=user.id) \
        .exclude(friendship_requests_received__from_user=user)

    notifs = notification(request)

    return render(request, 'profil/friendlist.html', {
        'users': users,
        'friends': friends,
        'requests': requests,
        'myasks': myasks,
        'notifs': notifs,
    })


def askfriend(request, id):
    user = request.user
    other_user = User.objects.get(pk=id)
    Friend.objects.add_friend(request.user, other_user)

    notify.send(user, recipient=other_user, verb="Vous avez recu une demande d'ami")

    return redirect('friendlist')


def addfriend(request, id):
    friend_request = FriendshipRequest.objects.get(from_user_id=id)
    friend_request.accept()
    return redirect('friendlist')


def refusfriend(request, id):
    friend_request = FriendshipRequest.objects.get(from_user_id=id, to_user=request.user)
    friend_request.reject()
    friend_request.delete()
    return redirect('friendlist')


def searchad(request):
    query = request.POST['usr_query']
    currentdate = datetime.datetime.today().strftime('%Y-%m-%d')
    ads = Ad.objects.filter(Q(sixte_name__icontains=query) | Q(sixte_location__icontains=query)).order_by('-sixte_date').filter(sixte_date__range=[currentdate, "2100-01-01"])
    oldads = Ad.objects.all().order_by('-sixte_date').filter(sixte_date__range=["1900-01-01", currentdate])
    notifs = notification(request)

    return render(request, 'menu/home.html', {
        'ads': ads,
        'oldads': oldads,
        'notifs': notifs,
    })


def searchuser(request):
    user = request.user
    query = request.POST['usr_query']

    friends = Friend.objects.friends(user)
    requests = Friend.objects.unread_requests(user=user)
    myasks = Friend.objects.sent_requests(user=user)

    users = User.objects.exclude(friends__from_user=user).exclude(id=user.id) \
        .exclude(friendship_requests_received__from_user=user).filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))

    notifs = notification(request)

    return render(request, 'profil/friendlist.html', {
        'users': users,
        'friends': friends,
        'requests': requests,
        'myasks': myasks,
        'notifs': notifs,
    })


def unread(request):
    user = request.user
    user.notifications.mark_all_as_read()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
