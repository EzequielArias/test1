import requests
from bs4 import BeautifulSoup
import re 
from main.links import links

headers = { 
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Google Chrome 123.0.6312.105 Safari/537.36'
}

"""
jeinzmacias.net
livetx.sx
decode base 64 tienen doble decode
"""

links = [
    'https://television.libre.futbol', # funka
    'https://tv-libre.com', # funka
    'https://tele-libre.com', # funka
    'https://librefutboltv.net', # No funka tiene archivos .php y ofuscados
    'https://futbollibrehd.net',
    'https://librefutbol.su',# no funka
    'https://futbollibre.nu',
    'https://tvabierta.weebly.com',
    'https://futbollibre.pe',
    'https://television-libre.online'
] 

white_list = ["https://www.personal.com.ar/", ""] # append with originals url's from flow and personal

suspect_list = [] # this mean the website is not a original url or black list(pirate site)

black_list = []
link_historial = {}
root_url = ""

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

def analize_websites(url, sub_dom=False):

    try:
        global root_url
        if url in link_historial:
            return

        if not sub_dom:            
            root_url = url
            link_historial[url] = {"sub_dominios" :  []}


        response = requests.get(root_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            anchor_results = soup.find_all('a')

            sub_domains = analize_anchors(anchor_results)
            
            for link in sub_domains:
                print(link)
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
            if  len(black_list) == 0:
                print('Esta URL es sospechosa revisar : ', url)
    except Exception as e:
        print("¡Error inesperado:", e)

   
    print(black_list)
    print("#####################################################")
    print(link_historial)

analize_websites('https://futbollibre.nu/tv2/en-vivo/espn-3/')
    
"""
    buscar href con findall entonces si el href coincide guardar con el link caso contrario seguir buscando hasta que ya no haya mas a con href 
    que la opcion 

    armar listas.
    blacklist,
    whitelist,
    casos a investigar. aquellos que no coincidan con la regex
"""

"""
    hacer un modelo de aprendizaje anti pirateria.
    space.io


    recoleccion de datos
    analisis de datos
    calificacion de datos => 
"""
