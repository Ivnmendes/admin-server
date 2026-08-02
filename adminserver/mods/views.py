import os
from django.shortcuts import render
from django.urls import reverse
from .models import Mod
import subprocess
import logging
from django.views.generic import DetailView
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from adminserver import settings
from mods.utils import get_server_status, is_restart_pending, set_restart_pending_flag

logger = logging.getLogger(__name__)


class ModDetailView(DetailView):
    model = Mod
    template_name = 'mod_detail.html'
    

def executar_comando(script_path, acao):
    """
    Executa script via subprocess.Popen de forma assíncrona.
    """
    if not script_path:
        logger.error(f"Caminho do script para {acao} não configurado.")
        return JsonResponse({'status': 'error', 'message': f'Caminho do script de {acao} não configurado.'})

    try:
        subprocess.Popen(['sudo', 'bash', script_path], text=True)
        logger.info(f"Comando de {acao} enviado.")
        return JsonResponse({'status': 'ok', 'message': f'Comando de {acao} enviado.'})

    except FileNotFoundError:
        logger.exception(f"Script de {acao} não encontrado: {script_path}")
        return JsonResponse({'status': 'error', 'message': f'Script de {acao} não encontrado.'})

    except OSError as e:
        logger.exception(f"Erro ao executar script de {acao}: {e}")
        return JsonResponse({'status': 'error', 'message': f'Erro ao executar script de {acao}.'})

    except Exception as e:
        logger.exception(f"Erro inesperado ao executar script de {acao}: {e}")
        return JsonResponse({'status': 'error', 'message': f'Erro inesperado: {e}'})


@staff_member_required
def stop_server_view(request):
    if is_restart_pending():
        set_restart_pending_flag(False)
    logger.info("Parando servidor Project Zomboid.", f"Usuario: {request.user.username if request.user.is_authenticated else 'Anônimo'}")
    return executar_comando(settings.PZ_SCRIPT_STOP_PATH, "parada do servidor")


@staff_member_required
def restart_server_view(request):
    if is_restart_pending():
        set_restart_pending_flag(False)
    logger.info("Reiniciando servidor Project Zomboid.", f"Usuario: {request.user.username if request.user.is_authenticated else 'Anônimo'}")
    return executar_comando(settings.PZ_SCRIPT_RESTART_PATH, "reinicialização do servidor")


@staff_member_required
def start_server_view(request):
    logger.info("Iniciando servidor Project Zomboid.", f"Usuario: {request.user.username if request.user.is_authenticated else 'Anônimo'}")
    return executar_comando(settings.PZ_SCRIPT_START_PATH, "inicialização do servidor")


@staff_member_required
def restart_world_view(request):
    if is_restart_pending():
        set_restart_pending_flag(False)
    logger.info("Reiniciando mundo do servidor Project Zomboid.", f"Usuario: {request.user.username if request.user.is_authenticated else 'Anônimo'}")
    return executar_comando(settings.PZ_SCRIPT_RESTART_WORLD_PATH, "reinicialização do mundo")


def server_status_json_view(request):
    status_code, status_text, status_color = get_server_status()
    return JsonResponse({
        "status_code": status_code,
        "status_text": status_text,
        "status_color": status_color,
        "urls": {
            "iniciar": reverse("mods:iniciar_servidor"),
            "parar": reverse("mods:parar_servidor"),
            "reiniciar": reverse("mods:reiniciar_servidor"),
        }
    })


@staff_member_required
def view_logs(request):
    log_path = os.path.join(settings.BASE_DIR, 'logs', 'error.log')  
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-100:] 
    except Exception as e:
        lines = [f"Erro ao abrir o arquivo de log: {e}"]

    return render(request, 'log_view.html', {'lines': lines})