from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
from my_app.forms import AddressForm
from my_app.models import Address, STATES_CHOICES


def login(request: HttpRequest):
    if request.method == 'GET':
        return render(request, "my_app/login.html")
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user:
        django_login(request, user)
        return redirect('/home/')

    message = 'Credenciais inválidas'
    return render(request, "my_app/login.html", {'message': message})


@login_required(login_url='/login')
def logut(request):
    django_logout(request)
    return redirect('/login/')


@login_required(login_url='/login')
def home(request):
    return render(request, 'my_app/home.html')


@login_required(login_url='/login')
def address_list(request):
    addresses = Address.objects.all()
    return render(request, 'my_app/address/list.html', {'addresses': addresses})


@login_required(login_url='/login')
def address_create(request):
    states = STATES_CHOICES
    form = AddressForm
    if request.method == 'GET':
        return render(request, 'my_app/address/create.html', {'form': form})

    Address.objects.create(
        address=request.POST.get('address'),
        address_complement=request.POST.get('address_complement'),
        state=request.POST.get('state'),
        city=request.POST.get('city'),
        country=request.POST.get('country'),
        user=request.user
    )

    return redirect('/addresses/')


@login_required(login_url='/login')
def address_update(request, id):
    address = Address.objects.get(id=id)
    if request.method == 'GET':
        states = STATES_CHOICES
        return render(request, 'my_app/address/update.html', {'states': states, 'address': address})

    address.address = request.POST.get('address')
    address.address_complement = request.POST.get('address_complement')
    address.state = request.POST.get('state')
    address.city = request.POST.get('city')
    address.country = request.POST.get('country')
    # address.user=request.user

    address.save()

    return redirect('/addresses/')
