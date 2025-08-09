from django.urls import path
from . import views

app_name = 'mods'

urlpatterns = [
    path('mod/<str:pk>/', views.ModDetailView.as_view(), name='mod_detail'),
    path('parar-server/', views.stop_server_view, name='parar_servidor'),
    path('reiniciar-server/', views.restart_server_view, name='reiniciar_servidor'),
    path('iniciar-server/', views.start_server_view, name='iniciar_servidor'),
    path('reiniciar-mundo/', views.restart_world_view, name='reiniciar_mundo'),
    path('server/status/', views.server_status_json_view, name='server_status_json'),
    path('logs/', views.view_logs, name='view_logs'),
]