from astropy.io import fits
from astropy import units as u
import numpy as np
import spectral_cube
import pyspeckit
from spectral_cube.spectral_axis import vac_to_air

cube = spectral_cube.SpectralCube.read('DATACUBEFINALuser_20140216T010259_78380e1d.fits', hdu=1)
# compute the continuum; it gets subtracted later
cont = cube.spectral_slab(7800*u.AA, 8200*u.AA).apply_numpy_function(np.mean, axis=0)


wavelengths = {
                #'pa40': 825.226,
                #'pa39': 825.456,
                #'pa38': 825.726,
                #'pa37': 826.016,
                #'pa36': 826.316,
                #'pa35': 826.655,
                #'pa34': 827.021,
                #'pa33': 827.421,
                #'pa32': 827.859,
                #'pa31': 828.341,
                #'pa30': 828.870,
                #'pa29': 829.458,
                #'pa28': 830.111,
                #'pa27': 830.838,
                #'pa26': 831.655,
                #'pa25': 832.571,
                #'pa24': 833.607,
                #'pa23': 834.783,
                #'pa22': 836.130,
                #'pa21': 837.678,
                'pa20': 839.471,
                'pa19': 841.563,
                'pa18': 844.027,
                'pa17': 846.959,
                'pa16': 850.483,
                'pa15': 854.773,
                'pa14': 860.075,
                'pa13': 866.740,
                'pa12': 875.286,
                'pa11': 886.532,
                'pa10': 901.78 ,
                'pa9' : 923.22 ,
}

# Cube velocity conversion should use vacuum wavelengths
slabs = {line:
         cube.with_spectral_unit(u.km/u.s, velocity_convention='optical',
                                 rest_value=wl*u.nm)
             .spectral_slab(-200*u.km/u.s, 250*u.km/u.s)
         for line,wl in wavelengths.items()}

for line,slab in slabs.items():
    print "kms",line
    slab._data -= cont # CONTINUUM SUBTRACTION HERE
    mom1 = slab.moment1(axis=0)
    mom1.write('moment1_{0}_kms.fits'.format(line), overwrite=True)
mean_moment = np.mean([fits.getdata('moment1_{0}_kms.fits'.format(line)) for
                       line in slabs], axis=0)
fits.PrimaryHDU(data=mean_moment, header=fits.getheader('moment1_{0}_kms.fits'.format(line))).writeto('moment1_paschen_mean_kms.fits', clobber=True)

newcube_shape = (sum(s.shape[0] for s in slabs.values()),) + slabs.values()[0].shape[1:]
newcube_spaxis = np.concatenate([s.spectral_axis for s in slabs.values()]).value*u.km/u.s
sortvect = newcube_spaxis.argsort()
sortspaxis = newcube_spaxis[sortvect]

newcube = np.empty(newcube_shape)

# normalize
ind = 0
for ii,slab in enumerate(slabs.values()):
    data = slab.filled_data[:] / slab.sum(axis=0)
    newcube[ind:ind+data.shape[0], :, :] = data
    ind += data.shape[0]

supercube = newcube[sortvect, :, :]

pxarr = pyspeckit.units.SpectroscopicAxis(sortspaxis.value, units='km/s')
pcube = pyspeckit.Cube(cube=supercube, xarr=pxarr)

pcube.fiteach(fittype='gaussian', guesses=[1/np.sqrt(np.pi), 10, 50.0],
              errmap=np.ones(supercube.shape[1:])/100., multicore=40)

pcube.write_fit('velocity_fits_paschen.fits', clobber=True)
