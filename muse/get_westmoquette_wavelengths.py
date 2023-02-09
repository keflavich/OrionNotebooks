"""
This script will parse Mark Westmoquette's line list table into an astropy
Table and then write it out as an IPAC-formatted tabel
"""
import numpy as np
from astropy import units as u
import requests
from bs4 import BeautifulSoup
from astropy import table

result = requests.get('http://www.star.ucl.ac.uk/~msw/lines.html')
soup = BeautifulSoup(result.content)

def tryfloat(x):
    try:
        return float(x)
    except:
        try:
            return float(x.split()[0])
        except:
            return np.nan

tbls = soup.findAll('table')
rows = tbls[3].findAll('tr')
names = [r.findAll('td')[0].text.encode('ascii','ignore') for r in rows[1:] if len(r.findAll('td'))>=3]
air = [tryfloat(r.findAll('td')[1].text) for r in rows[1:] if len(r.findAll('td'))>=3]*u.AA
vac = [tryfloat(r.findAll('td')[2].text) for r in rows[1:] if len(r.findAll('td'))>=3]*u.AA

tbl = table.Table([table.Column(names, name='LineName'),
                   table.Column(air, name='AirWavelength', unit=u.AA),
                   table.Column(vac, name='VacuumWavelength', unit=u.AA),])

tbl.write('westmoquette_lines.ipac', format='ascii.ipac')
