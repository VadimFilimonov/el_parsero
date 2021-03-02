#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import re
import os
import ssl

# Для того чтобы подключить класс формирования ссылки
import sys
# переходим в корень
sys.path.insert(0, '../')

ssl._create_default_https_context = ssl._create_unverified_context

def delrubbish(x):
	import re
	x = re.sub("^\s+|\n|\r|\t|\s*$|\t*$;", '', x)
	x = re.sub('"', "'", x)
	return x

def toBlue(x):
	x = '\033[96m' + x + '\033[0m'
	return x

def rowsnumber(filename):
	file = open(filename)
	content = file.read()
	content_list = content.split('\n')
	return len(content_list)

def buildCell(x):
	x = f'"{str(x)}"'
	return x

def buildRow(*cells):
	# Создаем пустую строку
	row = ''
	# Проходимся по всем ячейкам
	for cell in cells:
		# Каждой ячейке справа добавляем точку с запятой
		row += buildCell(cell) + ';'
	# У последнего столбца добавляем перенос строки
	row += '\n'
	return row

# Переменные
site = 'http://clipsite.ru'
# Переменная, куда будут попадать значения csv
str_csv = ""

# Файлы
# Файл, в котором хранятся ссылки на страницы с категориями
list_file = open('./build/list.txt', 'r')
# Список товаров
if not os.path.exists('./build'):
	os.mkdir('./build')
open('./build/result.csv', 'w').close()
result = open("./build/result.csv", "a")
# Количество строк в файле со ссылками
filelength = rowsnumber('./build/list.txt')
# Обнуляем счетчик
counter = 0
# Проходимся по всем ссылкам
for line in list_file.readlines():
	# Библиотека beautiful soup конвертит ссылки в нужный нам формат
	html_doc = urlopen(line).read()
	soup = BeautifulSoup(html_doc, "html.parser")

	# Заголовок страницы
	title = soup.find('h1').text
	title = delrubbish(title)

	# Текст
	text = soup.find('div', 'node__content').find('div', 'field--name-body')

	# Изображение
	image = soup.find('div', 'c-bg-block').get('style')
	image = delrubbish(image)

	# Поднимаем счетчик на 1
	counter += 1
	# Выводим в консоль
	print(toBlue(str(counter) + '/' + str(filelength) + ': ') + title)
	# Добавляем столбцы в csv
	str_csv += buildRow(str(counter), title, text, image)

# Первая строка таблицы - заголовки столбцов
str_csv_header = buildRow('id', 'Заголовок', 'Текст', 'Изображение')
result.write(str_csv_header)
# Записываем конечный csv файл с категориями
result.write(str_csv)
list_file.close()
result.close()
