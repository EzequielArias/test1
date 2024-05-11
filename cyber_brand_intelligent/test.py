import requests
import json
"""
self.url_call = "https://api.github.com"
        self.headers_call = { 
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
       'Accept': "application/vnd.github+json",
       'Charset': 'utf-8',
       'Content-Type': "application/json",
       'Authorization' : "",
       'X-GitHub-Api-Version' : "2022-11-28"
        }  
"""

class GitHubApi:
    url_call = ""
    headers_call = {}
    def __init__(self) -> None:
        self.url_call = "https://api.github.com"
        self.headers_call = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': "application/vnd.github+json",
        'Charset': 'utf-8',
        'Content-Type': "application/json",
        'Authorization' : "",
        'X-GitHub-Api-Version' : "2022-11-28"
        }  

    def main(self):
        request = requests.get("https://api.github.com",headers=self.headers_call)

""" 
 def searchByRepository(self, query):
       #user
       #repository
       #__package__
       self.generate_query_request(query)
       self.request_factory = RequestFactory(url_call=self.base_url, headers_call=self.headers)
       
       try:
           self.request_factory.make_request(type_request="GET", endpoint='/search/repositories', body=self.request_data)
           if self.request_factory.fail_response == False:
               
               total_data = self.request_factory.response_data.get('total_count')
               if total_data == 0:
                 
                   self.request_factory.response_data['items'] = []

                    #self.searchByUser(item)
                    #self.searchByPackage(item)
                  

               return {"code": self.request_factory.status_code_response,
                       "data": self.request_factory.response_data
                       }
           else:
               return {"code": f"{self.request_factory.status_code_response}",
                       "error": f"{self.request_factory.reason_response}"
                       }

       except self.request_factory.RequestException as s:
           return {"error": f"RequestException: {s}"}


- search

    si necesito filtrar por X
        enriquecer por User
        enriquecer por Package
        enriquecer por 
"""