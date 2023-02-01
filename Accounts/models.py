
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import post_save

from shortuuidfield import ShortUUIDField
import shortuuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager, PermissionsMixin
# Sending email and subscription
from Accounts.Subscription.welcoming import Welcoming

from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from .views import logout
from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from django.contrib import messages


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, is_active=True, is_confirmed=True, is_admin=False, is_staff=False, is_superuser=False, date_joined=None):
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User must have a password')

        user_c = self.model(
            email=self.normalize_email(email)
        )
        user_c.set_password(password)
        user_c.username = username
        user_c.active = is_active
        user_c.admin = is_admin
        user_c.staff = is_staff
        user_c.date_join = date_joined
        user_c.save(using=self._db)

        return user_c

    def create_superuser(self, username, email, password):
        if not email:
            raise ValueError('User must have an email address')

        if not password:
            raise ValueError('User must have a password')

        user = self.create_user(
            username=username, email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    uids = ShortUUIDField(
        verbose_name="UIDS",
        max_length=2,
        default=shortuuid.uuid(),
        editable=False,
    )
    username = models.CharField(
        verbose_name="Username", unique=True, max_length=15)
    email = models.EmailField(verbose_name="Email-Adress", unique=True)
    password = models.CharField(verbose_name="Password", max_length=150)
    date_joinded = models.DateTimeField(
        verbose_name="Joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Account'

    def __str__(self):
        return self.username

    @property
    def user_name(self):
        return self.username

    @property
    def email_address(self):
        return self.email

    @property
    def user_id(self):
        return self.uids


class Reporter(models.Model):
    subject = models.CharField(
        max_length=100, verbose_name='Subject', null=True)
    opinion = models.TextField(verbose_name="Opinion", max_length=500)
    date_writing = models.DateTimeField(
        verbose_name="Writing in", auto_now_add=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)


class UserSubscription(models.Model):
    subscribed = models.BooleanField(default=False)
    free_trial = models.BooleanField(default=False)
    trial_start_date = models.DateTimeField(auto_now_add=True)
    subscription_expired = models.DateTimeField(
        verbose_name="Subscription expiration", default=timezone.now())
    free_trial_expired = models.DateTimeField(
        verbose_name="Free trial expiration", default=timezone.now())
    # Add a new field to store the email_sent flag
    email_sent = models.BooleanField(default=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE)

    def free_trials(self, instance):
        # Calculate the date and time when the free trial will expire
        instance.free_trial_expired = instance.trial_start_date + \
            timedelta(minutes=2)
        # Return whether the free trial is still valid
        return timezone.now() < instance.free_trial_expired

    def subscribe(self, instance):
        # Calculate the date and time when the free trial will expire
        instance.subscription_expired = instance.trial_start_date + \
            timedelta(days=7)

        instance.save()
        # Return whether the free trial is still valid
        return timezone.now() < instance.subscription_expired


@receiver(user_logged_in)
def social_loggin(request, user, **kwargs):
    client = UserSubscription.objects.get(client=user)
    if client:
        if not (client.free_trials(client)) or not (client.subscribe(client)):
            cancel_free_trial = UserSubscription.objects.filter(
                client=user
            ).update(free_trial=False)
            django_logout(request)
            messages.add_message(
                request, messages.ERROR, f'Subscription ended. Check your email for the party details.')

            return redirect('Accounts:subscription-expired')
