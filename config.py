# config.py
# Using a free API instead (no key required)
API_KEY = "your_api_key_here"  # This can be left as is for fallback
BASE_URL = "https://api.exchangerate-api.com/v4/latest/USD"
FALLBACK_RATES = {
    "USD": 1.0,
    "EUR": 0.85,
    "GBP": 0.75,
    "JPY": 110.0,
    "MYR": 4.20,
    "SGD": 1.35,
    "AUD": 1.30,
    "CAD": 1.25,
    "CNY": 6.45,
    "INR": 74.0
}