from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .signals import profile_send, user_update
from .forms import ProfileForm


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
            email=response['email'],
            first_name=response['first_name'],
            last_name=response['last_name']
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
        except:  # noqa: E722
            messages.error(request, 'Incorrect Username')
        else:
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
                messages.error(request, 'Incorrect Username / Password')

    return render(request, 'profiles/login.html')


def logout_page(request):
    """ Kill user's session and redirect to main page """

    logout(request)
    messages.info(request, "You've been logged out!")
    return redirect('main_page')


def update_profile_page(request):
    """ Render page to update Profile """
    # Get profile instance
    profile = request.user.profile

    if request.method == 'POST':
        # Store previous username
        username = request.user.username

        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            # Send signal to update User
            user_update.send(
                sender=user_update,
                username=username
            )
            messages.info(request, 'Profile updated!')
            return redirect('main_page')

    form = ProfileForm(instance=profile)

    context = {
        'form': form
    }

    return render(request, 'profiles/user_settings.html', context)


def delete_user_page(request):
    """ Delete user profile """

    try:
        user = User.objects.get(id=request.user.id)
        user.delete()
        messages.info(request, 'User deleted!')
    except:  # noqa: E722
        messages.error(request, 'Internal error, please try again.')
    finally:
        return redirect('main_page')
