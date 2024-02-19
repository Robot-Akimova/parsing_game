import codecs
import json

input_file = "final_data.json"
output_file = "final_data_utf8.json"

# Чтение файла JSON с текущей кодировкой
with codecs.open(input_file, 'r', encoding='unicode_escape') as f:
    data = json.load(f)

# Форматирование данных с добавлением символа перевода строки
formatted_data = [json.dumps(item, ensure_ascii=False) + '\n' for item in data]

# Запись файла JSON с исправленной кодировкой и новыми строками
with open(output_file, 'w', encoding='utf-8') as f:
    f.writelines(formatted_data)

