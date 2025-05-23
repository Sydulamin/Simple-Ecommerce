from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Product.models import Product
# Create your views here.

# @login_required(login_url='reg')
def home(request):

    new_arivel = Product.objects.filter(new_arrival=True)
    top_rated = Product.objects.filter(top_rated=True)

    return render(request, 'home/home.html', {'new_arivel': new_arivel, 'top_rated': top_rated})