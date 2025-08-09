import re

from bs4 import BeautifulSoup
import requests

class Build42Error(Exception):
    """Custom exception for Build 42 errors."""
    pass


class RequiredModError(Exception):
    """Custom exception for required mod errors."""
    pass


def scrappling_steam_workshop(url):
    try:
        match = re.search(r'id=(\d+)', url)
        if not match:
            return None, None, None
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
        mod_id_element = soup.find('div', class_='workshopItemDescription').text.strip()
        if mod_id_element:
            mod_ids_text = mod_id_element.split('Mod ID:')[1].strip()
            mod_ids = ','.join([s.strip() for s in mod_ids_text.split(',')])

        else:
            print("Mod ID not found in the page.")
            return None, None, None
        
        # Verifica se o mod tem requisitos obrigatórios
        # Se sim, tenta extrair o nome e ID do mod requerido
        requirements = soup.find('div', class_='requiredItemsContainer')
        if requirements:
            requirements_url = requirements.find('a')['href']
            AddModDirectly(requirements_url)

        return title, workshop_id, mod_ids
    
    except Build42Error:
        raise

    except Exception as e:
        print(f"Erro no scraping: {e}")
        return None, None, None
    
def AddModDirectly(url):
    """
    Função auxiliar para adicionar um mod diretamente ao banco de dados.
    """
    name, workshop_id, mod_id = scrappling_steam_workshop(url)
    if not name or not workshop_id or not mod_id:
        raise RequiredModError("Mod não encontrado ou inválido.")
    
    mod = Mod(
        mod_id=mod_id,
        workshop_id=workshop_id,
        status='disabled',
        name=name,
        mod_link=url,
        suggested_by=None,
    )
    mod.save()