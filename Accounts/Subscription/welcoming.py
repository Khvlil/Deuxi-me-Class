from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.utils.html import strip_tags
from allauth.account.signals import user_signed_up as social_signed_up
from django.dispatch import receiver
import Accounts.models


class Welcoming:
    @receiver(social_signed_up)
    def send_email(request, user, **kwargs):
        # Send Email
        letter = get_template(
            'account/Email_letter.html').render(context={'username': user.username})
        # Formating the letter to html
        letter_ = strip_tags(letter)

        email = EmailMultiAlternatives(
            "Thanks for registering - now let's get this party started!",
            None,
            f'Welcome To S2ale <{settings.EMAIL_HOST_USER}>',
            [user.email]
        )
        email.attach_alternative(letter, 'text/html')
        email.fail_silently = False
        return email.send()

    @receiver(social_signed_up)
    def free_trial(request, user, **kwargs):
        # Give him 3 days free trial
        subscribe = Accounts.models.UserSubscription(
            free_trial=True, subscribed=False, client=user)

        return subscribe.save()
