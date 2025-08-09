from django.urls import path
from . import views

app_name = 'mods'

urlpatterns = [
    path('mod/<str:pk>/', views.ModDetailView.as_view(), name='mod_detail'),
    path('parar-server/', views.parar_servidor_view, name='parar_servidor'),
    path('reiniciar-server/', views.reiniciar_servidor_view, name='reiniciar_servidor'),
    path('iniciar-server/', views.iniciar_servidor_view, name='iniciar_servidor'),
    path('reiniciar-mundo/', views.reiniciar_mundo_view, name='reiniciar_mundo'),
]