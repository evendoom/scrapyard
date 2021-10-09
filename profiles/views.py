from django.shortcuts import render
from django.contrib.auth.models import User
from .signals import profile_send


def register_page(request):
    """ Render register page """

    if request.method == 'POST':
        # Create dictionary with form responses
        response = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'address1': request.POST.get('address1'),
            'address2': request.POST.get('address2'),
            'city': request.POST.get('city'),
            'country': request.POST.get('country'),
            'postcode': request.POST.get('postcode'),
            'phone_number': request.POST.get('phone_number')
        }

        # Create User object
        User.objects.create(
            username=response['email'],
            password=response['password'],
            email=response['email']
        )

        # Get user object
        user = User.objects.get(username=response['email'])

        # Send signal to create Profile object
        profile_send.send(
            sender=profile_send,
            user=user,
            response=response
        )

    return render(request, 'profiles/register.html')
