from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import PedidosForm
from .models import Pedidos

def home(request):
    return render(request,'home.html')

def nosotros(request):
    return render(request,'acerca-nosotros.html')

def registrarte(request):
    if request.method == 'GET':
        return render(request, 'registrarte.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST['password1'], 
                    #imagen = request.POST['imagen'],
                    email=request.POST['email'],)
                user.save()
                login(request, user)
                return redirect('ingresar')
            except IntegrityError:
                return render(request,'registrarte.html', {
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })
        return render(request, 'registrarte.html', {
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })

def ingresar(request):
    if request.method == 'GET':
        return render(request, 'ingresar.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'ingresar.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecto'
            })
        else:
            login(request, user)
            return redirect('pedidos')

@login_required
def salir(request):
    logout(request)
    return redirect('home')

@login_required
def pedidos(request):
    pedidos = Pedidos.objects.filter(user=request.user, enviado__isnull=True)
    return render(request, 'pedidos.html', {'pedidos': pedidos})

@login_required
def pedidos_completados(request):
    pedidos = Pedidos.objects.filter(user=request.user, enviado__isnull=False).order_by('-enviado')
    return render(request, 'pedidos-completados.html', {'pedidos': pedidos})

@login_required
def crear_pedido(request):
    if request.method == 'GET':
        return render(request, 'crear-pedido.html', {
            'form': PedidosForm
        })
    else:
        try:
            form = PedidosForm(request.POST)
            nuevo_pedido = form.save(commit=False)
            nuevo_pedido.user = request.user
            nuevo_pedido.save()
            return redirect('pedidos')
        except ValueError:
            return render(request, 'crear-pedidos.html', {
                'form': PedidosForm,
                'error': 'Ingrese los datos correctos'
            })

@login_required
def detalle_pedido(request, pedido_id):
    if request.method == 'GET':
        pedido = get_object_or_404(Pedidos, pk=pedido_id, user=request.user)
        form = PedidosForm(instance=pedido)
        return render(request, 'detalle-pedido.html', {'pedido': pedido, 'form': form})
    else:
        try:
            pedido = get_object_or_404(Pedidos, pk=pedido_id, user=request.user)##Falta cambiar el Task por el Pedido, cuandos se cree el modelo
            form = PedidosForm(request.POST, instance=pedido)##Falta cambiar el TaskForm por el PedidoForm, cuandos se cree el modelo
            form.save()
            return redirect('pedidos')
        except ValueError:
            return render(request, 'detalle-pedido.html', {'pedido': pedido, 'form': form, 'error': "Error al actualizar la tarea"})

@login_required
def pedido_completo(request, pedido_id):
    pedido = get_object_or_404(Pedidos, pk=pedido_id, user=request.user)
    if request.method == 'POST':
        pedido.enviado = timezone.now()
        pedido.save()
        return redirect('pedidos')

@login_required
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedidos, pk=pedido_id, user=request.user)
    if request.method == 'POST':
        pedido.delete()
        return redirect('pedidos')

