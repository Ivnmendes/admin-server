import subprocess
from django.template.loader import render_to_string
from django.urls import reverse
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from jet.dashboard.modules import AppList, ModelList, LinkList, RecentActions, DashboardModule

from mods.utils import is_restart_pending

from .models import Mod 
from .utils import get_server_status

class ServerControlWidget(DashboardModule):
    title = 'Controle do Servidor'
    template = 'server_control.html'

    def render(self):
        status_code, status_text, status_color = get_server_status()
        return render_to_string(self.template, {
            'status_code': status_code,
            'status_text': status_text,
            'status_color': status_color,
        })


class CustomIndexDashboard(Dashboard):

    columns = 3

    def init_with_context(self, context):

        self.children.append(LinkList(
            'Links Úteis',
            children=[
                {'title': 'Adicionar Novo Mod', 'url': reverse('admin:mods_mod_add')},
            ],
            column=0,
            order=0
        ))

        self.children.append(ServerControlWidget(
            title='Controle do Servidor',
            column=0,
            order=1,
        ))

        mods_ativos = Mod.objects.filter(status='enabled')
        self.children.append(LinkList(
            'Mods Ativos',
            children=[
                {'title': mod.name, 'url': mod.get_absolute_url()} for mod in mods_ativos
            ],
            column=2,
            order=1,
            cache_timeout=0,
        ))
