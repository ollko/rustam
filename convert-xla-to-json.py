# coding=utf-8
import xlrd
from collections import OrderedDict
import json

import datetime
import pytz

wb = xlrd.open_workbook('list-of-products_2.xls')
sh = wb.sheet_by_index(1)

products_list = []
tz            = pytz.timezone('Europe/Moscow')
for rownum in range(1, sh.nrows):

	product = OrderedDict()
	row_values = sh.row_values(rownum)

	product['model']  = 'shop.product'
	product['pk']     = rownum
	product['fields'] = OrderedDict()
	product['fields']['category'] = row_values[19]

	product['fields']['name'] = row_values[13]
	product['fields']['slug'] = 'page-slug'
	product['fields']['image'] = ''
	product['fields']['article'] = "0000000000000"
	product['fields']['price'] = row_values[14]
	product['fields']['available'] = True
	# С учетом временной зоны по Москве
	product['fields']['created'] = str(datetime.datetime.now(tz))

	product['fields']['updated'] = str(datetime.datetime.now(tz))

	product['fields']['manufacture'] = row_values[15]
	product['fields']['packaging'] = row_values[16]
	product['fields']['typeprice'] = row_values[17]


	products_list.append(product)

j = json.dumps(products_list)

with open('shop.json', 'w') as f:
    f.write(j)