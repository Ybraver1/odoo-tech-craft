import requests

class WiseAPI:
    #BASE_URL = "https://api.sandbox.transferwise.tech"

    def __init__(self, token, profile_id,url):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.profile_id = profile_id
        self.base_url = url

    def create_quote(self, sourceCurrency, targetCurrency, amount,targetAccount):
        data = {           
            "sourceCurrency": sourceCurrency,
            "targetCurrency": targetCurrency,
            "rateType": "FIXED",
            "sourceAmount": amount,
            "targetAccount": targetAccount,
        }
        return requests.post(f"{self.base_url}/v3/profiles/{self.profile_id}/quotes", headers=self.headers, json=data).json()

    def create_recipient(self, account_holder_name, email, currency):
        data = {            
            "accountHolderName": account_holder_name,
            "currency": currency,
            "profile": self.profile_id,
            "type": "email",
            "details": {
                "email": email
            }
        }
        return requests.post(f"{self.base_url}/v1/accounts", headers=self.headers, json=data).json()

    def create_transfer(self, target_account_id, quote_id, customer_transaction_id, reference):
        data = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id,
            "details": {"reference": reference}
        }
        return requests.post(f"{self.base_url}/v1/transfers", headers=self.headers, json=data).json()