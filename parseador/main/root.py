import requests
from bs4 import BeautifulSoup
import re 
from urllib.parse import urlparse
from typing import List, Optional
from urllib.parse import urlparse, urljoin
from collections import deque

class Scrapper():

    white_list = []
    suspect_list = []
    black_list = []
    root_url = ""
    current_loop = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    link_historial = []
    not_scrappable =  [
        "https://www.facebook.com",  # Facebook
        "https://www.instagram.com",  # Instagram
        "https://www.telegram.org",  # Telegram
        "https://www.twitter.com",  # Twitter
        "https://www.linkedin.com",  # LinkedIn
        "https://www.snapchat.com",  # Snapchat
        "https://www.tiktok.com",  # TikTok
        "https://www.pinterest.com",  # Pinterest
        "https://www.reddit.com"  # Reddit
    ]
    wordlist = []

    def __init__(self, word_list : Optional[List[str]] = None):
       if not word_list:
            self.wordlist = ["gratuito", "sin costo", "libre", "a costo cero", "de balde", "sin cobrar", "sin pagar", "costo cero", "gratuitamente"]
       self.visited_pages= set() 
    
    def is_allowed_by_robots(url):
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        robots_response = requests.get(robots_url)
        return not robots_response.text.startswith("User-agent: *") or "Disallow: /" not in robots_response.text

    # Function to recursively crawl URLs
    def crawl(self, current_url, depth, visited_urls, max_depth=5):
        if depth <= max_depth and current_url not in visited_urls and self.is_allowed_by_robots(current_url):
            # Fetch the webpage content
            # Parse the webpage using Beautiful Soup
            soup = self.extract_html(current_url)    
            visited_urls.add(current_url)
            print(f"Crawled: {current_url} (Depth: {depth})")

            # Find all 'a' (anchor) tags that contain links
            links = self.scrap_html(soup)

            # Visit each link found on the page
            for link in links:
                next_url = link['href']
                if next_url.startswith('http') and next_url not in visited_urls:
                    self.crawl(next_url, depth + 1, visited_urls)

    def scrap_html(self, soup : BeautifulSoup):
        iframes = self.analize_iframes()
        anchors = self.analize_anchors(soup.find_all('a', href=True))
        pass

    # Return True if a have to scrape the website
    def is_a_positive_case(self, url):

        parsed_url = urlparse(url)

        if parsed_url.netloc in self.not_scrappable:
            
            if '/marketplace' in parsed_url.path:
                self.suspect_list.append(url)
                return False

            for word in self.wordlist:
                pass

    def extract_html(self, url):
        response = requests.get(url,headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup

    def analize_paths(self, anchor_href):
        return anchor_href.startswith("http://") or anchor_href.startswith("https://")

    def analize_iframes(self, current_url, depth, max_depth=5):

        if depth <= max_depth and current_url not in self.visited_urls and self.is_allowed_by_robots(current_url):

            iframe_soup = self.extract_html(current_url)

            regEx = r'function\s+getParameterByName\s*\([^)]*\)\s*{[^}]*}'
            exists = re.search(regEx, iframe_soup)

            if exists:
                print("\033[31m",'Malicious function found =>', "\033[31m", current_url)
                self.black_list.append(current_url)
                return True

            iframes = iframe_soup.find_all('iframe')
            for iframe in iframes:
                src = iframe.get('src')
                if 'cvattv' in src:
                    print('Iframe contains cvattv:', src)

                if self.analize_paths(src):
                    iframe_html = requests.get(src, headers=self.headers)
                    if re.search(regEx, iframe_html.text):
                        return True
            return False

    def analize_anchors(self, anchor_results):
        sub_domains = []
        for anchor in anchor_results:
            href = anchor.get('href')
            if 'cvattv' in href:
                print('Malicious domain detected')
                self.black_list.append(href)
                sub_domains = []
                break

            if 'index.html' in href or '#' in href or href == "/":
                continue

            if href in self.link_historial[self.root_url]['sub_domains']:
                continue

            sub_domains.append(href)
        return sub_domains

    def analize_websites(self, url, sub_dom=False):
       
        if url in self.link_historial:
            print('Esta url ya fue analizada')
            return
            
        if self.is_a_positive_case(""):
            pass

        #if not sub_dom:
        #    self.root_url = url
        #    self.link_historial[url] = {"sub_domains": []}

        soup = self.extract_html(url)

        if soup:
            anchor_results = soup.find_all('a')
            sub_domains = self.analize_anchors(anchor_results)

            for link in sub_domains:
                isAbsolute = self.analize_paths(link)

                if isAbsolute:
                    if self.analize_iframes(link):
                        self.black_list.append(link)
                        break
                    self.link_historial[self.root_url]['sub_domains'].append(link)
                    self.analize_websites(link)
                    continue

                if self.analize_iframes(self.root_url + link):
                    self.black_list.append(self.root_url)
                    break

                aux2 = any(re.search(r'{0}'.format(link), sub_domain) for sub_domain in self.link_historial[self.root_url]["sub_domains"])
                if aux2:
                    return

                self.link_historial[self.root_url]['sub_domains'].append(link)
                self.analize_websites(self.root_url + link, True)
 
main = Scrapper(["E","E"])


#main.analize_websites("https://gestion.pe/mix/sports/fox-sports-en-vivo-como-ver-barcelona-vs-psg-por-tv-y-online-desde-argentina-champions-league-2024-nnda-nnrt-noticia/")
#print(main.suspect_list)

"""
 Anotarme el paso a paso para poder tener acceso tanto en reddit como en bing search
"""