from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
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
        User.objects.create_user(
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


def login_page(request):
    """ Render login page """

    if request.method == 'POST':

        # Create dictionary from form elements
        response = {
            'username': request.POST.get('email'),
            'password': request.POST.get('password')
        }

        # Check if username exists
        try:
            user = User.objects.get(username=response['username'])
            print(user)
        except:  # noqa: E722
            # Add flash message here
            print('Incorrect login details')

        # Authenticate user
        user = authenticate(
            request,
            username=response['username'],
            password=response['password']
        )

        # Log user in
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            # Add flash message
            print('Incorrect Username / Password')

    return render(request, 'profiles/login.html')
