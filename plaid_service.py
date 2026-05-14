import os
from dotenv import load_dotenv
import plaid
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from datetime import date, timedelta

load_dotenv()

configuration = plaid.Configuration(
    host=plaid.Environment.Production,
    api_key={
        'clientId': os.getenv('PLAID_CLIENT_ID'),
        'secret': os.getenv('PLAID_SECRET'),
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

def create_link_token():
    request = LinkTokenCreateRequest(
        products=[Products("transactions")],
        client_name="Finance Agent",
        country_codes=[CountryCode("US")],
        language="en",
        redirect_uri="http://localhost:5000",
        user=LinkTokenCreateRequestUser(client_user_id="user-001")
    )
    response = client.link_token_create(request)
    return response['link_token']

def exchange_public_token(public_token):
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = client.item_public_token_exchange(request)
    return response['access_token']

def get_transactions(access_token, days=30):
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
    )
    response = client.transactions_get(request)
    return response['transactions']