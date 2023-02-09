
########################################################
# # Started Logging At: 2013-02-02 16:46:26
########################################################
from pylab import *;import numpy,scipy,matplotlib,pyfits;
import image_registration
image_registration.cross_correlation_shifts_FITS('mrgS20130131S0047.fits','mrgS20130131S0048.fits')
help(image_registration.cross_correlation_shifts_FITS)
f = pyfits.open('mrgS20130131S0047.fits')
f
image_registration.cross_correlation_shifts_FITS('mrgS20130131S0047_SCI.fits','mrgS20130131S0048_SCI.fits')
image_registration.cross_correlation_shifts_FITS('mrgS20130131S0049_SCI.fits','mrgS20130131S0048_SCI.fits')
image_registration.FITS_tools.register_fits('mrgS20130131S0049_SCI.fits','mrgS20130131S0048_SCI.fits')
image_registration.FITS_tools.register_fits('mrgS20130131S00%02i_SCI.fits' % ii,'mrgS20130131S0047_SCI.fits')
for ii in xrange(48,53):
    print image_registration.FITS_tools.register_fits('mrgS20130131S00%02i_SCI.fits' % ii,'mrgS20130131S0047_SCI.fits')
    
for ii in [48,49,50,52]:
    shifts = image_registration.FITS_tools.register_fits('mrgS20130131S00%02i_SCI.fits' % ii,'mrgS20130131S0047_SCI.fits')
    crpix1 = pyfits.getheader('mrgS20130131S00%02i_SCI.fits' % ii)['CRPIX1']
    crpix2 = pyfits.getheader('mrgS20130131S00%02i_SCI.fits' % ii)['CRPIX2']
    newcrpix = crpix1 - shifts[0], crpix2 - shifts[1]
    print newcrpix,shifts
    shiftlist.append( (newcrpix,shifts) )
    
shiftlist = []
for ii in [48,49,50,52]:
    shifts = image_registration.FITS_tools.register_fits('mrgS20130131S00%02i_SCI.fits' % ii,'mrgS20130131S0047_SCI.fits')
    crpix1 = pyfits.getheader('mrgS20130131S00%02i_SCI.fits' % ii)['CRPIX1']
    crpix2 = pyfits.getheader('mrgS20130131S00%02i_SCI.fits' % ii)['CRPIX2']
    newcrpix = crpix1 - shifts[0], crpix2 - shifts[1]
    print newcrpix,shifts
    shiftlist.append( (newcrpix,shifts) )
    
shiftlist
for x in shiftlist:
    print 'hedit("blah", CRPIX1, ",x[0][0],")'
    
for x in shiftlist:
    print 'hedit("blah", CRPIX1, ',x[0][0],')'
    
for x in shiftlist:
    print 'hedit("blah", CRPIX1, ',x[0][0],')'
    print 'hedit("blah", CRPIX2, ',x[0][1],')'
    
for ii,x in zip([48,49,50,52],shiftlist):
    print 'hedit("mrgS20130131S00%02i.fits' % ii,", CRPIX1, ',x[0][0],')'
    print 'hedit("mrgS20130131S00%02i.fits' % ii,", CRPIX2, ',x[0][1],')'
    
for ii,x in zip([48,49,50,52],shiftlist):
    print 'hedit("mrgS20130131S00%02i.fits' % ii,', CRPIX1, ',x[0][0],')'
    print 'hedit("mrgS20130131S00%02i.fits' % ii,', CRPIX2, ',x[0][1],')'
    
for ii,x in zip([48,49,50,52],shiftlist):
    print 'hedit("mrgS20130131S00%02i.fits' % ii,', CRPIX1, ',x[0][0],', ver=no)'
    print 'hedit("mrgS20130131S00%02i.fits' % ii,', CRPIX2, ',x[0][1],', ver=no)'
    
hedit("mrgS20130131S0048.fits", CRPIX1,  2102.29218917 , ver=no)
hedit("mrgS20130131S0048.fits", CRPIX2,  2974.35484079 , ver=no)
hedit("mrgS20130131S0049.fits", CRPIX1,  2107.99148106 , ver=no)
hedit("mrgS20130131S0049.fits", CRPIX2,  2966.49542506 , ver=no)
hedit("mrgS20130131S0050.fits", CRPIX1,  2121.19466364 , ver=no)
hedit("mrgS20130131S0050.fits", CRPIX2,  2960.47588239 , ver=no)
hedit("mrgS20130131S0052.fits", CRPIX1,  2112.91756148 , ver=no)
hedit("mrgS20130131S0052.fits", CRPIX2,  2968.31566533 , ver=no)
import astroquery
astroquery.irsa
import astroquery.irsa
get_ipython().magic(u'pinfo astroquery.irsa.query_gator_cone')
astroquery.irsa.print_gator_catalogs()
get_ipython().magic(u'pinfo astroquery.irsa.query_gator_cone')
astroquery.irsa.query_gator_cone('pt_src_cat','OMC 1', 2, units='arcmin')
cat = Out[35]
newtable = atpy.Table()
import atpy
newtable = atpy.Table()
4*2/2.35
sqrt(7000)
import iraf
sys.path.append('/usr/stsci/pyssg/Python-2.7/lib/python2.7/site-packages/')
import iraf
