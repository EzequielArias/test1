import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from collections import deque

class WebCrawler:
    def __init__(self):
        self.visited_pages = set()

    # Function to check robots.txt for allowed URLs
    def is_allowed_by_robots(url):
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        robots_response = requests.get(robots_url)
        return not robots_response.text.startswith("User-agent: *") or "Disallow: /" not in robots_response.text

    # Function to recursively crawl URLs
    def crawl(self, current_url, depth, visited_urls, max_depth=5):
        if depth <= max_depth and current_url not in visited_urls and self.is_allowed_by_robots(current_url):
            # Fetch the webpage content
            response = requests.get(current_url)
            if response.status_code == 200:
                # Parse the webpage using Beautiful Soup
                soup = BeautifulSoup(response.content, 'html.parser')
                visited_urls.add(current_url)
                print(f"Crawled: {current_url} (Depth: {depth})")

                # Find all 'a' (anchor) tags that contain links
                links = soup.find_all('a', href=True)

                # Visit each link found on the page
                for link in links:
                    next_url = link['href']
                    if next_url.startswith('http') and next_url not in visited_urls:
                        self.crawl(next_url, depth + 1, visited_urls)

    def extract_data(self, url, soup):
        title = soup.title.string if soup.title else "No Title Found"
        print(f"Title of {url}: {title}")

    def normalize_url(self, current_url, link):
        parsed_link = urlparse(link)
        if parsed_link.scheme and parsed_link.netloc:  # Absolute URL
            return link
        elif parsed_link.path.startswith(('#', 'mailto:', 'tel:')):  # Ignore non-http links
            return None
        else:  # Relative URL
            base_url = urlparse(current_url)
            return urljoin(current_url, link)

