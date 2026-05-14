import os
from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv
from plaid_service import create_link_token, exchange_public_token, get_transactions
import anthropic
from collections import defaultdict

load_dotenv()

app = Flask(__name__)
app.secret_key = "finance-agent-secret"

anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/create_link_token", methods=["POST"])
def link_token():
    token = create_link_token()
    return jsonify({"link_token": token})

@app.route("/api/exchange_token", methods=["POST"])
def exchange_token():
    public_token = request.json.get("public_token")
    bank_name = request.json.get("bank_name", "Bank")
    access_token = exchange_public_token(public_token)
    
    # 存多個銀行
    accounts = session.get("accounts", {})
    accounts[bank_name] = access_token
    session["accounts"] = accounts
    session.modified = True
    return jsonify({"status": "success", "accounts": list(accounts.keys())})

@app.route("/api/accounts", methods=["GET"])
def get_accounts():
    accounts = session.get("accounts", {})
    return jsonify({"accounts": list(accounts.keys())})

@app.route("/api/chart_data", methods=["POST"])
def chart_data():
    accounts = session.get("accounts", {})
    if not accounts:
        return jsonify({"error": "No bank connected"}), 400

    all_transactions = []
    for bank_name, access_token in accounts.items():
        txs = get_transactions(access_token, days=30)
        for tx in txs:
            tx['bank'] = bank_name
        all_transactions.extend(txs)

    daily = defaultdict(float)
    for tx in all_transactions:
        daily[str(tx['date'])] += float(tx['amount'])

    sorted_daily = sorted(daily.items())
    return jsonify({
        "daily": [{"date": d, "amount": round(a, 2)} for d, a in sorted_daily],
        "tx_count": len(all_transactions)
    })

@app.route("/api/analyze", methods=["POST"])
def analyze():
    accounts = session.get("accounts", {})
    if not accounts:
        return jsonify({"error": "No bank connected"}), 400

    all_transactions = []
    for bank_name, access_token in accounts.items():
        txs = get_transactions(access_token, days=30)
        for tx in txs:
            tx['bank'] = bank_name
        all_transactions.extend(txs)

    user_question = request.json.get("question", "Summarize my spending")
    interest_cards = request.json.get("interest_cards", [])

    tx_text = "\n".join([
        f"{tx['date']} | {tx['bank']} | {tx['name']} | ${tx['amount']}"
        for tx in all_transactions
    ])

    interest_text = ""
    if interest_cards:
        interest_text = "\n\nCredit cards with interest (Pay Over Time):\n"
        for card in interest_cards:
            interest_text += f"- {card['name']}: balance ${card['balance']}, APR {card['apr']}%\n"
        interest_text += "\nPlease calculate monthly interest charges and total cost if minimum payments are made."

    message = anthropic_client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""You are a personal finance assistant.
Here are my recent transactions from all my bank accounts:
{tx_text}
{interest_text}

Question: {user_question}"""
        }]
    )

    return jsonify({"response": message.content[0].text})

if __name__ == "__main__":
    app.run(debug=True)