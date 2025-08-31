import requests
import json
from config import API_KEY, BASE_URL, FALLBACK_RATES

def get_exchange_rate(from_curr, to_curr):
    if from_curr == to_curr:
        return 1.0
        
    try:
        if API_KEY == "eb52adf56dfc84523b43f714" or not API_KEY:
            print("Using fallback rates - no API key provided")
            if from_curr in FALLBACK_RATES and to_curr in FALLBACK_RATES:
                return FALLBACK_RATES[to_curr] / FALLBACK_RATES[from_curr]
            return None
            
        response = requests.get(BASE_URL)
        response.raise_for_status()
        data = response.json()
        
        if data["result"] == "success":
            rates = data["conversion_rates"]
            from_rate = rates.get(from_curr)
            to_rate = rates.get(to_curr)
            if from_rate and to_rate:
                return to_rate / from_rate
        print("Error: Failed to fetch rates. Using offline defaults.")
        return None
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"API Error: {e}")
        if from_curr in FALLBACK_RATES and to_curr in FALLBACK_RATES:
            return FALLBACK_RATES[to_curr] / FALLBACK_RATES[from_curr]
        return None

def convert_currency(amount, from_curr, to_curr):
    rate = get_exchange_rate(from_curr, to_curr)
    if rate is None:
        return None
    return round(amount * rate, 2)