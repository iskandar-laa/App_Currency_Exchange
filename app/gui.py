from tkinter import *
import tkinter.messagebox as mb
from app.core import convert_currency
from app.utils import save_transaction
import pandas as pd
from config import FALLBACK_RATES

def gui_version():
    def perform_conversion():
        try:
            amount = float(amount_entry.get())
            from_curr = from_var.get()
            to_curr = to_var.get()
            
            result = convert_currency(amount, from_curr, to_curr)
            if result is None:
                mb.showerror("Error", "Conversion failed. Check currencies and connection.")
            else:
                save_transaction(amount, from_curr, to_curr, result)
                result_label.config(text=f"{amount} {from_curr} = {result:.2f} {to_curr}\nRate: 1 {from_curr} = {result/amount:.6f} {to_curr}")
        except ValueError:
            mb.showerror("Error", "Please enter a valid amount")

    root = Tk()
    root.title("Currency Exchange Pro")
    root.geometry("400x300")

    # Widgets
    Label(root, text="Amount:").pack()
    amount_entry = Entry(root)
    amount_entry.pack()

    Label(root, text="From Currency:").pack()
    from_var = StringVar(value="MYR")
    OptionMenu(root, from_var, *FALLBACK_RATES.keys()).pack()

    Label(root, text="To Currency:").pack()
    to_var = StringVar(value="USD")
    OptionMenu(root, to_var, *FALLBACK_RATES.keys()).pack()

    Button(root, text="Convert", command=perform_conversion).pack(pady=10)
    result_label = Label(root, text="", font=('Arial', 10))
    result_label.pack()

    Button(root, text="View History", command=lambda: mb.showinfo("History", pd.read_csv("transactions.csv").to_string())).pack()
    
    root.mainloop()