import pylab as pl
import matplotlib
import numpy as np
from astropy.io import fits
from astropy import units as u

def Orion_PVDiagrams(filename='OMC1_TSPEC_H2S1_cube.fits',restwavelength=2.1218*u.um, cm=pl.cm.hot,
                     start_fignum=0, min_valid=1e-16, hlcolor='k'):
    cube = fits.getdata(filename)
    header = fits.getheader(filename)

    wavelength = ((-header['CRPIX3']+np.arange(header['NAXIS3'])+1)*header['CD3_3'] + header['CRVAL3']) * u.AA
    velocity = wavelength.to('km/s',u.doppler_optical(restwavelength))

    nvel = len(velocity)

    sourceI = (196,130)
    def make_pv(startx=196,starty=130,endx=267,endy=388,npts=250):
        pvd = np.empty([nvel,npts])
        for ii,(x,y) in enumerate(zip(np.linspace(startx,endx,npts),np.linspace(starty,endy,npts))):
            pvd[:,ii] = cube[:,y,x]
        return pvd

    outflow_endpoints = [
                         (286,389),
                         (240,361),
                         (210,411),
                         (216,312),
                         (281,284),
                         (329,266),
                         (326,234),
                         (187,250)]

    for ii,(ex,ey) in enumerate(outflow_endpoints):
        dx = (ex-sourceI[0])
        dy = (ey-sourceI[1])
        angle = np.arctan2(dy,dx)
        cdelt = np.abs(header['CDELT1'] / np.cos(angle)) * 3600
        npts = (dx**2 + dy**2)**0.5
        pv = make_pv(endx=ex,endy=ey,npts=npts)
        pl.figure(start_fignum+ii/3)
        if ii % 3 == 0:
            pl.clf()
        ax = pl.subplot(3,1,ii % 3+1)
        vmin,vmax = velocity.min().value,velocity.max().value
        pv[pv<0] = np.nanmin(pv)
        pv[pv<min_valid] = min_valid
        pl.imshow(np.log10(pv),extent=[0,npts*cdelt,vmin,vmax,],aspect=np.abs(cdelt)/20, cmap=cm)
        pl.hlines(0,0,npts*cdelt,color=hlcolor,linestyle='--')
        pl.xlabel("Offset (\")")
        pl.ylabel("Velocity (km s$^{-1}$)")

        #new_yticks = {i:velocity[i] for i in ax.get_yticks() if i>=0 and i<len(velocity)}
        #for v in new_yticks.values():
        #    v.setfield(np.round(v,1),'float')
        #ax.set_yticks(new_yticks.keys())
        #ax.set_yticklabels(new_yticks.values())



_cool_data = {'blue':   ((0., 0.0416, 0.0416),
                       (0.365079, 1.000000, 1.000000),
                       (1.0, 1.0, 1.0)),
             'green': ((0., 0., 0.),
                       (0.365079, 0.000000, 0.000000),
                       (0.746032, 1.000000, 1.000000),
                       (1.0, 1.0, 1.0)),
             'red':  ((0., 0., 0.),
                       (0.746032, 0.000000, 0.000000),
                       (1.0, 1.0, 1.0))}


def do_plots():

    cool = matplotlib.colors.LinearSegmentedColormap('cool',_cool_data)
    cool.set_bad('k')
    hot = matplotlib.cm.hot
    hot.set_bad('k')

    Orion_PVDiagrams(cm=hot)
    Orion_PVDiagrams('OMC1_TSPEC_H2FeII1.64_cube.fits',restwavelength=1.64319*u.um, start_fignum=3, cm=cool, hlcolor='w', min_valid=1e-17)
    Orion_PVDiagrams('OMC1_TSPEC_H2FeII1.60_cube.fits',restwavelength=1.59905*u.um, start_fignum=6, cm=cool, hlcolor='w', min_valid=1e-17)
    Orion_PVDiagrams('OMC1_TSPEC_H2BrG_cube.fits',restwavelength=2.1661*u.um, start_fignum=9, cm=hot, hlcolor='k', min_valid=1e-16)
