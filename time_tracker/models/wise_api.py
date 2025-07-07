import requests

class WiseAPI:
    BASE_URL = "https://api.sandbox.transferwise.tech"

    def __init__(self, token, profile_id):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.profile_id = profile_id

    def create_quote(self, sourceCurrency, targetCurrency, amount):
        data = {           
            "sourceCurrency": sourceCurrency,
            "targetCurrency": targetCurrency,
            "rateType": "FIXED",
            "sourceAmount": amount
        }
        return requests.post(f"{self.BASE_URL}/v1/quotes", headers=self.headers, json=data).json()

    def create_recipient(self, account_holder_name, email, currency):
        data = {            
            "accountHolderName": account_holder_name,
            "currency": currency,
            "type": "email",
            "details": {
                "email": email
            }
        }
        return requests.post(f"{self.BASE_URL}/v1/accounts", headers=self.headers, json=data).json()

    def create_transfer(self, target_account_id, quote_id, customer_transaction_id):
        data = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id,
            "details": {"reference": "Freelance payment"}
        }
        return requests.post(f"{self.BASE_URL}/v1/transfers", headers=self.headers, json=data).json()