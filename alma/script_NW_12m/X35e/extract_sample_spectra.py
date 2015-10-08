import pyregion
from spectral_cube import SpectralCube

r = pyregion.open('box_for_diffuse_line_hunt.reg')

for spwnum in (0,1):
    cube1 = SpectralCube.read('Orion_NW_12m_spw{0}_lines.fits'.format(spwnum))

    spw1 = cube1.subcube_from_ds9region(r).mean(axis=(1,2))
    spw1.hdu.writeto('diffuse_box_spw{0}.fits'.format(spwnum), clobber=True)

    spw1 = cube1[:,294,204]
    spw1.hdu.writeto('hotcore_spw{0}.fits'.format(spwnum), clobber=True)
