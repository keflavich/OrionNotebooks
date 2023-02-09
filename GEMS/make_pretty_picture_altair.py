from makepp_support import mask_image,avm,get_mem
import os
import agpy
import numpy as np
import PIL,ImageEnhance
prefix=""

if not 'fe' in locals():
    import pyfits
    #fe_NS_mosaic.fits H2_NS_mosaic.fits   H2_mosaic.fits      KS_mosaic.fits      Ks_NS_mosaic.fits
    # fe_montage_georgs_southeast.fits
    # altair_big_h2.fits
    # fe_montage_georgs_southeast.fits
    fef = pyfits.open('altair_big_fe.fits')
    fe = fef[0].data
    if os.path.exists('altair_big_fe_unsharp.fits'):
        feunsharp = pyfits.getdata('altair_big_fe_unsharp.fits')
        fenormed = pyfits.getdata('altair_big_fe_normed.fits')
    else:
        #kernel = astropy.nddata.convolution.make_kernel.make_kernel([151,151],kernelwidth=50)
        #fesmooth = astropy.nddata.convolve(fe,kernel)
        fesmooth = agpy.smooth(mask_image(fe,downsample=4),250, fft_pad=False,
                interpolate_nan=True, psf_pad=False, ignore_edge_zeros=True,
                normalize_kernel=True, use_numpy_fft=True, nthreads=1,
                use_rfft=True, complextype=np.float32, silent=False,
                boundary='fill')
        feunsharp = fe
        for ii in xrange(4):
            for jj in xrange(4):
                shape = feunsharp[ii::4,jj::4].shape
                feunsharp[ii::4,jj::4] -= fesmooth[:shape[0],:shape[1]]
        fef[0].data = feunsharp
        fef.writeto("altair_big_fe_unsharp.fits",clobber=True)
        fenormed = fe
        for ii in xrange(4):
            for jj in xrange(4):
                shape = fenormed[ii::4,jj::4].shape
                fenormed[ii::4,jj::4] /= fesmooth[:shape[0],:shape[1]]
        fef[0].data = fenormed
        fef.writeto("altair_big_fe_normed.fits",clobber=True)
    # too big fesmooth = astropy.smooth(fe,100,ignore_nan=True)
    #b2 = pyfits.open('GEMS_B2_AltairTrapezium_mosaic_bgmatch.fits')
    h2f = pyfits.open('altair_big_h2.fits')
    h2 = h2f[0].data
    if os.path.exists('altair_big_h2_unsharp.fits'):
        h2unsharp = pyfits.getdata('altair_big_h2_unsharp.fits')
        h2normed = pyfits.getdata('altair_big_h2_normed.fits')
    else:
        #kernel = astropy.nddata.convolution.make_kernel.make_kernel([151,151],kernelwidth=50)
        #h2smooth = astropy.nddata.convolve(h2,kernel)
        h2smooth = agpy.smooth(mask_image(h2,downsample=4),250, fft_pad=False,
                interpolate_nan=True, psf_pad=False, ignore_edge_zeros=True,
                normalize_kernel=True, use_numpy_fft=True, nthreads=1,
                use_rfft=True, complextype=np.float32, silent=False,
                boundary='fill')
        h2unsharp = h2
        for ii in xrange(4):
            for jj in xrange(4):
                shape = h2unsharp[ii::4,jj::4].shape
                h2unsharp[ii::4,jj::4] -= h2smooth[:shape[0],:shape[1]]
        h2f[0].data = h2unsharp
        h2f.writeto("altair_big_h2_unsharp.fits",clobber=True)
        h2normed = h2
        for ii in xrange(4):
            for jj in xrange(4):
                shape = h2normed[ii::4,jj::4].shape
                h2normed[ii::4,jj::4] /= h2smooth[:shape[0],:shape[1]]
        h2f[0].data = h2normed
        h2f.writeto("altair_big_h2_normed.fits",clobber=True)
    # too big h2smooth = AG_fft_tools.smooth(h2,100,ignore_nan=True)
    ks = pyfits.getdata('altair_big_ks.fits')

import resource
from guppy import hpy
heapy = hpy()
print "Memory check: ",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.**3
memtot = heapy.heap().size / 1024.0**3
print "Memory check (guppy): ",memtot,'GB'
print "Memory Check (ps): ",get_mem()/1024.**3

import numpy as np

display_cutoff = 0.10
mid_cut = 2.0

# Follow the ds9 definition: y = log(ax+1)/log(a) 
# or do this: 
#femin = 140; femax=800; fescale=4.0
#h2min = 240; h2max=4000; h2scale=5.0 #1.25
#ksmin = 140; ksmax=1500; ksscale=4.0 #0.86
femin = 1650; femax=5000; fescale=4.0
h2min = 2150; h2max=10000; h2scale=4.0
ksmin = 500; ksmax=2500; ksscale=4.0
def linearize(x, xmin=None, xmax=None, truncate=True):
    if np.isscalar(x):
        return x
    else:
        if xmin is None:
            xmin = np.nanmin(x)
        if xmax is None:
            xmax = np.nanmax(x)
        if truncate:
            x = np.copy(x)
            x[x<xmin] = xmin
            x[x>xmax] = xmax
        return ((x-xmin)/(xmax-xmin))

def logscale(arr, logexp=3.0, toint=True, **kwargs):
    linarr = linearize(arr, **kwargs)
    if logexp is None:
        logarr = linarr
    else:
        logarr = np.log10(linarr * 10**logexp + 1)
    if toint:
        lla = linearize(logarr)*255
        return lla.astype('uint8')
    else:
        return logarr

logii=1
from matplotlib.colors import rgb_to_hsv,hsv_to_rgb

for h2x,fex,ksx,txt in ((h2normed,fenormed,ks,"normed_"),(h2,fe,ks,""),(h2unsharp,feunsharp,ks,"unsharp_")):
    for downsample,size in ((4,'small'),(1,'large')):

        print "Downsample: ",downsample," size: ",size," style: ",txt
        print "Memory check: ",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.**3
        memtot = heapy.heap().size / 1024.0**3
        print "Memory check (guppy): ",memtot,'GB'
        print "Memory Check (ps): ",get_mem()/1024.**3

        shape = h2x[::downsample,::downsample].shape
        h2s = np.zeros([shape[0],shape[1],3],dtype='float')
        if txt == "normed_":
            minv = -0.15
            maxv = 1
            logii = None
        elif txt is not '':
            minv = -250 #-20
            maxv = 1250 #h2max
            logii = 1
        else:
            minv = h2min
            maxv = h2max
            logii = 1
        h2s[:,:,0] = logscale(h2x[::downsample,::downsample],xmin=minv,xmax=maxv,logexp=logii,toint=False)
        h2s_hsv = rgb_to_hsv(h2s)
        h2s_hsv[:,:,0] = 30/360.
        h2s_orange = np.nan_to_num(hsv_to_rgb(h2s_hsv))

        if txt == "normed_":
            minv = -0.15
            maxv = 1.0
            logii = None
        elif txt is not '':
            minv = -300#-20
            maxv =  300#femax
            logii = 1
        else:
            minv = femin
            maxv = femax
            logii = 1
        fes = np.zeros([shape[0],shape[1],3],dtype='float')
        fes[:,:,0] = logscale(fex[::downsample,::downsample],xmin=minv,xmax=maxv,logexp=logii,toint=False)
        fes_hsv = rgb_to_hsv(fes)
        fes_hsv[:,:,0] = 210/360.
        fes_blue = np.nan_to_num(hsv_to_rgb(fes_hsv))

        kss = np.zeros([shape[0],shape[1],3],dtype='float')
        kss[:,:,0] = logscale(ksx[::downsample,::downsample],xmin=ksmin,xmax=ksmax,logexp=logii,toint=False)
        kss_red = np.nan_to_num(kss)
        #kss_hsv = rgb_to_hsv(kss)
        #kss_hsv[:,:,0] = 0/360.
        #kss_red = hsv_to_rgb(kss_hsv)

        print "Downsample: ",downsample," size: ",size," style: ",txt
        print "Memory check: ",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.**3
        memtot = heapy.heap().size / 1024.0**3
        print "Memory check (guppy): ",memtot,'GB'
        print "Memory Check (ps): ",get_mem()/1024.**3

        redblueorange = kss_red+h2s_orange+fes_blue
        redblueorange[redblueorange>1] = 1
        im = PIL.Image.fromarray((redblueorange*255).astype('uint8')[::-1,:])
        im.save(prefix+'AltairTrapezium_GEMS_mosaic_redblueorange_%s%s.png' % (txt,size))
        im = ImageEnhance.Contrast(im).enhance(1.5)
        im.save(prefix+'AltairTrapezium_GEMS_mosaic_redblueorange_%s%s_contrast.png' % (txt,size))
        im = ImageEnhance.Brightness(im).enhance(1.5)
        im.save(prefix+'AltairTrapezium_GEMS_mosaic_redblueorange_%s%s_contrast_bright.png' % (txt,size))

        print "(prior to avm embedding) Downsample: ",downsample," size: ",size," style: ",txt
        print "Memory check: ",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.**3
        memtot = heapy.heap().size / 1024.0**3
        print "Memory check (guppy): ",memtot,'GB'
        print "Memory Check (ps): ",get_mem()/1024.**3

        output = prefix+'AltairTrapezium_GEMS_mosaic_redblueorange_%s%s.png' % (txt,size)
        avm.embed(output, output)
        output = prefix+'AltairTrapezium_GEMS_mosaic_redblueorange_%s%s_contrast.png' % (txt,size)
        avm.embed(output, output)
        output = prefix+'AltairTrapezium_GEMS_mosaic_redblueorange_%s%s_contrast_bright.png' % (txt,size)
        avm.embed(output, output)

raise ValueError("Done")
