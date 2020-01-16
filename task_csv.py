""" 1. Задание на закрепление знаний по модулю CSV.
Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt
и формирующий новый «отчетный» файл в формате CSV. Для этого:

    Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
    их открытие и считывание данных. В этой функции из считанных данных необходимо
    с помощью регулярных выражений извлечь значения параметров
    «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
    Значения каждого параметра поместить в соответствующий список. Должно получиться четыре списка —
    например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции
    создать главный список для хранения данных отчета — например, main_data —
    и поместить в него названия столбцов отчета в виде списка:
    «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
    Значения для этих столбцов также оформить в виде списка и поместить
    в файл main_data (также для каждого файла);
    Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
    В этой функции реализовать получение данных через вызов функции get_data(),
    а также сохранение подготовленных данных в соответствующий CSV-файл;
    Проверить работу программы через вызов функции write_to_csv(). """

import csv

# Простое чтение из файла kp_data.csv
# Получаем итератор объекта
import os
import re

def get_data():


    main_data = []
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    num = len(os.listdir('./info'))
    columns = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(columns)
    for i in range(num):
        filename = f'./info/info_{i+1}.txt'
        with open(filename, 'r') as f_n:
            resume = []
            for line in f_n:
                #print(line)

                if re.match(r'Изготовитель ОС', line):
                    os_prod_list.append(line.split(':')[1].strip())
                    resume.append(os_prod_list[i])

                elif re.match(r'Название ОС', line):
                    #prod = re.findall('[^Название ОС:]', line)
                    #print(prod)
                    os_name_list.append(line.split(':')[1].strip())
                    resume.append(os_name_list[i])

                elif re.match(r'Код продукта', line):
                    os_code_list.append(line.split(':')[1].strip())
                    resume.append(os_code_list[i - 1])

                elif re.match(r'Тип системы', line):
                    os_type_list.append(line.split(':')[1].strip())
                    resume.append(os_type_list[i - 1])

            main_data.append(resume)

    return main_data

def write_to_csv(filename):
    with open('filename', 'w', encoding='UTF-8') as f_n:
        data = get_data()
        F_N_WRITER = csv.writer(f_n, quoting=csv.QUOTE_NONNUMERIC)
        F_N_WRITER.writerows(data)

write_to_csv('main_data.csv')