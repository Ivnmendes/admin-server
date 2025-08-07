import configparser
import io
from .models import Mod
import requests
from bs4 import BeautifulSoup
import re
from django.conf import settings
from django.core.cache import cache

def scrappling_steam_workshop(url):
    try:
        match = re.search(r'id=(\d+)', url)

        if not match:
            return None, None, None

        workshop_id = match.group(1)

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('div', class_='workshopItemTitle').text.strip()

        mod_id_element = soup.find('div', class_='workshopItemDescription').text.strip()

        if mod_id_element:
            mod_ids_text = mod_id_element.split('Mod ID:')[1].strip()
            mod_ids = ','.join([s.strip() for s in mod_ids_text.split(',')])
        else:
            print("Mod ID not found in the page.")
            return None, None, None

        return title, workshop_id, mod_ids
    
    except Exception as e:
        print(f"Erro no scraping: {e}")
        return None, None, None
    
def update_server_mods():
    """
    Lê a configuração do servidor PZ, atualiza os mods com base nos
    mods ativos no banco de dados e salva o arquivo de volta
    sem os cabeçalhos de seção.
    """
    enabled_mods = Mod.objects.filter(status='enabled')
    workshop_ids = ';'.join([mod.workshop_id for mod in enabled_mods])

    mod_id = ';'.join([mod.mod_id for mod in enabled_mods])

    config = configparser.ConfigParser()
    dummy_section = 'PZServerSettings'

    try:
        with open(settings.PZ_CONFIG_PATH, 'r') as f:
            config_string = f'[{dummy_section}]\n{f.read()}'
        config.read_string(config_string)
    except FileNotFoundError:
        config.add_section(dummy_section)

    config.set(dummy_section, 'WorkshopItems', workshop_ids)
    config.set(dummy_section, 'Mods', mod_id)

    string_io = io.StringIO()
    config.write(string_io)
    config_string_with_header = string_io.getvalue()

    lines = config_string_with_header.split('\n', 1)
    cleaned_config = lines[1] if len(lines) > 1 else ''

    with open(settings.PZ_CONFIG_PATH, 'w') as configfile:
        configfile.write(cleaned_config)


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