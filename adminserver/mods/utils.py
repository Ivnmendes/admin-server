import requests
from bs4 import BeautifulSoup
import re

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
    