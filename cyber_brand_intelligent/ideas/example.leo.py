from datetime import datetime
from typing import Optional
from src.Factories.RequestFactory import RequestFactory 
from src.Core.Connectors.Connector import Connector
from src.app.DomainGlossaries.Model.DomainGlossariesModel import DomainGlossaries  
from src.app.CompanyGlossaries.Model.CompanyGlossariesModel import CompanyGlossaries
from src.app._Models.ValuesApp import TYPE_REQUEST_HEADERS

class GoogleConnector(Connector):
   """
   A class that represents a Google Connector.
   Attributes:
   - api_key (str): The API key for accessing the Google Custom Search API.
   - cx (str): The custom search engine ID.
   - base_url (str): The base URL for making requests to the Google Custom Search API.
   - headers (Optional[dict]): Optional headers for the API request.
   - request_factory (RequestFactory): An instance of the RequestFactory class for making HTTP requests.
   - request_data (dict): The data for the API request.

   # Parameters query search
       - q (str): Query search
       - or_terms (str): Multiple terms search 
       - exact_terms (str): Phrase must contain the search
       - exclude_terms (str): Term must not contain the search
       - search_type (str): Search type example: image, news, video
       - site_search (str): Site where search or not 
       - site_search_filter (str): SiteSearchFilter, include or exclude site
   
   # Filters
       - hq (str): Add operator logic, AND, OR to search
       - file_type (str): File types search
       - filter (str): Enable duplicate data filtering
       - date_restrict (str): Search for numbers date
       - high_range (str): Date in format YYYYMMDD
       - low_range (str): Date in format YYYYMMDD 
       - link_site (str): Search contain specific link to site
       - rights (str): Filter for license result  cc_attribute cc_noncommercial, etc
       - safe (str): Filter explicit content active,off    

   # Parameter location y language
       - c2coff (str): Enable o disable search chino traditional  y simplicity.
       - cr: Optional[list[str]]: Country search
       - gl (str): Location user
       - hl (str): Language user
       - lr (str): Language specify document

   # Parameter Image
       - img_color_type (str): Img color
       - img_dominant_color (str): Img with dominant color red, orange, yellow, green, teal, blue, purple, pink, white, gray, black, brown
       - img_size (str): Img size
       - img_type (str): Img Type

   # Parameter order y totals
       - num (int): Max total result
       - sort (str): Specific order result
       - start (int): Start result

   Methods:
   - __init__(self, api_key, cx): Initializes a GoogleConnector instance with the provided API key and custom search engine ID.
   - search(self, query): Performs a search using the Google Custom Search API and returns the search results.
   - generate_query_request(self, params): Generates the query parameters for the API request.
   - generate_query_credentials(self): Generates the query credentials for the API request.
   - generate_query_params(self, params): Generates the query parameters for the API request.
   - generate_query_filter_params(self, params): Generates the filter parameters for the API request.
   - generate_query_params_img(self, params): Generates the image parameters for the API request.
   - generate_query_params_locations(self, params): Generates the location parameters for the API request.
   """

   api_key: str = ''
   cx: str = ''
   base_url: str = 'https://customsearch.googleapis.com/customsearch/v1'
   headers: Optional[dict] = { 
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
       'Accept': f'{TYPE_REQUEST_HEADERS}',
       'Charset': 'utf-8',
       'Content-Type': f'{TYPE_REQUEST_HEADERS}'
   }
   request_factory: RequestFactory
   request_data: dict = {}
   q: str
   or_terms: str = ''
   exact_terms: str = ''
   exclude_terms: str = ''
   search_type: str = 'searchTypeUndefined'
   site_search: str = ''
   site_search_filter: str = ''
   hq: str = 'AND'
   file_type: str = ''
   filter: str = '1'
   date_restrict: str = 'd[7]'
   high_range: str = ''
   low_range: str = ''
   link_site: str = ''
   rights: str = ''
   safe: str = 'active'
   c2coff: str = '1'
   cr: Optional[list[str]] = ['countryAR']
   gl: str = 'ar'
   hl: str = 'es'
   lr: str = 'lang_es'
   img_color_type: str = 'color'
   img_dominant_color: str = ''
   img_size: str = 'medium'
   img_type: str = 'photo'
   num: int = 10
   sort: str = ''
   start: int = 1

   type_header_response: str = TYPE_REQUEST_HEADERS

   def __init__(self, api_key:str = '', cx:str = '') -> None:
       """
       Initializes a GoogleConnector instance with the provided API key and custom search engine ID.
       Parameters:
       - api_key (str): The API key for accessing the Google Custom Search API.
       - cx (str): The custom search engine ID.
       """

       super().__init__()
       self.api_key = api_key
       self.cx = cx
       self.base_url = 'https://customsearch.googleapis.com/customsearch/v1'

   def apply_credential(self, account:dict) -> None:
       self.api_key = account.get('key')
       self.cx = account.get('cx')

   def normalize(self, data: dict) -> None:
       return_data = []
       self.normalize_audit_data(data)
       self.normalize_connector_google(data)
       
       data = data.get('items')
       
       for item in data:
           item['kind'] = item.get('kind')
           item['title'] = item.get('title')
           item['htmlTitle'] = item.get('htmlTitle')
           item['link'] = item.get('link')
           item['displayLink'] = item.get('displayLink')
           item['snippet'] = item.get('snippet')
           item['htmlSnippet'] = item.get('htmlSnippet')
           item['cacheId'] = item.get('cacheId')
           item['formattedUrl'] = item.get('formattedUrl')
           item['htmlFormattedUrl'] = item.get('htmlFormattedUrl')
           item['pagemap'] = item.get('pagemap')

           return_data.append(item)

       self.information_found = return_data

   def normalize_audit_data(self, data: dict) -> None:
       self.audit_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       self.audit_data['updated_at'] = None # Fix this when duplicate results
       self.audit_data['elapsed_time'] = data.get('searchInformation',None).get('formattedSearchTime', None)

   def normalize_connector_google(self, data: dict) -> None:
       connector_data = {}
       connector_data['name_conector'] = 'Google'
       connector_data['configuration_search_connector'] = data.get('queries', '').get('request','')[0]

       self.connector_data = connector_data

   def transform_search_query_data(self, query: str, exclude_term: str = '', extra_params: dict = {}, domain_glossary_data: DomainGlossaries = None, company_glossary_data: CompanyGlossaries = None) -> dict:
       query_search = {}
       query_search['q'] = query
       query_search['exclude_terms'] = exclude_term
       #query_search.update(extra_params)

       return query_search

   def search(self, query) -> dict:
       """
       Performs a search using the Google Custom Search API and returns the search results.
       Parameters:
       - query (str): The search query.
       Returns:
       - dict: The search results.
       """

       self.generate_query_request(query)
       self.request_factory = RequestFactory(url_call=self.base_url, headers_call=self.headers)
       
       try:
           self.request_factory.make_request(type_request="GET", endpoint='', body=self.request_data)
           if self.request_factory.fail_response == False:
               total_data = self.request_factory.response_data.get('searchInformation').get('totalResults')
               if total_data == '0':
                   self.request_factory.response_data['items'] = []

               return {"code": self.request_factory.status_code_response,
                       "data": self.request_factory.response_data
                       }
           else:
               return {"code": f"{self.request_factory.status_code_response}",
                       "error": f"{self.request_factory.reason_response}"
                       }

       except self.request_factory.RequestException as s:
           return {"error": f"RequestException: {s}"}

   def generate_query_request(self, params: dict) -> None:
       """
       Generates the query parameters for the API request.
       Parameters:
       - params (dict): The parameters for the API request.
       """

       self.generate_query_credentials()
       query_params = self.generate_query_params(params)
       query_params_filter = self.generate_query_filter_params(params)

       if 'search_type' in params:
           query_params_img = self.generate_query_params_img(params)
           self.request_data.update(query_params_img)

       query_params_locations = self.generate_query_params_locations(params)
       query_params_order_and_totals = self.generate_query_params_order_and_totals(params)

       self.request_data.update(query_params)
       self.request_data.update(query_params_filter)        
       self.request_data.update(query_params_locations)
       self.request_data.update(query_params_order_and_totals)

   def generate_query_credentials(self) -> None:

       """
       Generates the query credentials for the API request.
       """
       self.request_data.update({'key': self.api_key, 'cx': self.cx})

   def generate_query_params(self, params: dict)-> dict:
       """
       Generates the query parameters for the API request.
       Parameters:
       - params (dict): The parameters for the API request.

       Returns:
       - dict: The query parameters.
       """

       query_params = {}

       if 'q' in params:
           query_params['q'] = params['q']

       if 'or_terms' in params:
           query_params['orTerms'] = params['or_terms']

       if 'exact_terms' in params:
           query_params['exactTerms'] = params['exact_terms']

       if 'exclude_terms' in params:
           query_params['excludeTerms'] = params['exclude_terms']

       if 'search_type' in params:
           query_params['searchType'] = params['search_type']

       else:
           query_params['searchType'] = self.search_type

       if 'site_search' in params:
           query_params['siteSearch'] = params['site_search']

       if 'site_search_filter' in params:
           query_params['siteSearchFilter'] = params['site_search_filter']

       if 'link_site' in params:
           query_params['linkSite'] = params['link_site']

       return query_params

   def generate_query_filter_params(self, params: dict)-> dict:
       """
       Generates the filter parameters for the API request.
       
       Parameters:
       - params (dict): The parameters for the API request.

       Returns:
       - dict: The filter parameters.
       """

       query_params = {}

       if 'hq' in params:
           query_params['hq'] = params['hq']

       if 'file_type' in params:
           query_params['fileType'] = params['file_type']

       if 'filter' in params:
           query_params['filter'] = params['filter']

       else:
           query_params['filter'] = self.filter

       if 'date_restrict' in params:
           query_params['dateRestrict'] = params['date_restrict']

       else:
           query_params['dateRestrict'] = self.date_restrict

       if 'high_range' in params:
           query_params['highRange'] = params['high_range']

       if 'low_range' in params:
           query_params['lowRange'] = params['low_range']

       if 'rights' in params:
           query_params['rights'] = params['rights']

       if 'safe' in params:
           query_params['safe'] = params['safe']

       else:
           query_params['safe'] = self.safe

       return query_params

   def generate_query_params_img(self, params)-> dict:
       """
       Generates the image parameters for the API request.
       Parameters:
       - params (dict): The parameters for the API request.
       Returns:
       - dict: The image parameters.
       """

       query_params = {}

       if 'img_color_type' in params:
           query_params['imgColorType'] = params['img_color_type']

       else:
           query_params['imgColorType'] = self.img_color_type

       if 'img_dominant_color' in params:
           query_params['imgDominantColor'] = params['img_dominant_color']

       else:
           query_params['imgDominantColor'] = self.img_dominant_color

       if 'img_size' in params:
           query_params['imgSize'] = params['img_size']

       else:
           query_params['imgSize'] = self.img_size

       if 'img_type' in params:
           query_params['imgType'] = params['img_type']

       else:
           query_params['imgType'] = self.img_type

       return query_params

   def generate_query_params_locations(self, params)-> dict:
       """
       Generates the location parameters for the API request.
       Parameters:
       - params (dict): The parameters for the API request.
       Returns:
       - dict: The location parameters.
       """

       query_params = {}

       if 'c2coff' in params:
           query_params['c2coff'] = params['c2coff']

       else:
           query_params['c2coff'] = self.c2coff

       if 'cr' in params:    
           query_params['cr'] = params['cr']

       else:
           query_params['cr'] = self.cr

       if 'gl' in params:
           query_params['gl'] = params['gl']

       else:
           query_params['gl'] = self.gl

       if 'hl' in params:
           query_params['hl'] = params['hl']

       else:
           query_params['hl'] = self.hl

       if 'lr' in params:
           query_params['lr'] = params['lr']

       else:
           query_params['lr'] = self.lr
           
       return query_params

   def generate_query_params_order_and_totals(self, params)-> dict:
       query_params = {}
      
       if 'num' in params:
           query_params['num'] = params['num']
       else:
           query_params['num'] = self.num
       if 'sort' in params:
           query_params['sort'] = params['sort']
       if 'start' in params:
           query_params['start'] = params['start']
       else:
           query_params['start'] = self.start
           
       return query_params