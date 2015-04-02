lines = {'OI6300': 6302.046,
         'SIII6313': 6313.8,
         'OI6363': 6365.536,
         'NII6548': 6549.85,
         'HAlpha': 6564.61,
         'HBeta': 4862.69,
         'NII6584': 6585.28,
         'HeI6678': 6679.99556,
         'SII6716': 6718.29,
         'SII6731': 6732.67,
         'pa20': 8394.71,
         'pa19': 8415.63,
         'pa18': 8440.27,
         'pa17': 8469.59,
         'pa16': 8504.83,
         'pa15': 8547.73,
         'pa14': 8600.75,
         'pa13': 8667.40,
         'pa12': 8752.86,
         'pa11': 8865.32,
         'pa10': 9017.8 ,
         'pa9' : 9232.2 ,
         'HeI7067': 7067.138,
         'HeI7283': 7283.355,
         'ArIII7135': 7137.8,
         'ArIII7751': 7753.2,
         'SIII9071':9071.1,
         'NeII5756':5756.24,
         'HeI5877':5877.3,
         'OIII5008': 5008.24,
         'OII4960': 4960.3,
         #'FeII8617': 8717,
}

from astropy.table import Table
import numpy as np
t = Table.read('b00_lines.ipac', format='ascii.ipac')
# select bright lines >4600 ang
mask = (t['I6678_obs_7'] > 0.1) & (t['ID_Wavelength_A_2'] > 4600)
names = np.array(["{0}{1}".format(id, wl).replace(" ","") for id,wl in
         zip(t['ID_3'],t['ID_Wavelength_A_2'])])
b00lines_air = dict(zip(names[mask], t['ID_Wavelength_A_2'][mask],))
b00lines_measured = dict(zip(names[mask], t['Rest_Wavelength_A_1'][mask],))

feii_mask = np.array([nm in ('Fe II','[Fe II]') for nm in t['ID_3']]) & (t['I6678_obs_7'] > 0.01) & (t['ID_Wavelength_A_2'] > 4600)
b00feiilines_air = dict(zip(names[feii_mask], t['ID_Wavelength_A_2'][feii_mask],))
b00feiilines_measured = dict(zip(names[feii_mask], t['Rest_Wavelength_A_1'][feii_mask],))

fei_mask = np.array([nm in ('Fe I','Fe I]') for nm in t['ID_3']]) & (t['ID_Wavelength_A_2'] > 4600)
b00feilines_air = dict(zip(names[fei_mask], t['ID_Wavelength_A_2'][fei_mask],))
b00feilines_measured = dict(zip(names[fei_mask], t['Rest_Wavelength_A_1'][fei_mask],))
