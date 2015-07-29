import os
import glob
from astropy import units as u
from spectral_cube import SpectralCube

path = '/Volumes/passport/alma/orion/'
froot = 'calibrated.ms.image.line'

mapping = {'hcn4-3': 'spw0',
           'hcop4-3': 'spw1',
           'co3-2': 'spw2'}
freq = {#'hcn4-3':354.50548*u.GHz,
        #'hcop4-3':356.73424*u.GHz,
        #'co2-1':230.538*u.GHz,
        #'co3-2':345.79599*u.GHz,
        'sio5-4':217.10498*u.GHz,
       }

for source in ('source4',):
    for fn in glob.glob('{path}/*ms*.fits'.format(path=path)):
        try:
            cube = SpectralCube.read(fn)
        except:
            print "Skipped ",fn," because of error"
            continue
        print "Loaded cube ",fn
        if 'bigbeam' in fn:
            beamsize = 'big'
        elif 'smallbeam' in fn:
            beamsize = 'small'
        else:
            beamsize = 'other'

        print fn,cube.spectral_axis.min(),cube.spectral_axis.max()
        for line in freq:
            if ((freq[line] > cube.spectral_axis.min()) and
                (freq[line] < cube.spectral_axis.max())):
                vcube = (cube.with_spectral_unit(u.km/u.s,
                                                 rest_value=freq[line],
                                                 velocity_convention='radio')
                             .spectral_slab(-150*u.km/u.s, 150*u.km/u.s))


                outfn = '{line}_{source}_{beamsize}.fits'.format(line=line,
                                                                 source=source,
                                                                 beamsize=beamsize)
                print "Extracting {0} -> {1}".format(fn,outfn)
                vcube.write(outfn, overwrite=True)
