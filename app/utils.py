# app/utils.py
import csv
from datetime import datetime
import pandas as pd
from config import FALLBACK_RATES

def save_transaction(amount, from_curr, to_curr, result):
    try:
        with open("transactions.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                amount,
                from_curr,
                to_curr,
                result,
                f"1 {from_curr} = {result/amount:.6f} {to_curr}"
            ])
    except Exception as e:
        print(f"Error saving transaction: {e}")

def view_transaction_history():
    try:
        df = pd.read_csv("transactions.csv", 
                        names=["DateTime", "Amount", "From", "To", "Result", "Rate"])
        print("\n=== TRANSACTION HISTORY ===")
        print(df.to_markdown(index=False))
        
        print("\n=== STATISTICS ===")
        print(f"Total Conversions: {len(df)}")
        print(f"Most Converted From: {df['From'].mode()[0]}")
        print(f"Most Converted To: {df['To'].mode()[0]}")
        print(f"Largest Transaction: {df['Amount'].max()} {df.loc[df['Amount'].idxmax(), 'From']}")
    except FileNotFoundError:
        print("No transactions found. Convert some currencies first!")
    except Exception as e:
        print(f"Error reading history: {e}")