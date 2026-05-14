# 💰 Finance Agent

A personal AI-powered finance assistant that connects to your bank accounts and helps you track daily spending, analyze transactions, and manage installment payments — all powered by Claude AI.

## Features

- 🏦 **Multi-bank Connection** — Connect multiple bank accounts simultaneously via Plaid
- 📊 **Daily Spending Chart** — Visualize your spending over the last 30 days
- 💳 **Pay Over Time Tracker** — Track installment payments and see exactly how much you owe each month
- 🤖 **AI Analysis** — Ask Claude anything about your finances in plain English

## Tech Stack

- **Backend** — Python, Flask
- **Bank Data** — Plaid API
- **AI** — Anthropic Claude API
- **Frontend** — HTML, CSS, JavaScript, Chart.js

## Getting Started

### Prerequisites

- Python 3.9+
- Plaid account ([dashboard.plaid.com](https://dashboard.plaid.com))
- Anthropic account ([console.anthropic.com](https://console.anthropic.com))

### Installation

1. Clone the repository

```bash
   git clone https://github.com/lukeku-dev/finance-agent.git
   cd finance-agent
```

2. Install dependencies

```bash
   pip install plaid-python flask python-dotenv anthropic
```

3. Create a `.env` file in the root directory

PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_secret
ANTHROPIC_API_KEY=your_anthropic_api_key

4. Run the app

```bash
   python3 app.py
```

5. Open your browser and go to `http://127.0.0.1:5000`

## Usage

1. Click **Connect a Bank** and link your bank account via Plaid
2. View your **Daily Spending Chart** automatically populated with real transaction data
3. Add **Pay Over Time** installment plans to track monthly payments
4. Use the **Ask Claude** section to ask questions like:
   - _"How much did I spend this week?"_
   - _"Which category did I spend the most on?"_
   - _"How much do I owe in total this month?"_

## Security

- Bank credentials are never stored — handled securely by Plaid
- API keys are stored locally in `.env` and never committed to version control
- Plaid access is **read-only** — the app cannot move or transfer money

## License

MIT License
