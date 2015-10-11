import pyregion
from spectral_cube import SpectralCube

regions = pyregion.open('box_for_diffuse_line_hunt.reg')

for spwnum in (0,1,2):
    cube1 = SpectralCube.read('Orion_NW_12m_spw{0}_lines.fits'.format(spwnum))

    for reg in regions:
        r = pyregion.ShapeList([reg])
        name = reg.attr[1]['text']
        print("Extracting {0}".format(name))
        spw1 = cube1.subcube_from_ds9region(r).mean(axis=(1,2))
        spw1.hdu.writeto('{1}_spw{0}.fits'.format(spwnum, name), clobber=True)
