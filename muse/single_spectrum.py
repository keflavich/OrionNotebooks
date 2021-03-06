import numpy as np
from astropy import units as u
from astropy.io import fits
import spectral_cube
from lines import lines
import pyregion


coordinate = [1008,655] # 05h35m15.338s -05d23m59.9159s
def extract_spectra():
    cube_085 = spectral_cube.SpectralCube.read('DATACUBEFINALuser_20140216T010259_78380e1d.fits', hdu=1).with_spectral_unit(u.AA)
    cube_125 = spectral_cube.SpectralCube.read('CUBEec_nall.fits', hdu=1).with_spectral_unit(u.AA)

    sp085 = cube_085[:,coordinate[1], coordinate[0]]
    sp125 = cube_125[:,coordinate[1], coordinate[0]]

    sp085.write("spectrum_{0}_{1}_085.fits".format(*coordinate), overwrite=True)
    sp125.write("spectrum_{0}_{1}_125.fits".format(*coordinate), overwrite=True)

def extract_b00():
    regions = pyregion.open('B00.reg')

    cube_085 = spectral_cube.SpectralCube.read('DATACUBEFINALuser_20140216T010259_78380e1d.fits', hdu=1).with_spectral_unit(u.AA)
    cube_125 = spectral_cube.SpectralCube.read('CUBEec_nall.fits', hdu=1).with_spectral_unit(u.AA)
    reg_085 = cube_085.subcube_from_ds9region(regions)
    reg_125 = cube_125.subcube_from_ds9region(regions)

    sp085 = reg_085.sum(axis=(1,2))
    sp125 = reg_125.sum(axis=(1,2))
    # temporary workaround:
    if not isinstance(sp085, spectral_cube.spectral_cube.OneDSpectrum):
        x = sp085
        sp085 = cube_085[:,0,0]
        sp085 = spectral_cube.spectral_cube.OneDSpectrum(x, unit=sp085.unit, copy=False,
                                           wcs=sp085.wcs, meta=sp085.meta)
        x = sp125
        sp125 = cube_125[:,0,0]
        sp125 = spectral_cube.spectral_cube.OneDSpectrum(x, unit=sp125.unit, copy=False,
                                           wcs=sp125.wcs, meta=sp125.meta)

    sp085.write("spectrum_B00_085.fits", overwrite=True)
    sp125.write("spectrum_B00_125.fits", overwrite=True)


def examine_spectra(sp085filename="spectrum_{0}_{1}_085.fits".format(*coordinate), 
                    sp125filename="spectrum_{0}_{1}_125.fits".format(*coordinate), 
                    coordinate=coordinate,
                    ymax=1.4e7,
                   ):
    import pylab as pl
    import pyspeckit
    sp1 = pyspeckit.Spectrum(sp085filename)
    sp2 = pyspeckit.Spectrum(sp125filename)

    wavelengths = (np.array(lines.values())*u.AA).value
    sp1.xarr.convert_to_unit('angstroms')
    sp2.xarr.convert_to_unit('angstroms')
    pl.figure(1).clf()
    sp1.plotter(figure=pl.figure(1), ymax=ymax)
    sp2.plotter(axis=sp1.plotter.axis, color='b', clear=False, ymax=ymax)
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
    sp2new.plotter(axis=sp1new.plotter.axis, clear=False, color='b',
                   marker='.', linestyle='none')
    sp1new.specfit()
    sp2new.specfit()
    print sp1new.specfit.parinfo
    print sp2new.specfit.parinfo

    pl.figure(5).clf()
    fitvals = np.array(fitvals)
    pl.errorbar(fitvals[:,0], fitvals[:,1], yerr=fitvals[:,2], color='k', linestyle='none', label='0.85$\AA$')
    pl.errorbar(fitvals[:,0], fitvals[:,3], yerr=fitvals[:,4], color='r', linestyle='none', label='1.25$\AA$')

    if isinstance(coordinate, pyregion.ShapeList):
        vmap_125 = fits.open('velocity_fits_125.fits')
        mask_125 = coordinate.get_mask(hdu=vmap_125[0])
        vmap_085 = fits.open('velocity_fits_085.fits')
        mask_085 = coordinate.get_mask(hdu=vmap_085[0])
        v125 = vmap_125[1,mask_125].mean()
        v085 = vmap_085[1,mask_085].mean()

    else:
        vmap_125 = fits.getdata('velocity_fits_125.fits')
        v125,e125 = vmap_125[1,coordinate[1],coordinate[0]],vmap_125[4,coordinate[1],coordinate[0]]

        vmap_085 = fits.getdata('velocity_fits_085.fits')
        v085,e085 = vmap_085[1,coordinate[1],coordinate[0]],vmap_085[4,coordinate[1],coordinate[0]]

    pl.axhline(v125, linestyle='--', color='r')
    #pl.axhline(v125-e125, linestyle='--', color='k')
    #pl.axhline(v125+e125, linestyle='--', color='k')
    pl.axhline(v085, linestyle='--', color='k')
    #pl.axhline(v085-e085, linestyle='--', color='k')
    #pl.axhline(v085+e085, linestyle='--', color='k')
    pl.legend(loc='best')
    pl.xlabel("Wavelength ($\AA$)")
    pl.ylabel("Flux ($10^{-20}$ erg s$^{-1}$ cm$^{-2} \AA^{-1}$")

    return locals()
