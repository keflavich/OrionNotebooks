"""
Run from parent directory, make sure pvdiagrams/ and FITS/ exist as subdirs
"""
import os
import numpy as np
from numpy import sin,cos
from astropy import units as u
from astropy import coordinates
from spectral_cube import SpectralCube
from astropy.io import fits
import pvextractor
import aplpy
import pylab as pl

nrot = 360
angles = np.linspace(0,359,nrot)
angles_rad = angles * np.pi/180.

dx = 1*u.arcmin
#oldcenter = coordinates.SkyCoord('5:35:14.5 -5:22:23', unit=(u.hour, u.deg),
#                              frame='fk5')
center = coordinates.SkyCoord('5:35:14.360 -5:22:28.70', unit=(u.hour, u.deg),
                              frame='fk5')
sourcei = coordinates.SkyCoord('05:35:14.5121 -05 22 30.521', unit=(u.hour,
                                                                    u.deg),
                               frame='fk5')

paths = [ coordinates.SkyCoord([center.ra+dx*cos(theta),
                                center.ra-dx*cos(theta)],
                               [center.dec+dx*sin(theta),
                                center.dec-dx*sin(theta)],
                               unit=(u.deg, u.deg))
         for theta in angles_rad ]


cube = SpectralCube.read('FITS/ALMA_Outflow_b6_12M_12CO.fits')
cube = SpectralCube.read('FITS/Orion_NWSE_12CO2-1_merge_7m_12m.image.fits')
mask = (cube.spectral_axis < 3*u.km/u.s) | (cube.spectral_axis > 14.5*u.km/u.s)
cube = cube.with_mask(mask[:,None,None])
mx = cube.max(axis=0)
med = cube.median(axis=0)
mx = mx - med


pl.close(1)

for ii,(path,theta) in enumerate(zip(paths, angles)):
    outfilename = "pvdiagrams/NWSE_rotation_{0:0.4g}.fits".format(theta)
    if os.path.exists(outfilename):
        hdu = fits.open(outfilename)[0]
    else:
        hdu = pvextractor.extract_pv_slice(cube=cube, path=path)
        hdu.writeto(outfilename)
    print(theta,outfilename)

    pl.figure(1, figsize=(12,12)).clf()
    F = aplpy.FITSFigure(hdu, figure=pl.figure(1), subplot=[0.1, 0.6, 0.8, 0.35])
    F.show_grayscale()
    F.set_title("Rotation {0:0.4g} degrees".format(theta))
    
    F2 = aplpy.FITSFigure(mx.hdu, figure=pl.figure(1), subplot=[0.25,0.05, 0.5, 0.45])
    F2.show_grayscale()
    F2.show_lines([np.array([path.ra.deg, path.dec.deg])], color='r')
    F2.recenter(center.ra, center.dec, radius=(1.1*u.arcmin).to(u.deg).value)

    F.save('pvdiagrams/NWSE_rotation_{0:04d}.png'.format(ii), dpi=300)

# command will be run from within pvdiagrams/
cmd = "ffmpeg -y -i NWSE_rotation_%04d.png -c:v libx264 -pix_fmt yuv420p -vf scale=1024:768 -r 10 rotation_movie.mp4"
import subprocess
p = subprocess.Popen(cmd.split(), cwd='pvdiagrams/')
p.wait()


theta = 39*u.deg
sourcei_n = coordinates.SkyCoord(sourcei.ra, sourcei.dec+3*u.arcsec)
p = (coordinates.SkyCoord([sourcei_n.ra+dx*cos(theta),
                      sourcei_n.ra-dx*cos(theta)],
                     [sourcei_n.dec+dx*sin(theta),
                      sourcei_n.dec-dx*sin(theta)],
                     unit=(u.deg, u.deg)))
path = pvextractor.Path(p, width=4*u.arcsec)
patches = path.to_patches(spacing=10, wcs=mx.wcs)
for atch in patches:
    atch.set_facecolor('none')
    atch.set_edgecolor('blue')

hdu = pvextractor.extract_pv_slice(cube=cube, path=path)

pl.figure(1, figsize=(12,12)).clf()
F = aplpy.FITSFigure(hdu, figure=pl.figure(1), subplot=[0.1, 0.6, 0.8, 0.35])
F.show_grayscale()
F.set_title("Rotation {0:0.4g} degrees".format(theta))
F2.save('pvdiagrams/pvslice_along_sourcei_n.png')
    

F2 = aplpy.FITSFigure(mx.hdu, figure=pl.figure(1), subplot=[0.25,0.05, 0.5, 0.45])
F2.show_grayscale()
F2.show_lines([np.array([p.ra.deg, p.dec.deg])], color='r')
F2.recenter(center.ra, center.dec, radius=(1.1*u.arcmin).to(u.deg).value)
for x in patches:
    F2._ax1.add_patch(x)
F2.show_markers(sourcei.ra.deg, sourcei.dec.deg, color='g', zorder=1000,
                edgecolor='g',
                marker='x')
F2.save('pvdiagrams/cubemax_with_markers.png')
