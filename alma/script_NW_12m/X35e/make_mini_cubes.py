import numpy as np
from astropy import units as u
from spectral_cube import SpectralCube


lines = {'H2C34S_717-616': 232.75471*u.GHz,
         '13CS_5-4': 231.22069*u.GHz,
         'D2CO_404-303': 231.41026*u.GHz,
         'D2CS_707-606': 216.66243*u.GHz,
         'H2S_220-211': 216.71044*u.GHz,
        }

for spwnum in (0,1,2):
    cube = SpectralCube.read('Orion_NW_12m_spw{0}_lines.fits'.format(spwnum))

    for line,frq in lines.items():
        if frq > cube.spectral_extrema[0] and frq < cube.spectral_extrema[1]:
            print("Extracting {0}".format(line))
            vcube = cube.with_spectral_unit(u.km/u.s, rest_value=frq,
                                            velocity_convention='radio')
            subcube = vcube.spectral_slab(0*u.km/u.s, 18*u.km/u.s)
            frqint = int(np.round(frq.to(u.GHz).value))
            subcube.write("Orion_NW_12m_spw{0}_{1}_{2}.fits".format(spwnum,
                                                                    line,
                                                                    frqint),
                          overwrite=True)
