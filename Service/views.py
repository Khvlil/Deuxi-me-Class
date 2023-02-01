from django.shortcuts import render, redirect, get_object_or_404
from Accounts.models import User, UserSubscription
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
import requests


def landinpage(request):
    return render(request, 'service/Home/Home.html')


@login_required()
def home(request, pk=None):
    user = request.user
    if user.is_authenticated and pk is not None:
        authenticated = User.objects.filter(uids=pk)
        # Google Avatar
        if SocialAccount.objects.filter(user=user, provider='google'):
            avatar = SocialAccount.objects.get(
                extra_data__contains=user.email).extra_data['picture']
        # Github Avatar
        elif SocialAccount.objects.filter(user=user, provider='github'):
            avatar = SocialAccount.objects.get(
                extra_data__contains=user.email).extra_data['avatar_url']
        else:

            return render(request, 'service/Home/Feed.html', context={'username': user.username, 'user': user})

        return render(request, 'service/Home/Feed.html', context={'username': user.username, 'user': user, 'Avatar': avatar})

    return render(request, 'service/Home/Feed.html')


@ login_required(login_url='Accounts:Login')
def design(request, pk=None):
    user = request.user
    if user.is_authenticated and pk is not None:
        authenticated = User.objects.filter(uids=pk)

    return render(request, 'service/Categories/Design.html', context={'user': user})


@ login_required(login_url='Accounts:Login')
def code(request, pk=None):
    user = request.user
    if user.is_authenticated and pk is not None:
        authenticated = User.objects.filter(uids=pk)
    return render(request, 'service/Categories/Coding.html', context={'user': user})


@ login_required(login_url='Accounts:Login')
def language(request, pk=None):
    user = request.user
    if user.is_authenticated and pk is not None:
        authenticated = User.objects.filter(uids=pk)

    return render(request, 'service/Categories/Language.html', context={'user': request.user})


@ login_required(login_url='Accounts:Login')
def website_terms(request):
    user = request.user
    if user.is_authenticated and pk is not None:
        authenticated = User.objects.filter(uids=pk)

    return render(request, 'service/Home/Policy.html', context={'pk': request.user.username})
