import xlrd
from collections import OrderedDict
import json

import datetime
import pytz

wb = xlrd.open_workbook('list-of-products.xls')
sh = wb.sheet_by_index(1)

products_list = []
tz            = pytz.timezone('Europe/Moscow')
for rownum in range(1, sh.nrows):

	product = OrderedDict()
	row_values = sh.row_values(rownum)

	product['model']  = 'shop.product'
	product['pk']     = rownum
	product['fields'] = OrderedDict()
	product['fields']['category'] = row_values[14]

	product['fields']['name'] = row_values[0]
	product['fields']['slug'] = 'page-slug'
	product['fields']['image'] = ''
	product['fields']['article'] = "0000000000000"
	product['fields']['price'] = row_values[12]
	product['fields']['available'] = True
	# С учетом временной зоны по Москве
	product['fields']['created'] = str(datetime.datetime.now(tz))

	product['fields']['updated'] = str(datetime.datetime.now(tz))



	products_list.append(product)

j = json.dumps(products_list)

with open('shop.json', 'w') as f:
    f.write(j)