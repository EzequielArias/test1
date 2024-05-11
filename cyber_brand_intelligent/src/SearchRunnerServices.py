from connectors.github.GithubConnector import GithubConnector
import json

api_endpoints = [
    "/rate_limit",
    "/search/repositories" # q=tetris+language:assembly&sort=stars&order=desc 
]

class GithubConnectorController():
    
    def call_endpoint(endpoint):
        service = GithubConnector()
        #service.search('GET', api_endpoints[1] + "?q=tetris+language:javascript&sort=starts&order=desc&limit=2")
        service.search('GET', api_endpoints[0])
        print('Hola?')


class SearchRunServices():
    
    connector = GithubConnector()
    
    search_data : dict = {
        "query" : "pokemon",
        "exclude_query" : "",
        "extra_params" : {
            "language" : "Javascript",
            "created" : "2024-02-21"
        }
    }
    
    def run(self, id_search):
        
        search_data = self.search_data
        self.connector.apply_credentials({
            'Authorization' : "",
            'Accept' : "application/vnd.github+json",
            'X-GitHub-Api-Version' : "2022-11-28"
        })
        
        query = self.connector.transform_search_query_data(search_data['query'],
                                                      search_data['exclude_query'],
                                                      search_data['extra_params'])
        
        result_search = self.connector.search(query)
        print(result_search)

        if result_search.get('code') == 200:
            self.connector.normalize(result_search.get('data'))
        else:
            raise ValueError(result_search.get('error'))

main = SearchRunServices()

main.run("asd")