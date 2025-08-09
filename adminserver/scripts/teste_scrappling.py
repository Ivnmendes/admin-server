import sys
from stw import scrappling_steam_workshop  # Ajuste o nome do módulo se necessário

def main():
    url = input("Digite a URL do mod: ")
    resultado = scrappling_steam_workshop(url)

    if resultado == (None, None, None):
        print("Falha ao extrair dados do mod.")
    else:
        title, workshop_id, mod_ids = resultado
        print(f"Título: {title}")
        print(f"Workshop ID: {workshop_id}")
        print(f"Mod IDs: {mod_ids}")

if __name__ == "__main__":
    main()
