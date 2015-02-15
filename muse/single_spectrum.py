import numpy as np
from astropy import units as u
from astropy.io import fits
import spectral_cube
from lines import lines

coordinate = [1008,655]

def extract_spectra():
    cube_085 = spectral_cube.SpectralCube.read('DATACUBEFINALuser_20140216T010259_78380e1d.fits', hdu=1).with_spectral_unit(u.AA)
    cube_125 = spectral_cube.SpectralCube.read('CUBEec_nall.fits', hdu=1).with_spectral_unit(u.AA)

    sp085 = cube_085[:,coordinate[1], coordinate[0]]
    sp125 = cube_125[:,coordinate[1], coordinate[0]]

    sp085.write("spectrum_{0}_{1}_085.fits".format(*coordinate), overwrite=True)
    sp125.write("spectrum_{0}_{1}_125.fits".format(*coordinate), overwrite=True)


def examine_spectra():
    import pylab as pl
    import pyspeckit
    sp1 = pyspeckit.Spectrum("spectrum_{0}_{1}_085.fits".format(*coordinate))
    sp2 = pyspeckit.Spectrum("spectrum_{0}_{1}_125.fits".format(*coordinate))

    wavelengths = (np.array(lines.values())*u.AA).value
    sp1.xarr.convert_to_unit('angstroms')
    sp2.xarr.convert_to_unit('angstroms')
    sp1.plotter()
    sp2.plotter(axis=sp1.plotter.axis, color='b', clear=False)
    sp1.plotter.line_ids([str(x) for x in range(len(wavelengths))],
                         wavelengths, xval_units='angstroms')
    cont1 = sp1.slice(6380, 6500, units='angstrom').data.mean()
    cont2 = sp1.slice(6380, 6500, units='angstrom').data.mean()


    velo = 200

    spectra1 = []
    spectra2 = []
    fitvals = []
    for line in wavelengths:
        x = sp1.xarr.as_unit('km/s', center_frequency=line, center_frequency_units='angstroms')
        ssl085 = sp1.slice(x.x_to_pix(-velo), x.x_to_pix(velo))
        ssl085.xarr.convert_to_unit('km/s', center_frequency=line, center_frequency_units='angstroms')
        spectra1.append(ssl085)
        ssl085.specfit(reset=True, verbose=False)
        ssl085.specfit(reset=True, verbose=False)

        x = sp2.xarr.as_unit('km/s', center_frequency=line, center_frequency_units='angstroms')
        ssl125 = sp2.slice(x.x_to_pix(-velo), x.x_to_pix(velo))
        ssl125.xarr.convert_to_unit('km/s', center_frequency=line, center_frequency_units='angstroms')
        spectra2.append(ssl125)
        ssl125.specfit(reset=True, verbose=False)
        ssl125.specfit(reset=True, verbose=False)
        print "{0}: 085 v={1}, 125 v={2}".format(line,
                                                 ssl085.specfit.parinfo.SHIFT0.value,
                                                 ssl125.specfit.parinfo.SHIFT0.value,)

        fitvals.append([line,
                        ssl085.specfit.parinfo.SHIFT0.value,
                        ssl085.specfit.parinfo.SHIFT0.error,
                        ssl125.specfit.parinfo.SHIFT0.value,
                        ssl125.specfit.parinfo.SHIFT0.error,])

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

    pl.figure(5).clf()
    fitvals = np.array(fitvals)
    pl.errorbar(fitvals[:,0], fitvals[:,1], yerr=fitvals[:,2], linestyle='none')
    pl.errorbar(fitvals[:,0], fitvals[:,3], yerr=fitvals[:,4], linestyle='none')

    vmap_125 = fits.getdata('velocity_fits_125.fits')
    v125,e125 = vmap_125[1,coordinate[1],coordinate[0]],vmap_125[4,coordinate[1],coordinate[0]]
    pl.axhline(v125, linestyle='-', color='k')
    pl.axhline(v125-e125, linestyle='--', color='k')
    pl.axhline(v125+e125, linestyle='--', color='k')

    return locals()
