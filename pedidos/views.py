from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import PedidosForm, UserEditForm, ChangePasswordForm,AvatarFormulario
from .models import Avatar, Pedidos

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
def avatar(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request,'base.html',{'url': avatares[0].imagen.url})

@login_required
def pedidos(request):
    try:
        pedidos = Pedidos.objects.filter(user=request.user, enviado__isnull=True)
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request, 'pedidos.html', {'pedidos': pedidos, 'url': avatares[0].imagen.url})
    except:
        pedidos = Pedidos.objects.filter(user=request.user, enviado__isnull=True)
        return render(request, 'pedidos.html', {'pedidos': pedidos})

@login_required
def pedidos_completados(request):
    try:
        pedidos = Pedidos.objects.filter(user=request.user, enviado__isnull=False).order_by('-enviado')
        avatares = Avatar.objects.filter(user=request.user.id)
        return render(request, 'pedidos-completados.html', {'pedidos': pedidos, 'url': avatares[0].imagen.url})
    except:
        pedidos = Pedidos.objects.filter(user=request.user, enviado__isnull=False).order_by('-enviado')
        return render(request, 'pedidos-completados.html', {'pedidos': pedidos})

@login_required
def crear_pedido(request):
    try:
        if request.method == 'GET':
            avatares = Avatar.objects.filter(user=request.user.id)
            return render(request, 'crear-pedido.html', {
                'url': avatares[0].imagen.url,
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
    except:
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

@login_required
def editarPerfil(request):
    try:
        usuario = request.user
        user_basic_info = User.objects.get(id = usuario.id)
        avatares = Avatar.objects.filter(user=request.user.id)
        form = UserEditForm(request.POST, instance = usuario)
        if request.method == 'POST':
            if form.is_valid():
                user_basic_info.username = form.cleaned_data.get('username')
                user_basic_info.email = form.cleaned_data.get('email')
                user_basic_info.first_name = form.cleaned_data.get('first_name')
                user_basic_info.last_name = form.cleaned_data.get('last_name')
                
                user_basic_info.save()
                return redirect('pedidos')
            else:
                return redirect('pedidos')
        else:
            form = UserEditForm(initial = {'email': usuario.email, 'username': usuario.username, 'first_name': usuario.first_name, 'last_name': usuario.last_name})
        return render(request, 'editarPerfil.html', {"form":form, "usuario":usuario, 'url': avatares[0].imagen.url})
    except:
        usuario = request.user
        user_basic_info = User.objects.get(id = usuario.id)
        form = UserEditForm(request.POST, instance = usuario)
        if request.method == 'POST':
            if form.is_valid():
                user_basic_info.username = form.cleaned_data.get('username')
                user_basic_info.email = form.cleaned_data.get('email')
                user_basic_info.first_name = form.cleaned_data.get('first_name')
                user_basic_info.last_name = form.cleaned_data.get('last_name')
                
                user_basic_info.save()
                return redirect('pedidos')
            else:
                return redirect('pedidos')
        else:
            form = UserEditForm(initial = {'email': usuario.email, 'username': usuario.username, 'first_name': usuario.first_name, 'last_name': usuario.last_name})
        return render(request, 'editarPerfil.html', {"form":form, "usuario":usuario})


@login_required
def changepass(request):
    try:
        usuario = request.user
        avatares = Avatar.objects.filter(user=request.user.id)
        if request.method == 'POST':
            form = ChangePasswordForm(data = request.POST, user = request.user)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('pedidos')
        else:
            
            form = ChangePasswordForm(user = request.user)
        return render(request, 'cambiarContraseña.html', {'form':form, 'usuario':usuario,'url': avatares[0].imagen.url})
    except:
        usuario = request.user
        
        if request.method == 'POST':
            form = ChangePasswordForm(data = request.POST, user = request.user)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('pedidos')
        else:
            
            form = ChangePasswordForm(user = request.user)
        return render(request, 'cambiarContraseña.html', {'form':form, 'usuario':usuario})

@login_required
def agregarAvatar(request):
    try:
        
        if request.method== 'POST': 
            miFormulario = AvatarFormulario(request.POST, request.FILES)      
            if miFormulario.is_valid():            
                user = User.objects.get(username=request.user)           
                avatar = Avatar (user=user, imagen=miFormulario.cleaned_data['imagen'] , id=request.user.id)  
                avatares = Avatar.objects.filter(user=request.user.id)       
                avatar.save()            
                return render(request, "pedidos.html")    
        else:         
            miFormulario=AvatarFormulario()    
        return render(request, "agregarAvatar.html", {"miFormulario": miFormulario,'url': avatares[0].imagen.url})
    except:
        if request.method== 'POST': 
            miFormulario = AvatarFormulario(request.POST, request.FILES)      
            if miFormulario.is_valid():            
                user = User.objects.get(username=request.user)           
                avatar = Avatar (user=user, imagen=miFormulario.cleaned_data['imagen'] , id=request.user.id)         
                avatar.save()            
                return render(request, "pedidos.html")    
        else:         
            miFormulario=AvatarFormulario()    
        return render(request, "agregarAvatar.html", {"miFormulario": miFormulario})