# Импорты
import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from time import sleep 
import os
import json
import pandas as pd
import openpyxl

df = pd.DataFrame(columns = ['Название игры', 'Цена игры', 'Дата выхода и язык', 'описание', 'Платформа'] )


headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; ru-RU; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)'
}

list_card_url = []
list_card_count = 0

# Добавляем url адрес сайта для парсинга
url = 'https://404game.ru/genre'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml') 
data = soup.find_all('div', class_ = 's-in' )

# Получаем ссылки карточек 1ой страницы
for ferst_page in data:
    # sleep(3)
    card_url = ferst_page.find('a', class_='s-img fx-col fx-middle fx-center').get('href')
    list_card_url.append(card_url)
    list_card_count = list_card_count + 1


# Счётчик обработанных игр
count_game = 0 
# Счётчик обработанных игр с собранной информацией
final_count_game = 0
final_count_game_mistake = 0

for count in range(2,27):
    # sleep(3)
    url = f'https://404game.ru/genre/page/{count}/'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml') 
    data = soup.find_all('div', class_ = 's-in' )

# Реализуем перебор с переходами по ссылкам
    for i in data:
        card_url = i.find('a', class_='s-img fx-col fx-middle fx-center').get('href')
        list_card_url.append(card_url)
        list_card_count = list_card_count + 1
print(f'Количество игр в списке: {list_card_count}')
img_final_dict = {} 
for card in list_card_url:
    try:
        # sleep(3)
        firefox_options = Options()
        firefox_options.add_argument("--headless") 
        driver = webdriver.Firefox(options=firefox_options)
        # Очистка куки
        driver.delete_all_cookies()
        # Установка заголовков браузера
        driver.header_overrides = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/88.0'
        }
        driver.get(card)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        name_game = soup.find('h1', class_ = 'ftitle').text.replace('Аренда для Ps4 и Ps5', '').strip()#str.strip() добавлен
        price_game = soup.find('div', class_ = 's-price').text
        date_and_language = soup.find('ul', class_ = 'finfo').text
        description = soup.find('div', class_ = 'ftext full-text clearfix tabs-b visible').text
        platform = soup.find('div', class_ = 'fdost').text
        img_row_list = soup.find_all('img', class_='fotorama__img')

        # Создание словаря с данными для новой строки
        data = {
            'Название игры': name_game,
            'Цена игры': price_game,
            'Дата выхода и язык': date_and_language,
            'Описание': description,
            'Платформа': platform
        }
        # , index=[0] - соответствие одной строке фрэйма
        df2 = pd.DataFrame(data, index=[0])
        # Добавление новой строки в DataFrame
        # append удалён из пандас?
        df = pd.concat([df, df2], ignore_index=True)

        
        img_final_list = []
        # Пути файлов
        catalog_img_row = 'E:\BD_Site\site'
        catalog_img_final = 'E:\BD_Site\list_game'



        # Открытие JSON-файла для записи
    
        for img in img_row_list:
            img_link = img.get('src')
            if img_link: 
                if img_link in img_final_list:
                    continue
                else:
                    img_final_dict.update({f'{name_game}' : f'{img_link}' })
                    img_final_list.append(img_link)
                    # Открытие JSON-файла для записи
                    with open('data.json', 'a') as file:
                        json_apdate = {name_game : img_link}
                        json.dump(json_apdate, file)
                        file.write('\n')

                    print({f'{name_game} : {img_link}'})
                
                    
                        
            else:
                continue 
        count_game = count_game + 1
        driver.quit()
        final_count_game = final_count_game + 1
    except:
        final_count_game_mistake = final_count_game_mistake + 1
        with open('url_errors.json', 'a') as file:
            json_apdate = {'URL игры с ошибкой' : card}
            json.dump(json_apdate, file)
            file.write('\n')
        
        continue
    
    
    
    
    
    
    print(f'Цена {price_game}')
    print(f'{date_and_language}')
    print(f'{description}')
    print('------------------------------------')
    print(f'Количество обработанных игр: {final_count_game}')
    print(f'Количество возникших ошибок: {final_count_game_mistake}')
    print('____________________________________')

# Запись DataFrame в файл Excel
# Файл из строчки ниже, нужно создавать заранее. Если файла не существует
# то выйдет исключение
df.to_excel(f'D:\code\Parsing_curse_bs4_training\data_base_final.xlsx', index=False)
print(f'Количество записанных игр : {final_count_game}')
    