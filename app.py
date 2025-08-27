from flask import Flask
from threading import Thread
import webbrowser
import os
from app.routes import setup_routes
from app.gui import gui_version
from app.utils import view_transaction_history, save_transaction
from app.core import convert_currency
from config import FALLBACK_RATES
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

app = Flask(__name__)
setup_routes(app)

def setup_templates():
    os.makedirs("templates", exist_ok=True)
    if not os.path.exists("templates/index.html"):
        with open("templates/index.html", "w") as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Currency Exchange</title>
</head>
<body>
    <h1>Currency Exchange</h1>
    <form id="conversionForm">
        <input type="number" name="amount" placeholder="Amount" required>
        <select name="from_curr">
            {% for currency in currencies %}
            <option value="{{ currency }}">{{ currency }}</option>
            {% endfor %}
        </select>
        to
        <select name="to_curr">
            {% for currency in currencies %}
            <option value="{{ currency }}">{{ currency }}</option>
            {% endfor %}
        </select>
        <button type="submit">Convert</button>
    </form>
    <div id="result"></div>
    <a href="/history">View History</a>
</body>
</html>""")
    
    if not os.path.exists("templates/history.html"):
        with open("templates/history.html", "w") as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Transaction History</title>
</head>
<body>
    <h1>Transaction History</h1>
    {% if error %}
        <p>{{ error }}</p>
    {% else %}
        {{ tables[0]|safe }}
    {% endif %}
    <a href="/">Back to Converter</a>
</body>
</html>""")

def run_flask_app():
    app.run(debug=False, use_reloader=False, port=5000)

def cli_convert_currency():
    try:
        amount = float(input("\nEnter amount (0 to cancel): "))
        if amount == 0:
            return
        print(f"Available currencies: {', '.join(FALLBACK_RATES.keys())}")
        from_curr = input("From currency: ").upper()
        to_curr = input("To currency: ").upper()

        if from_curr not in FALLBACK_RATES or to_curr not in FALLBACK_RATES:
            print("Error: Unsupported currency.")
            return

        result = convert_currency(amount, from_curr, to_curr)
        if result is None:
            print("Error: Conversion failed.")
        else:
            print(f"\n{amount} {from_curr} = {result} {to_curr}")
            print(f"Rate: 1 {from_curr} = {result/amount:.6f} {to_curr}")
            save_transaction(amount, from_curr, to_curr, result)
    except ValueError:
        print("Error: Please enter a valid number.")

def main():
    setup_templates()
    
    flask_thread = Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    
    webbrowser.open('http://127.0.0.1:5000')
    
    print("\n=== REAL-TIME CURRENCY EXCHANGE ===")
    print(f"Supported currencies: {', '.join(FALLBACK_RATES.keys())}")
    print("Web interface opened in your browser (http://127.0.0.1:5000)")
    
    while True:
        print("\nOptions:")
        print("1. Convert Currency (CLI)")
        print("2. View Transaction History (CLI)")
        print("3. Open Desktop GUI Version")
        print("4. Exit")
        choice = input("Select option (1-4): ").strip()
        
        if choice == "1":
            cli_convert_currency()
        elif choice == "2":
            view_transaction_history()
        elif choice == "3":
            print("Launching Desktop GUI version...")
            gui_version()
        elif choice == "4":
            print("Exiting... Thank you for using the Currency Exchange!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()