from django.contrib import admin
from django.urls import path, include

app_name = 'adminserver'

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('mods/', include('mods.urls')),
    path('', admin.site.urls, name='home'),
]