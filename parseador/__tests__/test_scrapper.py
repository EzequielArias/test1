import sys
sys.path.append('..')
print(sys.path)

from main import root
from urllib.parse import urlparse

class TestScrapper:

    instance = root.Scrapper()
    wordlist = ["gratuito", "sin costo", "libre", "a costo cero", "de balde", "sin cobrar", "sin pagar", "costo cero", "gratuitamente"]

    # Should return a suspect list    
    def test_url_validator(self):

        result = self.instance.validate_url("https://www.facebook.com/marketplace/?ref=app_tab")

        assert isinstance(result, list), "El resultado debe ser una lista de urls"

        assert all(isinstance(item, str) for item in result), "Todos los elementos deben ser strings"
    
    def test_is_a_positive_case(self):

        result = self.instance.validate_url("https://tv-libre.com'", 'futbol')

        assert result == True, 'El url pasado por parametros debe ser un caso positivo'