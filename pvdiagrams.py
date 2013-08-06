import pylab as pl
import matplotlib
import numpy as np
from astropy.io import fits
from astropy import units as u
from astropy import wcs
from agpy import cubes
import pyspeckit
import string
from molecular_hydrogen.h2 import linename_to_restwl

sourceI = (196,130)
outflow_endpoints = [(286,396),
                     (240,361),
                     (210,411),
                     (216,312),
                     (287,296),
                     (329,266),
                     (327,228),
                     (187,250),
                     (163,363),
                     (296,249),
                     (280,250)]

def Orion_PVDiagrams(filename='OMC1_TSPEC_H2S1_cube.fits',restwavelength=2.1218*u.um, cm=pl.cm.hot,
                     start_fignum=0, min_valid=1e-16, displaymax=None, hlcolor='k', linename='H2 S(1) 1-0',
                     dosave=True):
    cube = fits.getdata(filename)
    header = fits.getheader(filename)

    wavelength = ((-header['CRPIX3']+np.arange(header['NAXIS3'])+1)*header['CD3_3'] + header['CRVAL3']) * u.AA
    velocity = wavelength.to('km/s',u.doppler_optical(restwavelength))

    nvel = len(velocity)

    def make_pv(startx=196,starty=130,endx=267,endy=388,npts=250):
        pvd = np.empty([nvel,npts])
        for ii,(x,y) in enumerate(zip(np.linspace(startx,endx,npts),np.linspace(starty,endy,npts))):
            pvd[:,ii] = cube[:,y,x]
        return pvd

    for ii,(ex,ey) in enumerate(outflow_endpoints):
        dx = (ex-sourceI[0])
        dy = (ey-sourceI[1])
        angle = np.arctan2(dy,dx)
        cdelt = np.abs(header['CDELT1'] / np.cos(angle)) * 3600
        npts = (dx**2 + dy**2)**0.5
        # pixels are in FITS units
        pv = make_pv(endx=ex-1,endy=ey-1,startx=sourceI[0]-1,starty=sourceI[0]-1,npts=npts)
        fignum = start_fignum+ii/3
        pl.figure(fignum)
        if ii % 3 == 0:
            pl.clf()
        ax = pl.subplot(3,1,ii % 3+1)
        vmin,vmax = velocity.min().value,velocity.max().value
        pv[pv<0] = np.nanmin(pv)
        pv[pv<min_valid] = min_valid
        pl.imshow(np.log10(pv),extent=[0,npts*cdelt,vmin,vmax,],aspect=np.abs(cdelt)/20, cmap=cm, 
                vmax=displaymax)
        pl.hlines(0,0,npts*cdelt,color=hlcolor,linestyle='--')
        ax.set_xlabel("Offset (\")")
        ax.set_ylabel("Velocity (km s$^{-1}$)")
        ax.set_title(linename+" Outflow Trace %i" % ii)
        if dosave and ii % 3 == 2:
            name = linename.replace(" ","_").replace("(","_").replace(")","_")
            name = ''.join([l for l in name if l in (string.ascii_letters+string.digits+"_")])
            figname = name+"_%i.png" % fignum
            pl.savefig(figname.replace("__","_"))

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

def make_regions(filename='OMC1_TSPEC_H2S1_cube.fits'):

    header = fits.getheader(filename)

    with open('outflow_traces_pixels.reg','w') as f:
        print >>f,'global color=white dashlist=8 3 width=1 font="helvetica 14 bold roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1'
        print >>f,'image'
        for ii,(ex,ey) in enumerate(outflow_endpoints):
            print >>f,'line(%i,%i,%i,%i)' % (sourceI[0],sourceI[1],ex,ey)
            print >>f,' # text(%f,%f) text={%i}' % (ex,ey,ii)

    w = wcs.WCS(cubes.flatten_header(header))
    
    with open('outflow_traces_fk5.reg','w') as f:
        print >>f,'global color=white dashlist=8 3 width=1 font="helvetica 14 bold roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1'
        print >>f,'fk5'
        raI,decI = w.wcs_pix2world(np.array([sourceI],dtype='float'),1)[0]
        for ii,(ex,ey) in enumerate(outflow_endpoints):
            ra,dec = w.wcs_pix2world(np.array([[ex,ey]],dtype='float'),1)[0]
            print >>f,'line(%f,%f,%f,%f)' % (raI,decI,ra,dec)
            print >>f,' # text(%f,%f) text={%i}' % (ra,dec,ii)

def do_plots():

    cool = matplotlib.colors.LinearSegmentedColormap('cool',_cool_data)
    cool.set_bad('k')
    hot = matplotlib.cm.hot
    hot.set_bad('k')

    Orion_PVDiagrams(cm=hot,dosave=True,min_valid=1e-15)
    Orion_PVDiagrams('OMC1_TSPEC_H2FeII1.64_cube.fits',linename="FeII 1.64",restwavelength=1.643998*u.um, start_fignum=3, cm=cool, hlcolor='k', min_valid=1e-17)
    Orion_PVDiagrams('OMC1_TSPEC_H2FeII1.60_cube.fits',linename="FeII 1.60",restwavelength=1.599909*u.um, start_fignum=6, cm=cool, hlcolor='k', min_valid=1e-17)
    Orion_PVDiagrams('OMC1_TSPEC_H2BrG_cube.fits',     linename="BrG",      restwavelength=2.1661178*u.um, start_fignum=9, cm=hot, hlcolor='k', min_valid=1e-16)

    for ii in range(9,15):
        restwl = (pyspeckit.models.hydrogen.rrl(4,ii-4)*u.GHz).to(u.um,u.spectral())
        filename = 'OMC1_TSPEC_H2Br%i_cube.fits' % ii
        if os.path.exists(filename):
            Orion_PVDiagrams(filename,linename="Br%i" %
                             ii,restwavelength=restwl, start_fignum=0, cm=hot, hlcolor='k',
                             min_valid=1e-17)

    for h2 in ['Q1','Q2','Q3','Q4','S1','S2','S3','S4','S5','S6']:
        linename = "%s(%s) 1-0" % tuple(h2)
        restwl = linename_to_restwl(linename) * u.um
        filename = 'OMC1_TSPEC_H2%s_cube.fits' % h2
        if os.path.exists(filename):
            Orion_PVDiagrams(filename,linename="H2 %s" % linename,
                             restwavelength=restwl, start_fignum=0, cm=hot, hlcolor='k',
                             min_valid=1e-17)
