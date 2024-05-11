import requests
from typing import Optional
#from pydantic import BaseModel, HttpUrl
from datetime import datetime

#class RequestFactory(BaseModel):
class RequestFactory():
    #url_call: HttpUrl
    url_call = ""
    headers_call: Optional[dict] = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json',
    'Charset': 'utf-8',
    'Content-Type': 'application/json'
    }
    endpoint_call: str = ''
    body_call: Optional[dict] = None
    type_request: str = 'GET'
    url_response: str = ''
    elapsed_response: Optional[datetime] = None
    content_response: Optional[str] = ''
    encoding_response: Optional[str] = 'utf-8'
    headers_response: Optional[str] = ''
    reason_response: Optional[str] = ''
    status_code_response: Optional[int] = 0
    fail_response: Optional[bool] = False
    response_data: Optional[dict] = None
    
    def __init__(self, url_call, headers_call) -> None:
        self.url_call = url_call
        self.headers_call = headers_call
            
    def make_request(self,type_request, endpoint, body=None)-> None:
        
        if body is not None:
            self.body_call = body
        try:
            if type_request == "GET":
                response = requests.get(f"{self.url_call}{endpoint}",
                headers=self.headers_call,
                params=self.body_call
                )
            else:
                response = requests.post(f"{self.url_call}{endpoint}",
                headers= self.headers_call,
                json= self.body_call,
                )
                
            self.url_response = response.url
            self.elapsed_response = response.elapsed
            self.encoding_response = response.encoding
            self.headers_response = response.headers
            self.reason_response = response.reason
            self.status_code_response = response.status_code
            self.content_response = response.content
            content_type_header = response.headers.get('Content-Type')
            content_type_parts = content_type_header.split(';')
            content_type = content_type_parts[0].strip()
            if response.reason == "OK":
                if content_type == "application/json":
                    self.response_data = response.json()
                else:
                    self.response_data = response.text
                    self.fail_response = False
            else:
                self.fail_response = True
        except requests.exceptions.RequestException as e:
            self.fail_response = True
            self.content_response = f"{e}"






"""

connector.apply_credential(app_config.fast_api_app.environments.config_data['account_data'][connector_data.name][0])
# if search_data.extra_params !='':
# search_data.extra_params = search_data.extra_params
query = connector.transform_search_query_data(search_data.query,
search_data.exclude_query,
search_data.extra_params,
domain_glossary_data,
company_glossary_data)
# SEARCH DATA
result_search = connector.search(query)
if result_search.get('code') == 200:
# NORMALIZE DATA FROM CONNECTOR
connector.normalize(result_search.get('data'))
else:
raise ValueError(result_search.get('error'))"""