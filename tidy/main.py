import http
import requests
import time
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
import urllib

con = sqlite3.connect('crawler5.db')
cur = con.cursor()

#ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    
cur.execute("""
    CREATE TABLE IF NOT EXISTS sites (
    idx INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    RemoteID INTEGER NOT NULL DEFAULT 0,
    local INTEGER NOT NULL DEFAULT 0,
    BotID INTEGER NOT NULL DEFAULT 0,
    send INTEGER NOT NULL DEFAULT 0,
    name varchar(500) DEFAULT NULL,
    datetime datetime DEFAULT NULL,
    url varchar(100) UNIQUE NOT NULL,
    favicon longblob DEFAULT NULL,
    Site_Notes varchar(500) DEFAULT NULL
)""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS pages (
        idx INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER DEFAULT NULL,
        date datetime DEFAULT CURRENT_TIMESTAMP,
        title TEXT DEFAULT NULL,
        keywords TEXT DEFAULT NULL,
        description TEXT DEFAULT NULL,
        path TEXT UNIQUE NOT NULL,
        FOREIGN KEY (site_id) REFERENCES sites(idx)
    );
""")
    
con.commit()

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.con = sqlite3.connect('crawler5.db')
        self.cur = self.con.cursor()
        
    def get_domain(self, url):
        parsed_url = urllib.parse.urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"
        
    def add_site(self, url):
        domain = self.get_domain(url)
        self.cur.execute("INSERT OR IGNORE INTO sites (url) VALUES (?)", (domain,))
        self.con.commit()
        return self.cur.lastrowid

    def add_page(self, site_id, url):
        self.cur.execute("INSERT OR IGNORE INTO pages (site_id, path) VALUES (?, ?)", (site_id, url))
        self.con.commit()

    def download_url(self, url):
        headers = {
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
        }
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path:
                #print('path exists')
                if path.startswith('/'):
                    path = urljoin(url, path)
                elif path.startswith('http'):
                    path = path
                else:
                    path = urljoin(url, path)
                yield path
                
    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        domain = self.get_domain(url)
        html = self.download_url(url)
        site_id = self.add_site(url)
        self.add_page(site_id, url)
        for linked_url in self.get_linked_urls(url, html):
            if self.get_domain(url) == domain:
                self.add_url_to_visit(linked_url)
                self.add_page(site_id, linked_url)
        time.sleep(1)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':
    Crawler(urls=['https://www.gamespot.com/']).run()
