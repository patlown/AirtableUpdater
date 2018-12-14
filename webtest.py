import webbrowser
import requests
import json
import urllib3
from bs4 import BeautifulSoup

link = 'https://airtable.com/account'
webbrowser.open(link)
html = requests.get(link).text
soup = BeautifulSoup(html, "lxml")
# data = json.loads(soup.findall('script'))
all_scripts = soup.find_all('script',)
print(all_scripts[0])
    