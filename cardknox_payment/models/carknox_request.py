import json
import requests
import pprint

class CardknoxAPI:


    def __init__(self,provider):
        self.software_name = "Tech Craft Odoo"
        self.software_version = "1.0"
        self.url = "https://x1.cardknox.com/gatewayjson"
        self.api_version = "5.0.0"
        self.key = provider.cardknox_token

    def _make_request(self,body):
        response = requests.post(self.url,json.dump(body))
        response.raise_for_status()
        response = json.loads(response.content)
        return response
    
    def _create_base_body(self):
        body = {
            'xKey':self.key,
            'xVersion':self.api_version,
            'xSoftwareName':self.software_name,
            'xSoftwareVersion':self.software_version
        }
        return body
    
    def _save_token(self,cc_number,exp_dade,cvv,zip):
        body = self._create_base_body()
        body['xCardNum'] = cc_number
        body['xExp'] = exp_dade
        body['xCVV'] = cvv
        body['xZip'] = zip
        body['xCommand'] = 'cc:Save'

        res = self._make_request(body)

