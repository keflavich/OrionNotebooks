from astropy.io import fits
from astropy import units as u
import numpy as np
import spectral_cube
import pyspeckit
from spectral_cube.spectral_axis import vac_to_air

cube = spectral_cube.SpectralCube.read('DATACUBEFINALuser_20140216T010259_78380e1d.fits', hdu=1)
cont = cube.spectral_slab(6380*u.AA, 6500*u.AA).apply_numpy_function(np.mean, axis=0)
cube._data -= cont

# Header says AWAV: air wavelengths.  It also says the coordinates are barycentric.
# V_LSR = V_helio - 18 km/s according to Garcia-Diaz et al 2008
# These are the lines' vacuum wavelengths
lines = {'OI6300': 6302.046,
         'SIII6313': 6313.8,
         'OI6363': 6365.536,
         'NII6548': 6549.85,
         'HAlpha': 6564.61,
         'NII6584': 6585.28,
         'HeI6678': 6679.99556,
         'SII6716': 6718.29,
         'SII6731': 6732.67,
}
airlines = {line: vac_to_air(wl*u.AA) for line,wl in lines.items()}
#wavelengths = spectral_cube.spectral_axis.vac_to_air(np.array(lines.values())*u.AA)
# 5877.25, 7064.21, 7137.8,  7320.94, 7331.68

wlslabs = {line:
           cube.spectral_slab(wl-5*u.AA, wl+6*u.AA)
           for line,wl in airlines.items()}

for line,slab in wlslabs.items():
    print "AA",line
    mom1 = slab.moment1_085(axis=0)
    mom1.write('moment1_085_{0}_angstroms.fits'.format(line), overwrite=True)
mean_moment = np.mean([fits.getdata('moment1_085_{0}_angstroms.fits'.format(line))-airlines[line].value
                       for line in wlslabs], axis=0)
fits.PrimaryHDU(data=mean_moment, header=fits.getheader('moment1_085_{0}_angstroms.fits'.format(line))).writeto('moment1_085_mean_deltaangstroms.fits', clobber=True)

# Cube velocity conversion should use vacuum wavelengths
slabs = {line:
         cube.with_spectral_unit(u.km/u.s, velocity_convention='optical',
                                 rest_value=wl*u.AA)
             .spectral_slab(-200*u.km/u.s, 250*u.km/u.s)
         for line,wl in lines.items()}

for line,slab in slabs.items():
    print "kms",line
    mom1 = slab.moment1_085(axis=0)
    mom1.write('moment1_085_{0}_kms.fits'.format(line), overwrite=True)
mean_moment = np.mean([fits.getdata('moment1_085_{0}_kms.fits'.format(line)) for
                       line in slabs], axis=0)
fits.PrimaryHDU(data=mean_moment, header=fits.getheader('moment1_085_{0}_kms.fits'.format(line))).writeto('moment1_085_mean_kms.fits', clobber=True)

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

pcube.write_fit('velocity_fits_085.fits', clobber=True)
