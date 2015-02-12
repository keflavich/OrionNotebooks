from astropy import units as u
import numpy as np
import spectral_cube
import pyspeckit

cube = spectral_cube.SpectralCube.read('CUBEec_nall.fits', hdu=1)
cont = cube.spectral_slab(6380*u.AA, 6500*u.AA).apply_numpy_function(np.mean, axis=0)
cube._data -= cont

# Header says AWAV: air wavelengths.  It also says the coordinates are barycentric.
# V_LSR = V_helio - 18 km/s according to Garcia-Diaz et al 2008
wavelengths = spectral_cube.spectral_axis.vac_to_air(np.array([6302.046,
    6313.8,  6365.536, 6549.85, 6564.61, 6585.28, 6679.99556,  6718.29,
    6732.67])*u.AA)
# 5877.25, 7064.21, 7137.8,  7320.94, 7331.68

slabs = [cube.with_spectral_unit(u.km/u.s, 'optical', wl).spectral_slab(-200*u.km/u.s, 200*u.km/u.s)
         for wl in wavelengths]

newcube_shape = (sum(s.shape[0] for s in slabs),) + slabs[0].shape[1:]
newcube_spaxis = np.concatenate([s.spectral_axis for s in slabs]).value*u.km/u.s
sortvect = newcube_spaxis.argsort()
sortspaxis = newcube_spaxis[sortvect]

newcube = np.empty(newcube_shape)

# normalize
ind = 0
for ii,slab in enumerate(slabs):
    data = slab.filled_data[:] / slab.sum(axis=0)
    newcube[ind:ind+data.shape[0], :, :] = data
    ind += data.shape[0]

supercube = newcube[sortvect, :, :]

pxarr = pyspeckit.units.SpectroscopicAxis(sortspaxis.value, units='km/s')
pcube = pyspeckit.Cube(cube=supercube, xarr=pxarr)

pcube.fiteach(fittype='gaussian', guesses=[1/np.sqrt(np.pi), 10, 50.0],
              errmap=np.ones(supercube.shape[1:])/100., multicore=40)

pcube.write_fit('velocity_fits_air.fits', clobber=True)
