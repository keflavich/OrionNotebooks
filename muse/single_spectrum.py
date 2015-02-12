from astropy.io import fits
import spectral_cube

coordinate = [1008,655]

cube_085 = spectral_cube.SpectralCube.read('DATACUBEFINALuser_20140216T010259_78380e1d.fits', hdu=1)
cube_125 = spectral_cube.SpectralCube.read('CUBEec_nall.fits', hdu=1)

sp085 = cube_085[:,coordinate[1], coordinate[0]]
sp125 = cube_125[:,coordinate[1], coordinate[0]]

sp085.write("spectrum_{0}_{1}_085.fits".format(*coordinate))
sp125.write("spectrum_{0}_{1}_125.fits".format(*coordinate))

sp085.quicklook(None)
sp125.quicklook(None)
