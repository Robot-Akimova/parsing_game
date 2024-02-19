import os
import shutil
import pandas as pd
import json
import urllib.request

# Чтение файла JSON
with open('final_data_utf8.json', 'r') as json_file:
    json_data = json.load(json_file)

# Чтение датафрейма
df_final = pd.read_excel('data_base_final.xlsx')

# Перебор строк датафрейма
for index, row in df_final.iterrows():
    product_name = row['Наименование товара']
    folder_path = f"./{product_name}"

    # Создание папки с названием товара
    os.makedirs(folder_path, exist_ok=True)

    # Поиск совпадений по ключу в файле JSON
    for item in json_data:
        if product_name in item:
            file_path = item[product_name]

            # Копирование файла в созданную папку
            if file_path.startswith('http'):
                # Если путь файла является URL-адресом
                file_name = file_path.split('/')[-1]
                file_path = os.path.join(folder_path, file_name)
                shutil.copyfileobj(urllib.request.urlopen(file_path), open(file_path, 'wb'))
            else:
                # Если путь файла является путем на локальном компьютере
                file_name = file_path.split('/')[-1]
                file_path = os.path.join(folder_path, file_name)
                shutil.copy2(file_path, folder_path)