from .models import Mod
import subprocess
import logging
from django.views.generic import DetailView
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from adminserver import settings
from mods.utils import get_server_status

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
        subprocess.Popen(['sudo', script_path], text=True)
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
def parar_servidor_view(request):
    return executar_comando(settings.PZ_SCRIPT_STOP_PATH, "parada do servidor")


@staff_member_required
def reiniciar_servidor_view(request):
    return executar_comando(settings.PZ_SCRIPT_RESTART_PATH, "reinicialização do servidor")


@staff_member_required
def iniciar_servidor_view(request):
    return executar_comando(settings.PZ_SCRIPT_START_PATH, "inicialização do servidor")


@staff_member_required
def reiniciar_mundo_view(request):
    return executar_comando(settings.PZ_SCRIPT_RESTART_WORLD_PATH, "reinicialização do mundo")


def server_status_json_view(request):
    status_code, status_text, status_color = get_server_status()
    return JsonResponse({
        'status_code': status_code,
        'status_text': status_text,
        'status_color': status_color
    })
