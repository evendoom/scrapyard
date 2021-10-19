import django.dispatch
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# Signals
profile_send = django.dispatch.Signal()
user_update = django.dispatch.Signal()


# Receivers
@receiver(profile_send)
def create_profile(sender, **kwargs):
    # Get User instance
    user = kwargs['user']

    # Get Register form elements
    response = kwargs['response']

    # Create Profile object
    Profile.objects.create(
        user=user,
        first_name=response['first_name'],
        surname=response['last_name'],
        address_1=response['address1'],
        address_2=response['address2'],
        postal_code=response['postcode'],
        city=response['city'],
        country=response['country'],
        phone_number=response['phone_number'],
        email=response['email']
    )


@receiver(user_update)
def update_user(sender, **kwargs):
    username = kwargs['username']

    # Get user and profile instances
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    # Update user instance
    user.username = profile.email
    user.email = profile.email
    user.first_name = profile.first_name
    user.last_name = profile.surname
    user.save()
