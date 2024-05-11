from connectors.Connector import Connector
from typing import Optional
from connectors.ApiCall import RequestFactory
from datetime import datetime

# La propiedad params de requests es incompatible con calificadores y distintos tipos de filtros.
# adaptar
class GithubConnector(Connector):

    request_factory : RequestFactory
    api_key = ""
    base_url = "https://api.github.com"
    headers: Optional[dict] = { 
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
       'Accept': "application/vnd.github+json",
       'Charset': 'utf-8',
       'Content-Type': "application/json",
       'X-GitHub-Api-Version' : "2022-11-28",
    }
    request_data: dict = {}
    search_repository_results = []
    query_for_the_requests = ""  

    def __init__(self) -> None:
        super().__init__()

    def search(self, query):
      self.searchByRepository(query)

      try:
        if self.request_factory.fail_response == False:
            total_data = self.request_factory.response_data.get('total_count')

            if total_data == '0':
                self.request_factory.response_data['items']

            return {
                "code" : self.request_factory.status_code_response,
                "data" : self.request_factory.response_data
            }
        
      except self.request_factory.RequestException as s:
           return {"error": f"RequestException: {s}"} 
    
    def searchByRepository(self, query):
       self.generate_query_request(query)
       self.request_factory = RequestFactory(url_call=self.base_url, headers_call=self.headers)

       self.request_factory.make_request('GET', '/search/repositories' + self.query_for_the_requests)

       self.search_repository_results = self.request_factory.response_data.get('items')
     
    def searchByUser(self, repository_id):
        pass
    
    def searchByPackage(self, repository_id):
        pass

    def generate_query_request(self, params : dict):

        query_params = self.generate_query_params(params)
        query_params_filter = self.generate_query_filter_params(params['extra_params'])
        #query_params_locations = self.generate_query_params_locations(params)
        query_params_order_and_totals = self.generate_query_params_order_and_totals(params)


        self.query_for_the_requests += query_params
        self.query_for_the_requests += query_params_filter
        self.query_for_the_requests += query_params_order_and_totals
  
    def generate_query_credentials(self):
        pass
          
    def generate_query_params(self, params):
         query_params = ""
        
         if 'q' in params:
          query_params += '?q=' + params['q']

         return query_params

    def generate_query_filter_params(self, params):
        query_params = ""
        
        if 'created' in params:
            query_params += '+created:>' + params['created']
            
        if 'language' in params:
            query_params += '+language:' + params['language']     

        if 'pushed' in params:
            query_params += '+pushed:>' + params['pushed']

        return query_params
      
    def generate_query_params_locations(self, params):
        query_params= ""

        if 'location' in params:
            query_params += 'location:' + params['location']

        return query_params
      
    def generate_query_params_order_and_totals(self, params):
          query_params = ""

          if 'sort' in params:
              query_params += '&sort=' + params['sort']
          
          if 'order' in params:
              query_params += '&order=' + params['order']
              
          if 'per_page' in params:
              query_params += '&per_page=' + params['per_page']
          else:
              query_params += '&per_page=' + '100'

          return query_params