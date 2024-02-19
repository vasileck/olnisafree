import csv

import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': '*/*',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

url = "https://olnisa.ru/manufacturers/schneider-electric/"

req = requests.get(url, headers=headers)

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(req.text)

with open('index.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

test = soup.find('div', class_='title').find_all('div')

head1 = test[2].text.strip()
head2 = test[3].text.strip()
head3 = test[4].text.strip()
print(head3)
