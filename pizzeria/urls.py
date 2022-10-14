"""pizzeria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path
from pedidos import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('registrarte/', views.registrarte, name='registrarte'),
    path('ingresar/', views.ingresar, name='ingresar'),
    path('salir/', views.salir, name='salir'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos_completados/', views.pedidos_completados, name='pedidos_completados'),
    path('pedido/crear/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedido/<int:pedido_id>/completo', views.pedido_completo, name='pedido_completo'),
    path('pedido/<int:pedido_id>/eliminado', views.eliminar_pedido, name='eliminar_pedido'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
