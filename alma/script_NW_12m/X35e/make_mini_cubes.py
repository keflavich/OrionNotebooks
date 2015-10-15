import numpy as np
from astropy import units as u
from spectral_cube import SpectralCube
from lines import lines


for spwnum in (0,1,2,3):
    cube = SpectralCube.read('Orion_NW_12m_spw{0}_lines.fits'.format(spwnum))

    for line,frq in lines.items():
        if frq > cube.spectral_extrema[0] and frq < cube.spectral_extrema[1]:
            print("Extracting {0}".format(line))
            vcube = cube.with_spectral_unit(u.km/u.s, rest_value=frq,
                                            velocity_convention='radio')
            subcube = vcube.spectral_slab(2*u.km/u.s, 15*u.km/u.s)
            frqint = int(np.round(frq.to(u.GHz).value))
            subcube.write("Orion_NW_12m_spw{0}_{1}_{2}.fits".format(spwnum,
                                                                    line,
                                                                    frqint),
                          overwrite=True)
