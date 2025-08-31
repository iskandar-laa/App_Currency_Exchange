from flask import render_template, request, jsonify
from app.core import convert_currency
from app.utils import save_transaction
import pandas as pd
from config import FALLBACK_RATES

def setup_routes(app):
    @app.route('/', methods=['GET'])
    def home():
        return render_template('index.html', currencies=list(FALLBACK_RATES.keys()))

    @app.route('/convert', methods=['POST'])
    def convert():
        if request.method == 'POST':
            try:
                if request.is_json:
                    data = request.get_json()
                else:
                    data = request.form
                
                amount = float(data['amount'])
                from_curr = data['from_curr'].upper()
                to_curr = data['to_curr'].upper()

                if from_curr not in FALLBACK_RATES or to_curr not in FALLBACK_RATES:
                    return jsonify({"error": "Unsupported currency"}), 400

                result = convert_currency(amount, from_curr, to_curr)
                if result is None:
                    return jsonify({"error": "Conversion failed"}), 400

                save_transaction(amount, from_curr, to_curr, result)
                return jsonify({
                    "amount": amount,
                    "from_curr": from_curr,
                    "to_curr": to_curr,
                    "result": result,
                    "rate": result/amount
                })
            except ValueError:
                return jsonify({"error": "Invalid amount"}), 400
            except KeyError:
                return jsonify({"error": "Missing required parameters"}), 400
        else:
            return jsonify({"error": "Method not allowed"}), 405

    @app.route('/history')
    def history():
        try:
            df = pd.read_csv("transactions.csv", 
                            names=["DateTime", "Amount", "From", "To", "Result", "Rate"])
            table_html = df.to_html(classes='table table-striped', index=False)
            
            total_transactions = len(df)
            most_from = df['From'].mode()[0] if not df['From'].mode().empty else "N/A"
            most_to = df['To'].mode()[0] if not df['To'].mode().empty else "N/A"
            
            if not df.empty:
                largest_idx = df['Amount'].idxmax()
                largest_amount = f"{df.loc[largest_idx, 'Amount']} {df.loc[largest_idx, 'From']}"
            else:
                largest_amount = "N/A"
            
            return render_template('history.html', 
                                table=table_html,
                                total_transactions=total_transactions,
                                most_from=most_from,
                                most_to=most_to,
                                largest_amount=largest_amount)
        except FileNotFoundError:
            return render_template('history.html', error="No transactions found")