import requests
import json
from datetime import datetime

def obtenir_temperatures(lat, lon):
    # Data d'avui en format AAAA-MM-DD
    data_avui = datetime.utcnow().strftime('%Y-%m-%d')
    
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&hourly=temperature_2m&start_date={data_avui}&end_date={data_avui}&timezone=UTC"
    )
    
    resposta = requests.get(url)
    resposta.raise_for_status()
    dades = resposta.json()
    
    temperatures = dades.get("hourly", {}).get("temperature_2m", [])
    return temperatures, data_avui

def calcular_stats(temps):
    if not temps:
        return None
    temp_max = max(temps)
    temp_min = min(temps)
    temp_mitjana = sum(temps) / len(temps)
    return {"maxima": temp_max, "minima": temp_min, "mitjana": temp_mitjana}

def exportar_json(stats, data):
    nom_fitxer = f"temp_{data.replace('-', '')}.json"
    with open(nom_fitxer, "w") as f:
        json.dump(stats, f, indent=4)
    print(f"Dades exportades a {nom_fitxer}")

def main():
    # Exemple: Barcelona
    lat = 41.3874
    lon = 2.1686
    
    temperatures, data = obtenir_temperatures(lat, lon)
    stats = calcular_stats(temperatures)
    if stats:
        exportar_json(stats, data)
    else:
        print("No s'han trobat temperatures per avui.")

if __name__ == "__main__":
    main()
