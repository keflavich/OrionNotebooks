path = '/Volumes/passport/alma/orion/'
froot = 'calibrated.ms.image.line'

mapping = {'hcn4-3': 'spw0',
           'hcop4-3': 'spw1',
           'co3-2': 'spw2'}
freq = {'hcn4-3':354.50548*u.GHz,
        'hcop4-3':356.73424*u.GHz,
        'co3-2':345.79599*u.GHz}

for source in ('source4',):
    for line in mapping:

        fn ='{path}/{froot}.{source}.{spw}.image.fits'.format(path=path,
                                                              froot=froot,
                                                              spw=mapping[line],
                                                              source=source)

        cube = (SpectralCube.read(fn)
                            .with_spectral_unit(u.km/u.s, rest_value=freq[line],
                                                velocity_convention='radio')
                            .spectral_slab(-50*u.km/u.s, 100*u.km/u.s))

        cube.write('{line}_{source}.fits'.format(line=line, source=source))
