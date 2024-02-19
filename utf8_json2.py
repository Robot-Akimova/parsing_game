import codecs
import json

input_file = "final_data.json"
output_file = "final_data_utf8.json"

# Чтение файла JSON с неправильной кодировкой
with codecs.open(input_file, 'r', encoding='unicode_escape') as f:
    data = f.read()

# Запись файла JSON с исправленной кодировкой
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(data)