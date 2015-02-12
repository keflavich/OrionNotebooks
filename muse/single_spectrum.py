import numpy as np
from astropy.io import fits
import spectral_cube

coordinate = [1008,655]

cube_085 = spectral_cube.SpectralCube.read('DATACUBEFINALuser_20140216T010259_78380e1d.fits', hdu=1)
cube_125 = spectral_cube.SpectralCube.read('CUBEec_nall.fits', hdu=1)

sp085 = cube_085[:,coordinate[1], coordinate[0]]
sp125 = cube_125[:,coordinate[1], coordinate[0]]

sp085.write("spectrum_{0}_{1}_085.fits".format(*coordinate), overwrite=True)
sp125.write("spectrum_{0}_{1}_125.fits".format(*coordinate), overwrite=True)

sp085.quicklook(None)
sp125.quicklook(None)


import pyspeckit
import pylab as pl
sp1 = pyspeckit.Spectrum("spectrum_{0}_{1}_085.fits".format(*coordinate))
sp2 = pyspeckit.Spectrum("spectrum_{0}_{1}_125.fits".format(*coordinate))

wavelengths = spectral_cube.spectral_axis.vac_to_air(np.array([6302.046,
                                                               6313.8,
                                                               6365.536,
                                                               6549.85,
                                                               6564.61,
                                                               6585.28,
                                                               6679.99556,
                                                               6718.29,
                                                               6732.67])*u.AA).value
sp1.xarr.convert_to_unit('angstroms')
sp2.xarr.convert_to_unit('angstroms')
sp1.plotter()
sp2.plotter(axis=sp1.plotter.axis, color='b', clear=False)
sp1.plotter.line_ids([str(x) for x in range(len(wavelengths))], wavelengths, xval_units='angstroms')
cont1 = sp1.slice(6380, 6500, units='angstrom').data.mean()
cont2 = sp1.slice(6380, 6500, units='angstrom').data.mean()


velo = 200

spectra1 = []
spectra2 = []
for line in wavelengths:
    x = sp1.xarr.as_unit('km/s', center_frequency=line, center_frequency_units='angstroms')
    ssl085 = sp1.slice(x.x_to_pix(-velo), x.x_to_pix(velo))
    ssl085.xarr.convert_to_unit('km/s', center_frequency=line, center_frequency_units='angstroms')
    spectra1.append(ssl085)
    ssl085.specfit()

    x = sp2.xarr.as_unit('km/s', center_frequency=line, center_frequency_units='angstroms')
    ssl125 = sp2.slice(x.x_to_pix(-velo), x.x_to_pix(velo))
    ssl125.xarr.convert_to_unit('km/s', center_frequency=line, center_frequency_units='angstroms')
    spectra2.append(ssl125)
    ssl125.specfit()
    print "{0}: 085 v={1}, 125 v={2}".format(line,
                                             ssl085.specfit.parinfo.SHIFT0.value,
                                             ssl125.specfit.parinfo.SHIFT0.value,)

pl.figure(4).clf()
pl.figure(5).clf()

x1s = []
d1s = []
for ss in spectra1:
    x1s += ss.xarr.tolist()
    ss.data -= cont1
    d1s += (ss.data/ss.data.sum()).tolist()
    ss.data /= ss.data.sum()
    ss.plotter(figure=pl.figure(4), clear=False)

x2s = []
d2s = []
for ss in spectra2:
    x2s += ss.xarr.tolist()
    ss.data -= cont2
    d2s += (ss.data/ss.data.sum()).tolist()
    ss.data /= ss.data.sum()
    ss.plotter(figure=pl.figure(5), clear=False)

sp2new = pyspeckit.Spectrum(xarr=np.sort(x2s), data=np.array(d2s)[np.argsort(x2s)], xarrkwargs={'units':'km/s'})
sp1new = pyspeckit.Spectrum(xarr=np.sort(x1s), data=np.array(d1s)[np.argsort(x1s)], xarrkwargs={'units':'km/s'})

pl.figure(2)
pl.clf()
pl.plot(x1s, d1s, 'r.')
pl.plot(x2s, d2s, 'b.')

pl.figure(3).clf()
sp1new.plotter(figure=pl.figure(3), marker='.', linestyle='none')
sp2new.plotter(axis=sp1new.plotter.axis, clear=False, color='b', marker='.', linestyle='none')
sp1new.specfit()
sp2new.specfit()
print sp1new.specfit.parinfo
print sp2new.specfit.parinfo
