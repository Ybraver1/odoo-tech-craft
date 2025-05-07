import json
import logging
import requests
import pprint

_logger = logging.getLogger(__name__)

class CardknoxAPI:

    """
    Class for handling Cardknox API requests.
    """    

    def __init__(self, provider):
        """
        Initialize the Cardknox API client.
        
        :param provider: The payment provider record
        """
        self.software_name = "Tech Craft Odoo"
        self.software_version = "1.0"
        self.url = "https://x1.cardknox.com/gatewayjson"
        self.api_version = "5.0.0"
        self.key = provider.cardknox_token
        self.provider = provider

    def _make_request(self, body):
        """
        Make a request to the Cardknox API.
        
        :param body: The request body
        :return: The API response
        """
        try:
            _logger.info("Making request to Cardknox API")
            response = requests.post(self.url, json=body)
            response.raise_for_status()
            result = response.json()
            
            # Log the response (excluding sensitive data)
            log_result = result.copy() if isinstance(result, dict) else {}
            if 'xToken' in log_result:
                log_result['xToken'] = '[REDACTED]'
            if 'xCardNum' in log_result:
                log_result['xCardNum'] = '[REDACTED]'
            _logger.info("Cardknox API response: %s", pprint.pformat(log_result))
            
            return result
        except requests.exceptions.RequestException as e:
            _logger.error("Error making request to Cardknox API: %s", str(e))
            raise
        except json.JSONDecodeError as e:
            _logger.error("Error decoding Cardknox API response: %s", str(e))
            raise
    
    def _create_base_body(self):
        """
        Create the base request body with common parameters.
        
        :return: The base request body
        """
        body = {
            'xKey': self.key,
            'xVersion': self.api_version,
            'xSoftwareName': self.software_name,
            'xSoftwareVersion': self.software_version
        }
        return body
    
    def _save_token(self, card_token=None, card_number=None, exp_date=None, cvv=None, zip_code=None):
        """
        Save a payment token.
        
        :param card_token: The card token from iFields
        :param card_number: The card number (only used if not using iFields)
        :param exp_date: The expiration date (only used if not using iFields)
        :param cvv: The CVV (only used if not using iFields)
        :param zip_code: The billing ZIP code
        :return: The API response
        """
        body = self._create_base_body()
        
        # If using iFields token
        if card_token:
            body['xToken'] = card_token
        # If using direct card data (not recommended for PCI compliance)
        elif card_number and exp_date:
            body['xCardNum'] = card_number
            body['xExp'] = exp_date
            if cvv:
                body['xCVV'] = cvv
        else:
            raise ValueError("Either card_token or card_number and exp_date must be provided")
            
        if zip_code:
            body['xZip'] = zip_code
            
        body['xCommand'] = 'cc:Save'
        
        return self._make_request(body)
        
    def process_payment(self, amount, reference, card_token=None, token_id=None, customer_name=None, customer_email=None, billing_address=None):
        """
        Process a payment.
        
        :param amount: The payment amount
        :param reference: The payment reference
        :param card_token: The card token from iFields (for one-time payments)
        :param token_id: The saved token ID (for recurring payments)
        :param customer_name: The customer name
        :param customer_email: The customer email
        :param billing_address: The billing address dictionary
        :return: The API response
        """
        body = self._create_base_body()
        
        # Set the payment amount
        body['xAmount'] = str(amount)
        body['xInvoice'] = reference
        
        # Set the payment method
        if card_token:
            body['xToken'] = card_token
        elif token_id:
            body['xToken'] = token_id
        else:
            raise ValueError("Either card_token or token_id must be provided")
            
        # Set customer information if provided
        if customer_name:
            body['xName'] = customer_name
        if customer_email:
            body['xEmail'] = customer_email
            
        # Set billing address if provided
        if billing_address:
            if 'street' in billing_address:
                body['xStreet'] = billing_address['street']
            if 'city' in billing_address:
                body['xCity'] = billing_address['city']
            if 'state' in billing_address:
                body['xState'] = billing_address['state']
            if 'zip' in billing_address:
                body['xZip'] = billing_address['zip']
            if 'country' in billing_address:
                body['xCountry'] = billing_address['country']
                
        # Set the command to process the payment
        body['xCommand'] = 'cc:Sale'
        
        return self._make_request(body)
        
    def refund_payment(self, amount, reference, transaction_id):
        """
        Refund a payment.
        
        :param amount: The refund amount
        :param reference: The refund reference
        :param transaction_id: The original transaction ID
        :return: The API response
        """
        body = self._create_base_body()
        
        body['xAmount'] = str(amount)
        body['xInvoice'] = reference
        body['xRefNum'] = transaction_id
        body['xCommand'] = 'cc:Refund'
        
        return self._make_request(body)
        
    def void_payment(self, transaction_id):
        """
        Void a payment.
        
        :param transaction_id: The transaction ID to void
        :return: The API response
        """
        body = self._create_base_body()
        
        body['xRefNum'] = transaction_id
        body['xCommand'] = 'cc:Void'
        
        return self._make_request(body)
