from ast import Mod
import subprocess
import logging
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from adminserver import settings
from mods.utils import set_restart_pending_flag

logger = logging.getLogger(__name__)

class ModDetailView(DetailView):
    model = Mod
    template_name = 'mod_detail.html'

@staff_member_required
def parar_servidor_view(request):
    """
    Script de parada do servidor.
    """

    script_path = settings.PZ_SCRIPT_STOP_PATH

    try:
        result = subprocess.run(
            ['sudo', script_path], 
            check=True, 
            capture_output=True, 
            text=True,
            timeout=30,
        )

        messages.success(request, f"Comando de parada enviado com sucesso!")
        logger.info(f"Saída do script stop_pz.sh: {result.stdout}")

    except subprocess.CalledProcessError as e:
        messages.error(request, f"Erro ao executar o script de parada.")
        logger.error(f"Erro no script: {e.stderr}")

    except subprocess.TimeoutExpired:
        messages.error(request, f"Tempo limite excedido ao executar o script de parada.")
        logger.warning("Timeout ao executar o script stop_pz.sh.")

    previous_url = request.META.get('HTTP_REFERER', '/') 

    return redirect(previous_url)

@staff_member_required
def reiniciar_servidor_view(request):
    """
    Script de reinicialização do servidor.
    """

    script_path = settings.PZ_SCRIPT_RESTART_PATH

    try:
        result = subprocess.run(
            ['sudo', script_path], 
            check=True, 
            capture_output=True, 
            text=True,
            timeout=30
        )

        messages.success(request, f"Comando de reinicialização enviado com sucesso!")

        set_restart_pending_flag(False)
        logger.info(f"Saída do script restart_pz.sh: {result.stdout}")

    except subprocess.CalledProcessError as e:
        messages.error(request, f"Erro ao executar o script de reinicialização.")
        logger.error(f"Erro no script: {e.stderr}")

    except subprocess.TimeoutExpired:
        messages.error(request, f"Tempo limite excedido ao executar o script de reinicialização.")
        logger.warning("Timeout ao executar o script restart_pz.sh.")

    previous_url = request.META.get('HTTP_REFERER', '/') 

    return redirect(previous_url)

@staff_member_required
def iniciar_servidor_view(request):
    """
    Script de inicialização do servidor.
    """

    script_path = settings.PZ_SCRIPT_START_PATH

    try:
        result = subprocess.run(
            ['sudo', script_path], 
            check=True, 
            capture_output=True, 
            text=True
        )

        messages.success(request, f"Comando de inicialização enviado com sucesso!")
        logger.info(f"Saída do script start_pz.sh: {result.stdout}")

    except subprocess.CalledProcessError as e:
        messages.error(request, f"Erro ao executar o script de inicialização.")
        logger.error(f"Erro no script: {e.stderr}")

    except subprocess.TimeoutExpired:
        messages.error(request, f"Tempo limite excedido ao executar o script de inicialização.")
        logger.warning("Timeout ao executar o script start_pz.sh.")

    previous_url = request.META.get('HTTP_REFERER', '/') 

    return redirect(previous_url)

@staff_member_required
def reiniciar_mundo_view(request):
    """
    Script de reinicialização do mundo.
    """

    script_path = settings.PZ_SCRIPT_RESTART_WORLD_PATH

    try:
        result = subprocess.run(
            ['sudo', script_path], 
            check=True, 
            capture_output=True, 
            text=True
        )

        messages.success(request, f"Comando de reinicialização do mundo enviado com sucesso!")
        logger.info(f"Saída do script restart_world.sh: {result.stdout}")

    except subprocess.CalledProcessError as e:
        messages.error(request, f"Erro ao executar o script de reinicialização do mundo.")
        logger.error(f"Erro no script: {e.stderr}")

    except subprocess.TimeoutExpired:
        messages.error(request, f"Tempo limite excedido ao executar o script de reinicialização do mundo.")
        logger.warning("Timeout ao executar o script restart_world.sh.")

    previous_url = request.META.get('HTTP_REFERER', '/')

    return redirect(previous_url)