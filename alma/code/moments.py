from spectral_cube import SpectralCube
import radio_beam
from astropy import units as u

cube = SpectralCube.read('ALMA_Outflow_b6_12M_12CO.fits')
radio_beam.Beam.from_fits_header(cube.header)
beam = radio_beam.Beam.from_fits_header(cube.header)
mcube = cube.with_mask(cube>(0.3*u.K).to(u.Jy, u.brightness_temperature(beam, cube.wcs.wcs.restfrq*u.Hz)))
m0 = mcube.moment0()
m0.hdu.writeto("ALMA_Outflow_b6_12M_12CO_NW.masked_moment0.fits", clobber=True)
m0_blue = mcube.spectral_slab(-120*u.km/u.s, -0.3*u.km/u.s).moment0()
m0_blue.hdu.writeto("ALMA_Outflow_b6_12M_12CO_NW.masked_moment0_blue.fits", clobber=True)
m0_red = mcube.spectral_slab(21*u.km/u.s, 120*u.km/u.s).moment0()
m0_red.hdu.writeto("ALMA_Outflow_b6_12M_12CO_NW.masked_moment0_red.fits", clobber=True)

mx = mcube.max(axis=0)
mx.hdu.writeto("ALMA_Outflow_b6_12M_12CO_NW.masked_max.fits", clobber=True)
mx_blue = mcube.spectral_slab(-120*u.km/u.s, -0.3*u.km/u.s).max(axis=0)
mx_blue.hdu.writeto("ALMA_Outflow_b6_12M_12CO_NW.masked_max_blue.fits", clobber=True)
mx_red = mcube.spectral_slab(21*u.km/u.s, 120*u.km/u.s).max(axis=0)
mx_red.hdu.writeto("ALMA_Outflow_b6_12M_12CO_NW.masked_max_red.fits", clobber=True)



cubeSE = SpectralCube.read('ALMA_Outflow_b6_12M_12CO_SE.fits')
mcubeSE = cubeSE.with_mask(cubeSE>(0.3*u.K).to(u.Jy, u.brightness_temperature(radio_beam.Beam.from_fits_header(cubeSE.header), cubeSE.wcs.wcs.restfrq*u.Hz)))
m0SE = mcubeSE.moment0()
m0SE.hdu.writeto("ALMA_Outflow_b6_12M_12CO_SE.masked_moment0.fits", clobber=True)
m0SE_blue = mcubeSE.spectral_slab(-120*u.km/u.s, -0.3*u.km/u.s).moment0()
m0SE_blue.hdu.writeto("ALMA_Outflow_b6_12M_12CO_SE.masked_moment0_blue.fits", clobber=True)
m0SE_red = mcubeSE.spectral_slab(21*u.km/u.s, 120*u.km/u.s).moment0()
m0SE_red.hdu.writeto("ALMA_Outflow_b6_12M_12CO_SE.masked_moment0_red.fits", clobber=True)

mxSE = mcubeSE.max(axis=0)
mxSE.hdu.writeto("ALMA_Outflow_b6_12M_12CO_SE.masked_max.fits", clobber=True)
mxSE_blue = mcubeSE.spectral_slab(-120*u.km/u.s, -0.3*u.km/u.s).max(axis=0)
mxSE_blue.hdu.writeto("ALMA_Outflow_b6_12M_12CO_SE.masked_max_blue.fits", clobber=True)
mxSE_red = mcubeSE.spectral_slab(21*u.km/u.s, 120*u.km/u.s).max(axis=0)
mxSE_red.hdu.writeto("ALMA_Outflow_b6_12M_12CO_SE.masked_max_red.fits", clobber=True)


import montage_wrapper
ftemplate = 'ALMA_Outflow_b6_12M_12CO{0}.masked_moment0{1}.fits'
montage_wrapper.wrappers.mosaic_files([ftemplate.format('_NW',''), ftemplate.format('_SE','')], outfile=ftemplate.format('',''),)
montage_wrapper.wrappers.mosaic_files([ftemplate.format('_NW','_blue'), ftemplate.format('_SE','_blue')], outfile=ftemplate.format('','_blue'),)
montage_wrapper.wrappers.mosaic_files([ftemplate.format('_NW','_red'), ftemplate.format('_SE','_red')], outfile=ftemplate.format('','_red'),)

ftemplate = 'ALMA_Outflow_b6_12M_12CO{0}.masked_max{1}.fits'
montage_wrapper.wrappers.mosaic_files([ftemplate.format('_NW',''), ftemplate.format('_SE','')], outfile=ftemplate.format('',''),)
montage_wrapper.wrappers.mosaic_files([ftemplate.format('_NW','_blue'), ftemplate.format('_SE','_blue')], outfile=ftemplate.format('','_blue'),)
montage_wrapper.wrappers.mosaic_files([ftemplate.format('_NW','_red'), ftemplate.format('_SE','_red')], outfile=ftemplate.format('','_red'),)
