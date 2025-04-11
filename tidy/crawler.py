import mysql.connector
import requests
import time
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
import urllib

#testing Tidy API, we will use this string to test
req = {"BotID": "5", "BotIP": "212.102.59.80", "BotName": "Chris", "BotPub": "aEzkaYh2L3HspVAnigmlCO1qxlFUCgLPjcLdG4VLEotCus6ldIHAroXbMkS5aim3bamSdgslF9ATadEnJKmOm5DGaQbpJ0QIwpfXdXpNpY8J99zJiWsVXsXHFpG4wahv6yBkD1b9PEaY1rvhXMG5U4MjgyqzIl1idv3ykjk66alD9i7G5VYzZU0luAIjo7YcNguw2Ts1uyUe5EmPTWTAC6gUxujUkdQLsb8pDAYqfRwuMhVWhIGrp53wJtdtsxnCLPzUhydjASSjlgEr1sUyZZsGOlBpLN4BmnQmTuwnmmEACM6FvZEBDM1WrUGsf6JrZua84t1inCG36XDoeBJvxb7Ybmayr0p4je9o9C6ajw48novNHELBQnVl638Qo2ntGUcvqzaKaou3t5usIhYWFY7MJmUmtfdL0bMAnjZ8FGzMuC2Fo5FXD9Ca1CgVeK8nio4F63cv5PQT04jNgcqOWmu6J8FlvWU2i3oYEvLJh8v0EDkhm8JkLomVGQEEElWXhyAi8E8pqhuSRupRD3iUem52sTpyNq", "DataType": "URL", "SiteAddress": "https://gamespot.com", "LocalID": "215", "SiteIcon": "test", "Site_Notes": "test", "Title": "Gamespot", "Keywords": "Video Games", "Description": "Video game news", "PagePath": "https://gamespot.com"}
server = https://212.102.59.80:251

resp = requests.request(req, server)


db_config = {
    'host': 'localhost',
    'user': 'chris',
    'password': 'password',
    'database': 'TidySearch'
}

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.con = None
        self.cur = None

    def connect_to_db(self):
        self.con = mysql.connector.connect(**db_config)
        self.cur = self.con.cursor()

    def disconnect_from_db(self):
        if self.cur:
            self.cur.close()
        if self.con:
            self.con.close()
        
    def get_domain(self, url):
        parsed_url = urllib.parse.urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"
        
    def add_site(self, url):
        domain = self.get_domain(url)
        self.cur.execute("INSERT IGNORE INTO sites (url) VALUES (%s)", (domain,))
        self.con.commit()

        #get the site id, whether just inserted or already existing
        self.cur.execute("SELECT `index` FROM sites WHERE url = %s", (domain,))
        site_index = self.cur.fetchone()[0]
        return site_index

    def add_page(self, site_id, url):
        self.cur.execute("INSERT IGNORE INTO pages (site_id, path) VALUES (%s, %s)", (site_id, url))
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

    def send_data(SiteAddress, LocalID, SiteName, SiteIcon, Site_Notes, Title, Keywords, Description, PagePath):


    def crawl(self, url):
        domain = self.get_domain(url)
        html = self.download_url(url)
        site_id = self.add_site(url)
        self.add_page(site_id, url)
        self.send_date()
        for linked_url in self.get_linked_urls(url, html):
            if self.get_domain(url) == domain:
                self.add_url_to_visit(linked_url)
                self.add_page(site_id, linked_url)
            elif linked_url != domain:
                self.add_site(linked_url)
        time.sleep(1)

    def run(self):
        self.connect_to_db()
        try:
            while self.urls_to_visit:
                url = self.urls_to_visit.pop(0)
                logging.info(f'Crawling: {url}')
                
                try:
                    self.crawl(url)
                except requests.exceptions.RequestException as e:
                    logging.error(f'Failed to crawl {url}: {e}')
                except mysql.connector.Error as e:
                    logging.error(f'Database error while crawling {url}: {e}')
                except Exception as e:
                    logging.exception(f'Failed to crawl {url}: {e}')
                finally:
                    self.visited_urls.append(url)
        finally:
            self.disconnect_from_db()

if __name__ == '__main__':
    Crawler(urls=['https://www.gamespot.com/']).run()


