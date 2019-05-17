from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import UpdateView

from .forms import CreateAd

from .models import Ad


def home(request):
    ads = Ad.objects.all()
    return render(request, 'menu/home.html', {
        'ads': ads
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
    return render(request, 'menu/home.html', {
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