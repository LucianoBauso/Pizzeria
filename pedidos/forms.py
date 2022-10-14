from django import forms
from .models import Pedidos

class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['cliente', 'direccion', 'pedido']
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el cliente'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la dirección'}),
            'pedido': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese el pedido'}),
        }
        
       