from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
# Models
import Accounts.models  # import User, Reporter, UserSubscription
from django.contrib import messages
from django.http import JsonResponse

# Http Response
from django.http import HttpResponse, HttpResponseRedirect
# Time settings
from datetime import timedelta
from django.utils.timezone import now
from django.db import IntegrityError
# Login settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.urls import reverse, reverse_lazy, resolve
# Social Accounts
from allauth.socialaccount.models import SocialAccount
# Sending email
from Accounts.Subscription.welcoming import Welcoming

from Accounts.Subscription.expiration import send_email_expired
# Create your views here.


def sign_in(request):
    next_post = request.POST.get('next')
    lesson_post = request.POST.get('lecture')
    current_url = request.POST
    # If user alrady authenticate return to home / never show login page
    if request.user.is_authenticated:
        return redirect(reverse('Service:Home', kwargs={'pk': str(request.user.uids)}))

    if request.method == 'POST':
        # Get email and password
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user:
            client = Accounts.models.UserSubscription.objects.get(client=user)
            # Login user
            login(request, user)
            cancel_onlign = Accounts.models.User.objects.filter(
                uids=user.uids).update(is_active=True)
            # if the user subscriptions expired
            if not (client.free_trials(client)) or not (client.subscribe(client)):
                cancel_free_trial = Accounts.models.UserSubscription.objects.filter(
                    client_id=user).update(free_trial=False)
                cancel_confirmation = Accounts.models.User.objects.filter(
                    uids=user.uids).update(is_confirmed=False)
                response = redirect('Accounts:subscription-expired')
                # Store the user's email in the session
                request.session['email'] = user.email
                request.session['uids'] = user.uids

                return response

            # If 'next' is present in the request.POST dictionary
            if request.POST.get('next'):
                return redirect(next_post)
            # If 'voting' is present in the current_url dictionary and 'Vote' is present in the voting_post dictionary
            elif current_url.get('voting'):
                return redirect(reverse('Accounts:Vote', kwargs={'pk': user.uids}))
            # If 'lesson' is present in the current_url dictionary and 'Lessons' is present in the lesson_post dictionary
            elif current_url.get('lecture'):
                lesson_ = lesson_post.split()[0][9:]
                return redirect(reverse('Lessons:{}'.format(lesson_), kwargs={'pk': user.uids}))
            # If none of these conditions are met
            else:
                response = redirect(
                    reverse('Service:Home', kwargs={'pk': str(user.uids)}))

            # Set coockies and session
            response.set_cookie('Username', request.user.username)
            response.set_cookie('Login-In', request.user.date_joinded)
            response.set_cookie('Login-Status', True)
            request.session['Usernmae'] = request.user.username
            request.session['Email'] = request.user.email
            request.session['ID'] = request.user.uids
            request.session['Last_Login'] = str(request.user.last_login)
            request.session['Confirmed'] = request.user.is_confirmed
            request.session['Active'] = 'Active'

            return response
        # The user already signup with social authentication
        elif SocialAccount.objects.filter(extra_data__contains=email):
            provider = SocialAccount.objects.get(
                extra_data__contains=email).provider
            messages.add_message(
                request, messages.ERROR, f'Please login with your social account : {str(provider).capitalize()} Account')

            return redirect('Accounts:Login')

        # The user not exist
        else:
            messages.add_message(
                request, messages.ERROR, 'Please enter the correct Email Adress and password')

            return redirect('Accounts:Login')

    return render(request, 'account/Login.html')


def register(request):
    if request.method == "POST":
        # Get username, email and password
        username = request.POST.get("username").lower()
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        # Erro for User who already exist
        if Accounts.models.User.objects.filter(username=username).exists():
            return render(request, 'account/Register.html', context={'error_username': 'Oops ,Account already exist ,try something new'})

        elif Accounts.models.User.objects.filter(email=email).exists():
            return render(request, 'account/Register.html', context={'error_email': 'Oops ,Email already exist ,try something new'})

        else:
            try:
                # Create New User
                user = Accounts.models.User.objects.create(
                    username=username, email=email, password=make_password(password), is_active=True, is_confirmed=False)
                # Give Hime a free trial
                Welcoming.free_trial(request, user)
                # Registre the user
                user.save()
                user = authenticate(request, username=email,
                                    password=password)
                # Send Email
                Welcoming.send_email(request, user)
                # Log him in
                login(request, user)
                response = redirect(
                    reverse('Service:Home', kwargs={'pk': str(user.uids)}))
                # Set cockies and session
                response.set_cookie('Username', request.user.username)
                response.set_cookie('Login-In', request.user.date_joinded)
                response.set_cookie('Login-Status', True)
                request.session['Usernmae'] = request.user.username
                request.session['Email'] = request.user.email
                request.session['ID'] = request.user.uids
                request.session['Last_Login'] = str(request.user.last_login)
                request.session['Confirmed'] = request.user.is_confirmed
                request.session['Active'] = 'Active'
                request.session['in-Free-Trial'] = True
                request.session.save()
                return response

            except IntegrityError:
                print("Isn't register...")
                return render(request, 'account/Register.html')

    return render(request, 'account/Register.html')


def logout(request):
    django_logout(request)
    response = redirect('Service:Home')
    response.delete_cookie('Username')
    response.delete_cookie('Login-In')
    response.delete_cookie('Login-Status')
    return response


def error_404(request, exception):
    pre_url = request.session['last-correct-path']
    return render(request, 'Error/404/Error404.html', context={'previous': pre_url}, status=404)


def error_500(request):
    return render(request, 'Error/500/Error500.html', status=500)


@ login_required(login_url='Accounts:Login', redirect_field_name='voting')
def vote(request, pk=None):
    user = request.user
    if user.is_authenticated and pk is not None:
        authenticated = Accounts.models.User.objects.filter(uids=pk)

        if request.method == "POST":
            opinions = request.POST.get('opinion')
            if opinions != ' ':
                reporter = Accounts.models.Reporter(subject=None,
                                                    opinion=opinions, reporter=user)
                reporter.save()

            return redirect(reverse('Service:Home', kwargs={'pk': str(user.uids)}))

        # Google Avatar
        if SocialAccount.objects.filter(user=user, provider='google'):
            avatar = SocialAccount.objects.get(
                extra_data__contains=user.email).extra_data['picture']
        # Github Avatar
        elif SocialAccount.objects.filter(user=user, provider='github'):
            avatar = SocialAccount.objects.get(
                extra_data__contains=user.email).extra_data['avatar_url']
        else:
            return render(request, 'account/Vote.html', context={'username': user.username.title(), 'user': user})

        return render(request, 'account/Vote.html', context={'username': user.username.title(), 'user': user, 'Avatar': avatar})

    else:
        return redirect('Accounts:Login')

    return render(request, 'account/Vote.html')


@ login_required(login_url='Accounts:Login', redirect_field_name='decease')
def susbscribePagePlan(request):
    user = request.user

    if request.method == 'POST':
        send = request.POST.get('send')
        send_email_expired(
            request, user, email_addres=request.session.get('email'))
        response = redirect('Service:Home')
        response.delete_cookie('Email')
        django_logout(request)
        return response
    else:
        django_logout(request)

    return render(request, 'account/Subscription/Subscription-Expired.html')


def test(request):
    timing = UserSubscription.objects.get(client=request.user).free_trials

    tt = (now() - UserSubscription.objects.get(client=request.user)
          .trial_start_date)
    # if time:
    #    return redirect('Accounts:Logout')
    return render(request, 'account/Email_letter.html', context={'time': timing, 'tt': tt, 'username': request.user.username})
