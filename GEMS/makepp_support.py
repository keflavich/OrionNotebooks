#pylint: disable-all
import numpy as np
import os
import AG_fft_tools
import agpy
import astropy.nddata
from astropy.io import fits as pyfits
import time
import aplpy
import pyavm
t0 = time.time()

#import psi.process

#def get_mem():
#    pid = psi.process.ProcessTable()[os.getpid()]
#    return pid.vsz

os.chdir('/Users/adam/work/orion/GEMS')

import pyregion
stars = pyregion.open('ks_NS_catalog.reg')
#trapstars = pyregion.open('trapstars.reg')
header = pyfits.getheader('big_mosaic_feii.fits')
wcs=astropy.wcs.WCS(header)
star_coords = np.array([wcs.wcs_world2pix([s.coord_list],0) for s in stars]).squeeze()
#trapstarcoords = np.array([wcs.wcs_world2pix([s.coord_list[:2]],0) for s in trapstars]).squeeze()
#trapstarradii = np.array([1.5 * s.params[2].degree / wcs.wcs.cd[1,1] for s in trapstars])

avm = pyavm.AVM.from_header(header)

def mask_image(image, star_coords=star_coords, downsample=1, radius=50):
    if downsample != 1:
        image = image[::downsample,::downsample].copy()
    else:
        image = image.copy() # memory expensive, but needed for masking =/
    yy,xx = np.indices(image.shape)
    #rr = (xx**2+yy**2)**0.5
    d = float(downsample)
    r = radius / d
    for x,y in star_coords:
        x /= d
        y /= d
        mask = ((xx[y-r:y+r,x-r:x+r]-x)**2+(yy[y-r:y+r,x-r:x+r]-y)**2) < (r)**2
        image[y-r:y+r,x-r:x+r][mask] = np.nan
    #for (x,y),r in zip(trapstarcoords,trapstarradii):
    #    x /= d
    #    y /= d
    #    r /= d
    #    mask = ((xx[y-r:y+r,x-r:x+r]-x)**2+(yy[y-r:y+r,x-r:x+r]-y)**2) < (r)**2
    #    image[y-r:y+r,x-r:x+r][mask] = np.nan
    return image



