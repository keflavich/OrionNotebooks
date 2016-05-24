import numpy as np
from astropy import coordinates
from astropy import units as u
from astropy.io import fits
import aplpy
import pyavm
from PIL import Image

FF = aplpy.FITSFigure('/Users/adam/Dropbox/2012_GeMS_OMC1/omc1_h2_041122.fits')
FF.show_rgb('/Users/adam/work/orion/GEMS/Trapezium_NICFPS_mosaic_redblueorange_ALMA_large.png')
center = coordinates.SkyCoord('5:35:14.12 -5:21:45.0', frame='fk5', unit=(u.hour, u.deg))
FF.recenter(center.ra.deg, center.dec.deg, width=(2.45*u.arcmin).to(u.deg).value,
            height=(3.5*u.arcmin).to(u.deg).value)
FF.save("aplpy_Trapezium_NICFPS_mosaic_redblueorange_ALMA_large.png")
FF.show_regions("/Users/adam/Dropbox/2012_GeMS_OMC1/BNKL_sources_BN_I_n_white.reg", layer='sources')
FF.save("aplpy_Trapezium_NICFPS_mosaic_redblueorange_ALMA_large_regions.png")
FF.show_regions("/Users/adam/Dropbox/2012_GeMS_OMC1/BNKL_CO_H2_Feii_streamers.reg", layer='sources')
FF.save("aplpy_Trapezium_NICFPS_mosaic_redblueorange_ALMA_large_regions2.png")

imname = 'Trapezium_GEMS_mosaic_redblueorange_ALMA_normed_large_contrast_bright2.png'
avm = pyavm.avm.AVM.from_image(imname)
avm_wcs = avm.to_wcs()
nx, ny = Image.open(imname).size
hdu = fits.PrimaryHDU(data=np.empty([ny,nx]), header=avm_wcs.to_header())
FF2 = aplpy.FITSFigure(hdu)
FF2.show_rgb(imname)
FF2.recenter(center.ra.deg, center.dec.deg, width=(2.45*u.arcmin).to(u.deg).value,
             height=(3.5*u.arcmin).to(u.deg).value)
FF2.save("aplpy_{0}.png".format(imname))
FF2.show_regions("/Users/adam/Dropbox/2012_GeMS_OMC1/BNKL_sources_BN_I_n_white.reg", layer='sources')
FF2.save("aplpy_{0}_regions.png".format(imname))
FF2.show_regions("/Users/adam/Dropbox/2012_GeMS_OMC1/BNKL_CO_H2_Feii_streamers.reg", layer='sources')
FF2.save("aplpy_{0}_regions2.png".format(imname), dpi=300)
