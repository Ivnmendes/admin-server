from ast import Mod
import subprocess
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from mods.utils import set_restart_pending_flag

class ModDetailView(DetailView):
    model = Mod
    template_name = 'mod_detail.html'

@staff_member_required
def parar_servidor_view(request):
    """
    Script de parada do servidor.
    """

    script_path = '/home/opc/stop_pz.sh'

    try:
        result = subprocess.run(
            ['sudo', script_path], 
            check=True, 
            capture_output=True, 
            text=True
        )

        messages.success(request, f"Comando de reinicialização enviado com sucesso!")
        print("Saída do script:", result.stdout)

    except subprocess.CalledProcessError as e:
        messages.error(request, f"Erro ao executar o script de reinicialização.")
        print(f"Erro no script: {e.stderr}")

    return redirect(reverse('jet-dashboard'))

@staff_member_required
def reiniciar_servidor_view(request):
    """
    Script de reinicialização do servidor.
    """

    script_path = '/home/opc/restart_pz.sh'

    try:
        result = subprocess.run(
            ['sudo', script_path], 
            check=True, 
            capture_output=True, 
            text=True
        )

        messages.success(request, f"Comando de reinicialização enviado com sucesso!")

        set_restart_pending_flag(False)
        print("Saída do script:", result.stdout)

    except subprocess.CalledProcessError as e:
        messages.error(request, f"Erro ao executar o script de reinicialização.")
        print(f"Erro no script: {e.stderr}")

    return redirect(reverse('jet-dashboard'))

@staff_member_required
def iniciar_servidor_view(request):
    """
    Script de inicialização do servidor.
    """

    script_path = '/home/opc/start_pz.sh'

    try:
        result = subprocess.run(
            ['sudo', script_path], 
            check=True, 
            capture_output=True, 
            text=True
        )

        messages.success(request, f"Comando de inicialização enviado com sucesso!")
        print("Saída do script:", result.stdout)

    except subprocess.CalledProcessError as e:
        messages.error(request, f"Erro ao executar o script de inicialização.")
        print(f"Erro no script: {e.stderr}")

    return redirect(reverse(''))
