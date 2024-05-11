from connectors.github import GithubConnector

"""
 search_data : dict = {
        "query" : "pokemon",
        "exclude_query" : "",
        "extra_params" : {
            "language" : "Javascript",
            "created" : "2024-02-21"
        }
    }
"""

class TestGithubConnector():

    test_class = GithubConnector()

    def search_parameters(self):  # Asegúrate de incluir `self` como primer argumento
        search_query = {
            "query" : "pokemon",
            "exclude_query" : "",
            "extra_params" : {
                "language" : "Javascript",
                "created" : "2024-02-21"
            }
        }

        query = self.test_class.transform_search_query_data(search_query['query'],
                                                      search_query['exclude_query'],
                                                      search_query['extra_params'])
        result_search = self.test_class.search(query)

        assert result_search.get('code') == 200, "La respuesta de error fue incorrecta"
        assert 'items' in result_search.get('data', {}), "El JSON no contiene la propiedad 'items'"


    def no_params_search(self):

        failed_call = self.test_class.search(not None)

        

    def normalize_results():
        pass

