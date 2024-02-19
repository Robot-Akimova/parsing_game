# Код исправляет ошибки с запятыми в полученном при парсинге 
# json файле
import json

input_file = "data.json"
output_file = "final_data.json"

# Чтение файла JSON
with open(input_file, 'r') as f:
    data = f.readlines()

# Объединение строк с использованием запятых
fixed_data = '[' + ','.join(data) + ']'

# Запись исправленного файла JSON
with open(output_file, 'w') as f:
    f.write(fixed_data)