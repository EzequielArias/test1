import requests
from bs4 import BeautifulSoup
import re 

headers = { 
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Google Chrome 123.0.6312.105 Safari/537.36'
}
 
from main.links import google_links

white_list = [] # append with originals url's from flow and personal

suspect_list = [] # this mean the website is not a original url or black list(pirate site)
cannot_scrape = []

black_list = []
link_historial = {}
root_url = ""
current_loop = 0

def analize_paths(anchor_href):

    if anchor_href.startswith("http://") or anchor_href.startswith("https://"):
        return True # Quiere decir que es una ruta absoluta

    return False # Quiere decir que es una ruta relativa

def analize_iframes(url):
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        regEx = r'function\s+getParameterByName\s*\([^)]*\)\s*{[^}]*}'

        exists = re.search(regEx, response.text)

        if exists:
            print("\033[31m",'Es un caso positivo funcion maliciosa encontrada =>', "\033[31m", url)
            black_list.append(url)
            return True

        iframes_results = soup.find_all('iframe')

        for iframe in iframes_results:
            src = iframe.get('src')

            if r'cvattv' in src:
                print('Es un caso positivo un iframe tiene cvattv ', + src)

            if analize_paths(src):
                iframe_html = requests.get(src, headers=headers)
                
                isPirate = re.search(regEx, iframe_html.text)
                if isPirate:
                     return True

# Return a list of sub-domains
def analize_anchors(anchor_results):
    
    sub_domains = []

    for anchor in anchor_results:

        href = anchor.get('href')

        if r'cvattv' in href:
            print('Dominio malicioso')
            black_list.append(href)
            sub_domains = []
            break

        if 'index.html' in href:
            continue
 
        if '#' in href or "/" == href:
            print('Es una redireccion o es la ruta home')
            continue
        
        if href in link_historial[root_url]['sub_dominios']:
            continue
        else:
            sub_domains.append(href) 

    return sub_domains

def analize_websites(self, url, sub_dom=False):
    try:
        global root_url
        if url in link_historial:
            return

        if not sub_dom:            
            root_url = url
            print("")
            print("This is the last URL " + url)
            print(" ")
            link_historial[url] = {"sub_dominios" :  []}
        else:
            print('En este caso debe agregarse a un historial de cola en el caso de que existan subdominios de una url por analizar.')

        response = requests.get(root_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            print(" ")
            print(url)
            print(" ")

            anchor_results = soup.find_all('a')

            sub_domains = analize_anchors(anchor_results)

            for link in sub_domains:
                isAbsolute = analize_paths(link)

                if isAbsolute:
                    if analize_iframes(link):
                        black_list.append(link)
                        break
                    link_historial[root_url]['sub_dominios'].append(link)
                    analize_websites(link)
                    continue
                
                if analize_iframes(root_url + link):
                    black_list.append(root_url)
                    break

                aux2 = any(re.search(r'{0}'.format(link), sub_domain) for sub_domain in link_historial[root_url]["sub_dominios"])
                if aux2:
                    print('cancelando sub funcion')
                    return 

                link_historial[root_url]['sub_dominios'].append(link)
                analize_websites(root_url + link, True)
        else:
            cannot_scrape.append(url)
    except Exception as e:
        print("¡Error inesperado:", e)



analize_websites('https://tv-libre.com')

#for websites in google_links:
#    analize_websites(websites)

print("This is my BlackList")
print(black_list)
print("")
print(cannot_scrape)


"""
   1 - IFRAME + 30%
   De un listado de palabras si encontre coincidencias sigo scrapeando, en el caso de que 
   no encuentre coincidencias en el link dado cortar ejecucion del script porque es probable que no
   sea una pagina pirata

   solo scrapear las url propias del dominio actual las otras que encuentre dejarlas en un historial

   tener un limite de recursividad para cada URL dada 

   Si una url tiene redireccion por ejemplo a /facebook/marketplace colocar como sospechoso porque puede ser sospechoso

   Utilizar pydanti

   crear con expresiones regular queries para buscar funciones o enlaces parametizables para poder.
"""

"""
Si estoy analizando una URL busco subdominios y en el caso que encuentra una URL absoluta a otra pagina agregarla a una queue
entonces al terminar con el analisis de una pagina o el limite maximo de recursividad tengo que analizar la siguiente URL en la cola
para poder escribir e reiniciar el limitador de recursividad a 0

POSIBILITY : Se podria agregar un filtro a los subdominios. EJ : /espn/barcelona es un si /pepa/pig es un caso a no analizar

PROBLEMAS EN TENER EN CUENTA CON LA LOGICA PENSADA:
    - El limitador de recursividad tiene que crearse de una manera que solo analice las rutas relativas y no rutas absolutas
    - El limitador puede ser que evite analizar dominios / subdominios importantes que contengan datos relevantes.

"""
