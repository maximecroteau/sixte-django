from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from friendship.models import Friend
from friendship.models import FriendshipRequest
from django.shortcuts import redirect
from django.db.models import Q


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
    if form.is_valid():
        form.save()
        return redirect('home')
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
        return redirect('home')

    else:
        form = CreateTeam()
    return render(request, 'menu/createteam.html', {
        'form': form,
        'ad': ad,
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
    ads_edits = Ad.objects.get(id=id)
    form = CreateAd(request.POST, instance=ads_edits)
    if form.is_valid():
        form.save()
        return redirect('my_ad')
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
    edit_team = Team.objects.get(id=id)
    form = CreateTeam(request.POST, instance=edit_team)
    if form.is_valid():
        form.save()
        return redirect('my_teams')
    else:
        form = CreateTeam()
    return render(request, 'menu/editteam.html', {
        'edit_team': edit_team,
        'form': form,
    })


def friendlist(request):
    # List of this user's friends
    user = request.user

    friends = Friend.objects.friends(user)
    requests = Friend.objects.unread_requests(user=user)
    myasks = User.objects.filter(friendship_requests_received__from_user=user)
    users = User.objects.exclude(friends__from_user=user).exclude(id=user.id) \
        .exclude(friendship_requests_received__from_user=user)

    return render(request, 'profil/friendlist.html', {
        'user': user,
        'users': users,
        'friends': friends,
        'requests': requests,
        'myasks': myasks,
    })


def askfriend(request, id):
    other_user = User.objects.get(pk=id)
    Friend.objects.add_friend(request.user, other_user)
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
    ads = Ad.objects.filter(Q(sixte_name__icontains=query) | Q(sixte_location__icontains=query))
    return render(request, 'menu/home.html', {
        'ads': ads,
     })
