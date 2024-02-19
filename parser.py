import csv
import json
import os.path

import requests
from bs4 import BeautifulSoup

url = 'https://olnisa.ru/manufacturers/schneider-electric/'

headers = {
    'Accept': '*/*',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

projects_data_list = []
iteration_count = 500
print(f'Всего итераций: #{iteration_count}')



for item in range(1, 11):
    if item == 1:
        req = requests.get(url, headers=headers)
    elif item > 1:
        req = requests.get(url + f'page-{item}/', headers=headers)

    folder_name = f'data/data_{item}'

    if os.path.exists(folder_name):
        print('Папка уже существует')
    else:
        os.mkdir(folder_name)

    with open(f'{folder_name}/index_{item}.html', 'w', encoding='utf-8') as file:
        file.write(req.text)

    with open(f'{folder_name}/index_{item}.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    test = soup.find('div', class_='title').find_all('div')

    head1 = test[2].text.strip()
    head2 = test[3].text.strip()
    head3 = test[4].text.strip()

    with open(f'{folder_name}/{item}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (head1,
             head2,
             head3)
        )

    articles = soup.find_all('div', itemprop='model')
    project_urls = []
    for link in articles:
        project_url = "https://olnisa.ru/"+link.find('a').get('href')
        project_urls.append(project_url)


    for project_url in project_urls:
        req = requests.get(project_url, headers)
        project_name = project_url.split('/')[-2]

        with open(f'{folder_name}/{project_name}.html', 'w', encoding='utf-8') as file:
            file.write(req.text)
        with open(f'{folder_name}/{project_name}.html', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')

        try:
            project_data = soup.find('div', itemprop='description').find('p').text
        except AttributeError:
            project_data = "No project description"

        try:
            brand = soup.find('p', itemprop='brand').text
        except AttributeError:
            brand = 'No brand'

        projects_data_list.append(
            {
                'Артикул': project_name,
                'Бренд': brand,
                'Описание': project_data
            }
        )

        iteration_count -= 1
        print(f'Страница #{item} завершена, осталось итераций: {iteration_count}')
        if iteration_count == 0:
            print("Сбор данных завершен")





with open("data/projects_data.json", 'a', encoding='utf-8') as file:
    json.dump(projects_data_list, file, indent=4, ensure_ascii=False)



