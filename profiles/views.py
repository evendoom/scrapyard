from django.shortcuts import render


def register_page(request):
    """ Render register page """
    
    return render(request, 'profiles/register.html')
