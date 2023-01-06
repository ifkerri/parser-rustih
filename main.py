from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests as r

ua = UserAgent()
url = 'https://rustih.ru/'
headers = {
    'Accept': '*/*',
    'User-Agent': ua.random
}

response = r.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
