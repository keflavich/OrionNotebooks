from __future__ import print_function
from astropy import units as u
import numpy as np
from spectral_cube import SpectralCube, BooleanArrayMask
import os
import glob
import montage_wrapper

os.chdir('/Users/adam/work/orion/alma/FITS')

files = glob.glob('Orion*spw*2[123][0-9].fits')
files = glob.glob('Orion*spw*C18O*2[123][0-9].fits')

for fn in files:
    pfx = os.path.splitext(fn)[0]
    if 'contsub' in pfx:
        continue

    cube = SpectralCube.read(fn).with_spectral_unit(u.km/u.s, velocity_convention='radio')
    print(fn,cube)
    m0 = cube.moment0(axis=0)
    max = cube.max(axis=0)
    med = cube.median(axis=0)
    m0.hdu.writeto('moment0/{0}_moment0.fits'.format(pfx), clobber=True)
    max.hdu.writeto('max/{0}_max.fits'.format(pfx), clobber=True)
    med.hdu.writeto('med/{0}_med.fits'.format(pfx), clobber=True)

    ftemplate = "max/"+pfx.replace("NW","{0}").replace("SE","{0}")+"_max.fits"
    montage_wrapper.wrappers.mosaic_files([ftemplate.format("NW"), ftemplate.format("SE")], outfile=ftemplate.format('montage'),)

    ftemplate = "moment0/"+pfx.replace("NW","{0}").replace("SE","{0}")+"_moment0.fits"
    montage_wrapper.wrappers.mosaic_files([ftemplate.format("NW"), ftemplate.format("SE")], outfile=ftemplate.format('montage'),)

    ftemplate = "med/"+pfx.replace("NW","{0}").replace("SE","{0}")+"_med.fits"
    montage_wrapper.wrappers.mosaic_files([ftemplate.format("NW"), ftemplate.format("SE")], outfile=ftemplate.format('montage'),)
