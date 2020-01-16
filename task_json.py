"""Задание на закрепление знаний по модулю j son. Есть файл orders в формате JSON с
информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для
этого:
a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар
(item) , количество ( quantity) , цена ( price) , покупатель ( buyer) , дата ( date) . Функция
должна предусматривать запись данных в виде словаря в файл orders.json. При
записи данных указать величину отступа в 4 пробельных символа;
b. Проверить работу программы через вызов функции write_order_to_json() с передачей
в нее значений каждого параметра."""

import json
import random
import datetime

def generate_goods():
    now = datetime.datetime.now()
    dict_to_json = {
        "item": f'item{random.randint(1, 10)}',
        "quantity": random.randint(1, 10),
        "price": f'price{random.randint(1, 100)}',
        "buyer": f'buyer{random.randint(1, 10)}',
        "date": now.strftime("%Y-%m-%d")
    }
    return dict_to_json

# использование метода loads для чтения json-файла, как строки
# преобразуем json-строку в python-объект (словарь)
with open('orders.json') as f_n:
    obj = json.load(f_n)
    print(type(obj))

for section, commands in obj.items():
    print(section)
    commands.append(generate_goods())
    print(commands)
    print(obj)
    new_item = commands


with open('orders.json', 'w') as f_n:
    pass
    json.dump(obj, f_n, sort_keys=True, indent=4)
