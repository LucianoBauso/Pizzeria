from django import forms
from .models import Pedidos

from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User


class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['cliente', 'direccion', 'pedido']
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el cliente'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la dirección'}),
            'pedido': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese el pedido'}),
        }
        

class UserEditForm(UserChangeForm):
    
    username = forms.CharField(label='Usuario',widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label='Email',widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(label='Nombre',widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    last_name = forms.CharField(label='Apellido',widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}))
    password = forms.CharField(label='Contraseña',widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Contraseña'}))
    #password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    #password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [ 'username', 'email', 'first_name', 'last_name', 'password']
        help_texts = {k:"" for k in fields}

class ChangePasswordForm(PasswordChangeForm):
    
    old_password = forms.CharField(label='Contraseña Actual', widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña Actual'}))
    new_password1 = forms.CharField(label='Nueva Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña Nueva'}))
    new_password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña Nueva'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        help_texts = {k:"" for k in fields}

class AvatarFormulario(forms.Form):
    imagen = forms.ImageField()