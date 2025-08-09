from django.db import IntegrityError
from .models import Mod
import requests
from bs4 import BeautifulSoup
import re
from django.conf import settings
from django.core.cache import cache
import psutil
import logging

logger = logging.getLogger(__name__)

class Build42Error(Exception):
    """Custom exception for Build 42 errors."""
    pass


def scrappling_steam_workshop(url, user):

    results = { 'errors': [], 'success': [] }

    try:
        match = re.search(r'id=(\d+)', url)
        if not match:
            logger.error(f"URL inválida ou sem ID do workshop: {url}")
            results['errors'].append(f"URL inválida ou sem ID do workshop: {url}")
            return None, None, None, results
        # Extrai o ID do workshop da URL
        workshop_id = match.group(1)

        # Prepara o request com headers para evitar bloqueios
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        # Verifica se a resposta foi bem-sucedida
        response.raise_for_status()

        # Faz o parsing do HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Verifica se o mod é compatível com Build 41
        categories = soup.find('div', class_='rightDetailsBlock').text.strip()
        if categories:
            has_build_42 = categories.find('Build 42')

            if has_build_42 != -1:
                has_build_41 = categories.find('Build 41')
                if has_build_41 == -1:
                    raise Build42Error("Mod compatível apenas com Build 42.")
                
        # Extrai o nome do mod
        title = soup.find('div', class_='workshopItemTitle').text.strip()

        # Extrai o ID do mod da descrição
        mod_id_element = soup.find('div', class_='workshopItemDescription').get_text(separator="\n").strip()
        if mod_id_element:
            match = re.search(r'Mod ID:(.*)', mod_id_element)
            if match:
                mod_id_text = match.group(1).split('\n')[0].strip()
                mod_id = ','.join([s.strip() for s in mod_id_text.split(',')])

        else:
            logger.error(f"Mod ID não encontrado na descrição: {url}")
            results['errors'].append(f"Mod ID não encontrado na descrição: {url}")
            return None, None, None, results

        # Verifica se o mod tem requisitos obrigatórios
        # Se sim, tenta extrair o nome e ID do mod requerido
        requirements = soup.find('div', class_='requiredItemsContainer')
        if requirements:
            links = requirements.find_all('a')
            for link in links:
                requirements_url = link.get('href')
                if requirements_url:
                    results = AddMod(requirements_url, user)

        return title, workshop_id, mod_id, results

    except Build42Error:
        raise

    except Exception as e:
        logger.error(f"Erro no scraping: {e}, url={url}, workshop_id={workshop_id}, mod_id={mod_id if 'mod_id' in locals() else 'N/A'}")
        results['errors'].append(f"Erro no scraping: {e}, url={url}")
        return None, None, None, results


def AddMod(urls, user):
    """
    Função auxiliar para mods diretamente ao banco de dados.
    """
    results = { 'errors': [], 'success': [] }

    for url in urls.split(';'):
        url = url.strip()
        try:
            name, workshop_id, mod_id, results = scrappling_steam_workshop(url, user)

            if results['errors']:
                results['errors'].append(name if name else url)
                continue

            mod, created = Mod.objects.get_or_create(
                mod_id=mod_id,
                defaults={
                    'workshop_id': workshop_id,
                    'status': 'disabled',
                    'name': name,
                    'mod_link': url,
                    'suggested_by': user,
                }
            )
            if created:
                results['success'].append(name)
            else:
                results['errors'].append(f"{name} já existe.")

        except Build42Error as e:
            logger.error(f"Erro ao adicionar mod: {e}, url={url}, workshop_id={workshop_id}, mod_id={mod_id if 'mod_id' in locals() else 'N/A'}, user={user.username if user else 'N/A'}")
            results['errors'].append(f"{name if name else url} - {str(e)}")

        except IntegrityError as e:
            logger.error(f"Erro de integridade ao adicionar mod: {e}, url={url}, workshop_id={workshop_id}, mod_id={mod_id if 'mod_id' in locals() else 'N/A'}, user={user.username if user else 'N/A'}")
            results['errors'].append(f"{name if name else url} - Mod já existe.")

        except Exception as e:
            logger.error(f"Erro inesperado ao adicionar mod: {e}, url={url}, workshop_id={workshop_id}, mod_id={mod_id if 'mod_id' in locals() else 'N/A'}, user={user.username if user else 'N/A'}")
            results['errors'].append(f"{name if name else url} - Erro inesperado: {str(e)}")

    return results


def update_server_mods():
    """
    Lê a configuração do servidor PZ, atualiza os mods com base nos
    mods ativos no banco de dados e salva o arquivo de volta
    """
    enabled_mods = Mod.objects.filter(status='enabled')
    workshop_ids = ';'.join([mod.workshop_id for mod in enabled_mods])

    mod_id = ';'.join([mod.mod_id for mod in enabled_mods])

    file_path = settings.PZ_CONFIG_PATH
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("WorkshopItems="):
            line = f"WorkshopItems={workshop_ids}\n"
        elif line.startswith("Mods="):
            line = f"Mods={mod_id}\n"
        new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


RESTART_PENDING_KEY = 'server_restart_pending'

def set_restart_pending_flag(is_pending: bool):
    """
    Define o flag de reinicialização pendente no cache.
    """
    cache.set(RESTART_PENDING_KEY, is_pending, 86400)


def is_restart_pending():
    """
    Verifica se o flag de reinicialização pendente está definido no cache.
    Retorna True se estiver pendente, caso contrário, False.
    """
    return cache.get(RESTART_PENDING_KEY, False)

def is_pz_server_running():
    """
    Verifica se o processo do servidor Project Zomboid está a rodar.
    Retorna True se o processo for encontrado, caso contrário False.
    """
   
    for proc in psutil.process_iter(['name', 'username']):
        try:
            
            if 'ProjectZomboid' in proc.info['name'] and proc.info['username'] == 'pzuser':
                return True 
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            
            pass
    return False 

def get_server_status():
    """
    Verifica se o processo do servidor está rodando.
    Retorna uma tupla: (status_code, status_text, status_color)
    """
    if is_pz_server_running():
        if is_restart_pending():
            return ('pending_restart', 'Reinicialização Pendente', 'warning')
        else:
            return ('running', 'Rodando', 'success')
    else:
        return ('stopped', 'Parado', 'danger')