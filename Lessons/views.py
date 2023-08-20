from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from Accounts.models import User

# Create your views here.


@login_required(login_url='Accounts:Login', redirect_field_name='lecture')
def illustrator(request, pk):
    user = request.user
    authenticate = User.objects.filter(uids=pk)
    previous = 'Design'
    # Print all session
    # for key, value in request.session.items():
    #   print('{} = {}'.format(key, value))
    request.session['last-correct-path'] = request.path
    return render(request, 'Service/Lessons/Design-Lessons/illustrator.html', context={'pk': user.uids, 'previous': previous})


@login_required(login_url='Accounts:Login', redirect_field_name='lecture')
def photoshop(request, pk):
    user = request.user
    authenticate = User.objects.filter(uids=pk)
    previous = 'Design'
    request.session['last-correct-path'] = request.path

    return render(request, 'Service/Lessons/Design-Lessons/Photoshop.html', context={'pk': user.uids, 'previous': previous})


@login_required(login_url='Accounts:Login', redirect_field_name='lecture')
def premier_pro(request, pk):
    user = request.user
    authenticate = User.objects.filter(uids=pk)
    previous = 'Design'
    request.session['last-correct-path'] = request.path

    return render(request, 'Service/Lessons/Design-Lessons/Premier-Pro.html', context={'pk': user.uids, 'previous': previous})


@login_required(login_url='Accounts:Login', redirect_field_name='lecture')
def tds_max(request, pk):
    user = request.user
    authenticate = User.objects.filter(uids=pk)
    previous = 'Design'
    request.session['last-correct-path'] = request.path

    return render(request, 'Service/Lessons/Design-Lessons/3ds-max.html', context={'pk': user.uids, 'previous': previous})


# ---------------------- Coding categorie ------------------------
@login_required(login_url='Accounts:Login', redirect_field_name='lecture')
def code(request, pk):
    user = request.user
    authenticate = User.objects.filter(uids=pk)
    previous = 'Code'
    request.session['last-correct-path'] = request.path

    return render(request, 'Service/Lessons/Code-Lessons/Code.html', context={'pk': user.uids, 'previous': previous})


login_required(login_url='Accounts:Login', redirect_field_name='lecture')


def algo(request, pk):
    user = request.user
    authenticate = User.objects.filter(uids=pk)
    previous = 'Code'
    request.session['last-correct-path'] = request.path

    return render(request, 'Service/Lessons/Code-Lessons/Algo.html', context={'pk': user.uids, 'previous': previous})


login_required(login_url='Accounts:Login', redirect_field_name='lecture')


def math(request, pk):
    user = request.user
    authenticate = User.objects.filter(uids=pk)
    previous = 'Code'
    request.session['last-correct-path'] = request.path

    return render(request, 'Service/Lessons/Code-Lessons/Math.html', context={'pk': user.uids, 'previous': previous})


# ---------------------- Language categorie ------------------------

@login_required(login_url='Accounts:Login', redirect_field_name='lecture')
def french(request, pk):
    user = request.user
    authenticate = User.objects.filter(uids=pk)
    previous = 'Language'
    request.session['last-correct-path'] = request.path

    return render(request, 'Service/Lessons/Language-Lessons/French.html', context={'pk': user.uids, 'previous': previous})


@login_required(login_url='Accounts:Login', redirect_field_name='lecture')
def english(request, pk):
    user = request.user
    authenticate = User.objects.filter(uids=pk)
    previous = 'Language'
    request.session['last-correct-path'] = request.path

    return render(request, 'Service/Lessons/Language-Lessons/English.html', context={'pk': user.uids, 'previous': previous})
