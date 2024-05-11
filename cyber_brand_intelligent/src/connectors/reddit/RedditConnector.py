from connectors.Connector import Connector
from typing import Optional
from connectors.ApiCall import RequestFactory
from datetime import datetime



class RedditConnector(Connector):

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

    def refresh_access_token(self):
        pass

    def apply_credentials(self, credentials : Optional[dict]) -> None:
        self.headers["Authorization"] = credentials["Authorization"]
        self.headers["Accept"] = credentials["Accept"]
        self.headers["X-GitHub-Api-Version"] = credentials["X-GitHub-Api-Version"]
        print(self.headers)

    def normalize(self, data) -> dict:
       return_data = []
       print('this is mi elapsed from normalize')
       print(self.request_factory.elapsed_response)
       self.normalize_audit_data(self.request_factory.elapsed_response)
       self.normalize_connector_github(data)

       data = data.get('items')
       
       for item in data:
           item['id'] = item.get('id') 
           item['node_id'] = item.get('node_id')
           item['name'] = item.get('name')
           item['owner'] = item.get('owner')
           item['html_url'] = item.get('html_url')
           item['timestamps'] = {
               "create_at" : item.get('created_at'),
               "pushed_at" : item.get('pushed_at'),
               "updated_at" : item.get('updated_at')
           }

           return_data.append(item)
 
       self.information_found = return_data
 
    def normalize_audit_data(self, data):
       self.audit_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       self.audit_data['updated_at'] = None # Fix this when duplicate results
       self.audit_data['elapsed_time'] = data

    def normalize_connector_github(self, data):
       connector_data = {}
       connector_data['name_conector'] = 'Github'
       connector_data['configuration_search_connector'] = self.query_for_the_requests
    
    def transform_search_query_data(self, query: str, exclude_term: str = '', extra_params: dict = {}, domain_glossary_data = None, company_glossary_data = None) -> None:
        query_search = {}
        query_search['extra_params'] = extra_params 
        query_search['q'] = query 
        query_search['exclude_terms'] = exclude_term
      
        return query_search
   
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
    


"""

"""