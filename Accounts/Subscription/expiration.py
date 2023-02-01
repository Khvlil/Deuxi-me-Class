from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from django.contrib.auth import logout as django_logout
import Accounts.models


@receiver(user_logged_in)
def send_email_expired(request, user, **kwargs):
    # Check if the user argument was provided
    if not user:
        # The user argument was not provided, so return from the function
        return

    # Check if the user has already logged in
    if not request.session.get('user_id'):
        # This is the first time the user has logged in
        # Update the user's is_active field and set their ID in the session
        cancel_onlign = Accounts.models.User.objects.filter(
            uids=user.uids).update(is_active=True)
        request.session['user_id'] = user.uids
        request.session.save()

    # Get the UserSubscription instance for the user
    client = Accounts.models.UserSubscription.objects.get(client=user)
    if not (client.free_trials(client)) or not (client.subscribe(client)):
        # Check if the email has been sent already
        if not client.email_sent:
            # Send Email
            letter = get_template(
                'account/ExpiredSubscriptionEmail.html').render(context={'username': user.username})
            # Formating the letter to html
            letter_ = strip_tags(letter)

            email = EmailMultiAlternatives(
                'Susbcription Expired',
                None,
                f'Susbcription Expired <{settings.EMAIL_HOST_USER}>',
                [user.email]
            )
            email.attach_alternative(letter, 'text/html')
            email.fail_silently = False
            email.send()

            # Set the email_sent flag on the UserSubscription instance
            client.email_sent = True
            client.save()

            return email
