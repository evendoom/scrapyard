import django.dispatch
from django.dispatch import receiver
from .models import Profile

# Signals
profile_send = django.dispatch.Signal()


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
