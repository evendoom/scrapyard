from django.shortcuts import render


def main_page(request):
    """ Render main page """
    
    return render(request, 'home/home.html')
