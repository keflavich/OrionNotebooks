import numpy as np
import requests
from bs4 import BeautifulSoup
from astropy.table import Table, Column
import re
page = requests.get('http://iopscience.iop.org/0067-0049/129/1/229/fulltext/51083.tb1.html')
b = BeautifulSoup(page.content, 'html5')

b.findAll('table')[1].findAll('tr')[0].findAll('td')
header = [x.text for x  in b.findAll('table')[1].findAll('tr')[0].findAll('td')]

rows = [[x.text.replace('...','') for x in row.findAll('td')] for row in b.findAll('table')[1].findAll('tr')[1:]]

for table in b.findAll('table')[2:]:
    rows += [[x.text.replace('...','') for x in row.findAll('td')] for row in table.findAll('tr')[1:]]

import unicodedata
def clean(x):
    # http://stackoverflow.com/a/2701901/814354
    y = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore')
    y = re.compile('\s').sub('_', y)
    y = re.compile('[()/?-]').sub('', y)
    return y


rowsarr = np.array(rows)
rowsarr[rowsarr == ' '] = '-999'
rowsarr[rowsarr == ''] = '-999'

names = [clean(x) for x in header]

t = Table(data=rowsarr,
          names=names,
          dtype=['float']*2 + ['str']*2 + ['float']*5 + ['str'])

t.write('b00_lines.ipac', format='ascii.ipac')
