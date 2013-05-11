#pylint: disable-all
from pylab import *
import os
test=False
if test: prefix="test_"
else: prefix=""
import AG_fft_tools
import agpy
import astropy.nddata
import pyfits
import time
import aplpy
import pyavm
t0 = time.time()

os.chdir('/Volumes/disk4/orion/GEMS_mosaics/')

import pyregion
stars = pyregion.open('ks_NS_catalog.reg')
header = pyfits.getheader('big_mosaic_feii.fits')
wcs=astropy.wcs.WCS(header)
star_coords = np.array([wcs.wcs_world2pix([s.coord_list],0) for s in stars]).squeeze()

avm = pyavm.AVM.from_header(header)

def mask_image(image, star_coords=star_coords, downsample=1, radius=50):
    image = image.copy() # memory expensive, but needed for masking =/
    if downsample != 1:
        image = image[::downsample,::downsample]
    yy,xx = np.indices(image.shape)
    #rr = (xx**2+yy**2)**0.5
    for x,y in star_coords:
        mask = ((xx-x/4.)**2+(yy-y/4.)**2) < (radius/float(downsample))**2
        image[mask] = np.nan

    return image

import PIL,ImageEnhance,ImageOps

if test:
    pilslice = slice(None,None,None)
else:
    pilslice = slice(None,None,None)

if not 'fe' in locals():
    import pyfits
    #FeII_NS_mosaic.fits H2_NS_mosaic.fits   H2_mosaic.fits      KS_mosaic.fits      Ks_NS_mosaic.fits
    # fe_montage_georgs_southeast.fits
    # big_mosaic_h2.fits
    # fe_montage_georgs_southeast.fits
    fef = pyfits.open('big_mosaic_feii.fits')
    fe = fef[0].data
    if os.path.exists('big_mosaic_feii_unsharp.fits'):
        feunsharp = pyfits.getdata('big_mosaic_feii_unsharp.fits')
        fenormed = pyfits.getdata('big_mosaic_feii_normed.fits')
    else:
        #kernel = astropy.nddata.convolution.make_kernel.make_kernel([151,151],kernelwidth=50)
        #fesmooth = astropy.nddata.convolve(fe,kernel)
        fesmooth = agpy.smooth(mask_image(fe,downsample=4),250, fft_pad=False,
                interpolate_nan=True, psf_pad=False, ignore_edge_zeros=True,
                normalize_kernel=True, use_numpy_fft=True, nthreads=1,
                use_rfft=True, complextype=np.float32, silent=False,
                boundary='wrap')
        feunsharp = fe
        for ii in xrange(4):
            for jj in xrange(4):
                shape = feunsharp[ii::4,jj::4].shape
                feunsharp[ii::4,jj::4] -= fesmooth[:shape[0],:shape[1]]
        fef[0].data = feunsharp
        fef.writeto("big_mosaic_feii_unsharp.fits",clobber=True)
        fenormed = fe
        for ii in xrange(4):
            for jj in xrange(4):
                shape = fenormed[ii::4,jj::4].shape
                fenormed[ii::4,jj::4] /= fesmooth[:shape[0],:shape[1]]
        fef[0].data = fenormed
        fef.writeto("big_mosaic_feii_normed.fits",clobber=True)
    # too big fesmooth = astropy.smooth(fe,100,ignore_nan=True)
    #b2 = pyfits.open('GEMS_B2_Trapezium_mosaic_bgmatch.fits')
    h2f = pyfits.open('big_mosaic_h2.fits')
    h2 = h2f[0].data
    if os.path.exists('big_mosaic_h2_unsharp.fits'):
        h2unsharp = pyfits.getdata('big_mosaic_h2_unsharp.fits')
        h2normed = pyfits.getdata('big_mosaic_h2_normed.fits')
    else:
        #kernel = astropy.nddata.convolution.make_kernel.make_kernel([151,151],kernelwidth=50)
        #h2smooth = astropy.nddata.convolve(h2,kernel)
        h2smooth = agpy.smooth(mask_image(h2,downsample=4),250, fft_pad=False,
                interpolate_nan=True, psf_pad=False, ignore_edge_zeros=True,
                normalize_kernel=True, use_numpy_fft=True, nthreads=1,
                use_rfft=True, complextype=np.float32, silent=False,
                boundary='wrap')
        h2unsharp = h2
        for ii in xrange(4):
            for jj in xrange(4):
                shape = h2unsharp[ii::4,jj::4].shape
                h2unsharp[ii::4,jj::4] -= h2smooth[:shape[0],:shape[1]]
        h2f[0].data = h2unsharp
        h2f.writeto("big_mosaic_h2_unsharp.fits",clobber=True)
        h2normed = h2
        for ii in xrange(4):
            for jj in xrange(4):
                shape = h2normed[ii::4,jj::4].shape
                h2normed[ii::4,jj::4] /= h2smooth[:shape[0],:shape[1]]
        h2f[0].data = h2normed
        h2f.writeto("big_mosaic_h2_normed.fits",clobber=True)
    # too big h2smooth = AG_fft_tools.smooth(h2,100,ignore_nan=True)
    ks = pyfits.getdata('big_mosaic_ks.fits')

import resource
from guppy import hpy
heapy = hpy()
print "Memory check: ",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.**3
memtot = heapy.heap().size / 1024.0**3
print "Memory check (guppy): ",memtot,'GB'

import numpy as np
import copy
import matplotlib

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


#myshape = (2700,7200)
myshape=ks.shape
myslice = slice(None,None,None),slice(None,None,None)
rgb = np.ones([myshape[0],myshape[1],4],dtype='uint8')
rgb[:,:,1] = logscale(ks,xmin=ksmin,xmax=ksmax,logexp=ksscale)
rgb[:,:,0] = logscale(h2,xmin=h2min,xmax=h2max,logexp=h2scale)
rgb[:,:,2] = logscale(fe,xmin=femin,xmax=femax,logexp=fescale)
#rgb[:,:,1] = (np.log10((h2[0].data[myslice]-h2min)/h2max*10**h2scale+1))/h2scale; rgb[:,:,1][rgb[:,:,1]<0] = 0; rgb[:,:,1][rgb[:,:,1]>1] = 1
#rgb[:,:,2] = (np.log10((b2[0].data[myslice]-b2min)/b2max*10**b2scale+1))/b2scale; rgb[:,:,2][rgb[:,:,2]<0] = 0; rgb[:,:,2][rgb[:,:,2]>1] = 1
#rgb[:,:,2] = (np.log10((fe[0].data[myslice]-femin)/femax*10**fescale+1))/fescale; rgb[:,:,2][rgb[:,:,2]<0] = 0; rgb[:,:,2][rgb[:,:,2]>1] = 1
rgb[rgb!=rgb]=0

# for logii in xrange(0,2):
#     print "Making small image %i.  t=%0.1f s" % (logii,time.time()-t0)
#     rgb_small = np.ones([myshape[0]/4,myshape[1]/4,4],dtype='uint8')
#     rgb_small[:,:,0] = logscale(ks[::4,::4],xmin=ksmin,xmax=ksmax,logexp=logii)
#     rgb_small[:,:,1] = logscale(h2[::4,::4],xmin=h2min,xmax=h2max,logexp=logii)
#     rgb_small[:,:,2] = logscale(fe[::4,::4],xmin=femin,xmax=femax,logexp=logii)
#     rgb_small[:,:,3] = 255
#     rgb_small_pil = rgb_small[::-1,:,:] # reverse y axis because PIL is backwards
#     #rgb_small_pil[np.max(rgb_small_pil,axis=2)>=255,:] = 255
#     #rgb_small_pil[:,:,3] = np.uint8(256)-rgb_small_pil[:,:,3]
#     im = PIL.Image.fromarray(rgb_small_pil)
#     print "Saving GEMS mosaic ",time.time()-t0
#     im.save(prefix+'Trapezium_GEMS_mosaic_logexp%ii_small.png' % logii)
#     print "Fin small image %i.  t=%0.1f s" % (logii,time.time()-t0)
# 
#     kbackground = PIL.Image.new("RGB", im.size, (0, 0, 0))
#     kbackground.paste(im, mask=im.split()[3])
#     print "Saving GEMS mosaic with black bg ",time.time()-t0
#     #kbackground.save(prefix+'Trapezium_GEMS_mosaic_logexp%ii_blackbg_small.png' % (logii))
#     kbackground_contrast = ImageEnhance.Contrast(kbackground).enhance(1.5)
#     kbackground_contrast.save(prefix+'Trapezium_GEMS_mosaic_logexp%ii_blackbg_contrast_small.png' % (logii))
#     kbackground_bright = ImageEnhance.Brightness(kbackground_contrast).enhance(1.5)
#     kbackground_bright.save(prefix+'Trapezium_GEMS_mosaic_logexp%ii_blackbg_contrast_bright_small.png' % (logii))
# 
# for logii in xrange(0,2):
#     print "Making large image %i.  t=%0.1f s" % (logii,time.time()-t0)
#     rgb_large = np.ones([myshape[0],myshape[1],4],dtype='uint8')
#     rgb_large[:,:,1] = logscale(ks,xmin=ksmin,xmax=ksmax,logexp=logii)
#     rgb_large[:,:,0] = logscale(h2,xmin=h2min,xmax=h2max,logexp=logii)
#     rgb_large[:,:,2] = logscale(fe,xmin=femin,xmax=femax,logexp=logii)
#     rgb_large[:,:,3] = 255
#     rgb_large_pil = rgb_large[::-1,:,:] # reverse y axis because PIL is backwards
#     #rgb_large_pil[np.max(rgb_large_pil,axis=2)>=255,:] = 255
#     #rgb_large_pil[:,:,3] = np.uint8(256)-rgb_large_pil[:,:,3]
#     im = PIL.Image.fromarray(rgb_large_pil)
#     print "Saving GEMS mosaic ",time.time()-t0
#     im.save(prefix+'Trapezium_GEMS_mosaic_logexp%ii_large.png' % logii)
#     print "Fin large image %i.  t=%0.1f s" % (logii,time.time()-t0)
# 
#     kbackground = PIL.Image.new("RGB", im.size, (0, 0, 0))
#     kbackground.paste(im, mask=im.split()[3])
#     print "Saving GEMS mosaic with black bg ",time.time()-t0
#     #kbackground.save(prefix+'Trapezium_GEMS_mosaic_logexp%ii_blackbg_large.png' % (logii))
#     kbackground_contrast = ImageEnhance.Contrast(kbackground).enhance(1.5)
#     kbackground_contrast.save(prefix+'Trapezium_GEMS_mosaic_logexp%ii_blackbg_contrast_large.png' % (logii))
#     kbackground_bright = ImageEnhance.Brightness(kbackground_contrast).enhance(1.5)
#     kbackground_bright.save(prefix+'Trapezium_GEMS_mosaic_logexp%ii_blackbg_contrast_bright_large.png' % (logii))
# rgb_eq_lg = skimage.exposure.equalize(rgb_large_pil)
# rgb_eq_sm = skimage.exposure.equalize(rgb_small_pil)
# 
# imlg = PIL.Image.fromarray((rgb_eq_lg*255).astype('uint8'))
# im.save(prefix+'Trapezium_GEMS_mosaic_eq_large.png')
# imsm = PIL.Image.fromarray((rgb_eq_sm*255).astype('uint8'))
# im.save(prefix+'Trapezium_GEMS_mosaic_eq_small.png')



import skimage
import skimage.exposure
import skimage.color
from matplotlib.colors import rgb_to_hsv,hsv_to_rgb

logii=1

smallshape = ks[::4,::4].shape
rgb_float = np.ones([smallshape[0],smallshape[1],3],dtype='float')
rgb_float[:,:,0] = logscale(ks[::4,::4],xmin=ksmin,xmax=ksmax,logexp=logii,toint=False)
rgb_float[:,:,1] = logscale(h2[::4,::4],xmin=h2min,xmax=h2max,logexp=logii,toint=False)
rgb_float[:,:,2] = logscale(fe[::4,::4],xmin=femin,xmax=femax,logexp=logii,toint=False)
rgb_float[rgb_float!=rgb_float] = 0
hsv_small = rgb_to_hsv(rgb_float[:,:,:3])
#for hue in linspace(0,330,12):
#    print "making small image %i with hue %i.  t=%0.1f s" % (logii,hue,time.time()-t0)
#    rot_small = hsv_small.copy()
#    rot_small[:,:,0] += hue/360.
#    rot_small[:,:,0] %= 1
#    rgb_float_rot = hsv_to_rgb(rot_small)
#    rgb_float_pil = (255*rgb_float_rot[::-1,:,:]).astype('uint8') # reverse y axis because pil is backwards
#    #rgb_float_pil[np.max(rgb_float_pil,axis=2)>=255,:] = 255
#    #rgb_float_pil[:,:,3] = np.uint8(256)-rgb_float_pil[:,:,3]
#    im = PIL.Image.fromarray(rgb_float_pil)
#    print "saving gems mosaic ",time.time()-t0
#    im.save(prefix+'Trapezium_gems_mosaic_logexp%i_hue%i_small.png' % (logii,hue))
#    print "fin small image %i.  t=%0.1f s" % (logii,time.time()-t0)
#
#    print "saving gems mosaic with black bg ",time.time()-t0
#    #kbackground.save(prefix+'Trapezium_gems_mosaic_logexp%ii_blackbg_small.png' % (logii))
#    kbackground_contrast = ImageEnhance.Contrast(im).enhance(1.5)
#    kbackground_contrast.save(prefix+'Trapezium_gems_mosaic_logexp%i_hue%i_blackbg_contrast_small.png' % (logii,hue))
#    kbackground_bright = ImageEnhance.Brightness(kbackground_contrast).enhance(1.5)
#    kbackground_bright.save(prefix+'Trapezium_gems_mosaic_logexp%i_hue%i_blackbg_contrast_bright_small.png' % (logii,hue))

logii=1

#rgb_float = np.ones([myshape[0]/4,myshape[1]/4,3],dtype='float')
#rgb_float[:,:,0] = logscale(ks[::4,::4],xmin=ksmin,xmax=ksmax,logexp=logii,toint=False)
#rgb_float[:,:,2] = logscale(h2[::4,::4],xmin=h2min,xmax=h2max,logexp=logii,toint=False)
#rgb_float[:,:,1] = logscale(fe[::4,::4],xmin=femin,xmax=femax,logexp=logii,toint=False)
#rgb_float[rgb_float!=rgb_float] = 0
#hsv_small = rgb_to_hsv(rgb_float[:,:,:3])
#for hue in linspace(0,300,6):
#    print "Making rgswap_small image %i with hue %i.  t=%0.1f s" % (logii,hue,time.time()-t0)
#    rot_rgswap_small = hsv_small.copy()
#    rot_rgswap_small[:,:,0] += hue/360.
#    rot_rgswap_small[:,:,0] %= 1
#    rgb_float_rot = hsv_to_rgb(rot_rgswap_small)
#    rgb_float_pil = (255*rgb_float_rot[::-1,:,:]).astype('uint8') # reverse y axis because PIL is backwards
#    #rgb_float_pil[np.max(rgb_float_pil,axis=2)>=255,:] = 255
#    #rgb_float_pil[:,:,3] = np.uint8(256)-rgb_float_pil[:,:,3]
#    im = PIL.Image.fromarray(rgb_float_pil)
#    print "Saving GEMS mosaic ",time.time()-t0
#    im.save(prefix+'Trapezium_GEMS_mosaic_logexp%i_hue%i_rgswap_small.png' % (logii,hue))
#    print "Fin rgswap_small image %i.  t=%0.1f s" % (logii,time.time()-t0)
#
#    print "Saving GEMS mosaic with black bg ",time.time()-t0
#    #kbackground.save(prefix+'Trapezium_GEMS_mosaic_logexp%ii_blackbg_rgswap_small.png' % (logii))
#    kbackground_contrast = ImageEnhance.Contrast(im).enhance(1.5)
#    kbackground_contrast.save(prefix+'Trapezium_GEMS_mosaic_logexp%i_hue%i_blackbg_contrast_rgswap_small.png' % (logii,hue))
#    kbackground_bright = ImageEnhance.Brightness(kbackground_contrast).enhance(1.5)
#    kbackground_bright.save(prefix+'Trapezium_GEMS_mosaic_logexp%i_hue%i_blackbg_contrast_bright_rgswap_small.png' % (logii,hue))

for h2x,fex,ksx,txt in ((h2normed,fenormed,ks,"normed_"),(h2,fe,ks,""),(h2unsharp,feunsharp,ks,"unsharp_")):
    for downsample,size in ((4,'small'),(1,'large')):

        print "Downsample: ",downsample," size: ",size," style: ",txt
        print "Memory check: ",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.**3
        memtot = heapy.heap().size / 1024.0**3
        print "Memory check (guppy): ",memtot,'GB'

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
        h2s_orange = hsv_to_rgb(h2s_hsv)

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
        fes_blue = hsv_to_rgb(fes_hsv)

        kss = np.zeros([shape[0],shape[1],3],dtype='float')
        kss[:,:,0] = logscale(ksx[::downsample,::downsample],xmin=ksmin,xmax=ksmax,logexp=logii,toint=False)
        kss_red = kss
        #kss_hsv = rgb_to_hsv(kss)
        #kss_hsv[:,:,0] = 0/360.
        #kss_red = hsv_to_rgb(kss_hsv)

        print "Downsample: ",downsample," size: ",size," style: ",txt
        print "Memory check: ",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.**3
        memtot = heapy.heap().size / 1024.0**3
        print "Memory check (guppy): ",memtot,'GB'

        redblueorange = kss_red+h2s_orange+fes_blue
        redblueorange[redblueorange>1] = 1
        im = PIL.Image.fromarray((redblueorange*255).astype('uint8')[::-1,:])
        im.save(prefix+'Trapezium_GEMS_mosaic_redblueorange_%s%s.png' % (txt,size))
        im = ImageEnhance.Contrast(im).enhance(1.5)
        im.save(prefix+'Trapezium_GEMS_mosaic_redblueorange_%s%s_contrast.png' % (txt,size))
        im = ImageEnhance.Brightness(im).enhance(1.5)
        im.save(prefix+'Trapezium_GEMS_mosaic_redblueorange_%s%s_contrast_bright.png' % (txt,size))

        output = prefix+'Trapezium_GEMS_mosaic_redblueorange_%s%s.png' % (txt,size)
        avm.embed(output, output)
        output = prefix+'Trapezium_GEMS_mosaic_redblueorange_%s%s_contrast.png' % (txt,size)
        avm.embed(output, output)
        output = prefix+'Trapezium_GEMS_mosaic_redblueorange_%s%s_contrast_bright.png' % (txt,size)
        avm.embed(output, output)

raise ValueError("Done")

print "Creating scaling ",time.time()-t0
autumn_transparent = copy.copy(matplotlib.cm.autumn)
#autumn_transparent._lut = matplotlib.cm.autumn(np.linspace(0.4,1.0,autumn_transparent.N+3))
autumn_transparent._lut = matplotlib.cm.Oranges_r(np.linspace(0.2,0.8,autumn_transparent.N+3))
autumn_transparent._lut[:,1] *= 1.5
autumn_transparent._lut[autumn_transparent._lut[:,1]>1,1] = 1
autumn_transparent._isinit=True
#autumn_transparent._lut = matplotlib.cm.autumn_r(np.linspace(0.0,0.7,autumn_transparent.N+3))
#autumn_transparent._lut[:,2] *= 0.1
autumn_transparent._lut[:,3] *= np.sin(np.linspace(0.1,0.8,autumn_transparent.N+3)*pi/2)**2
autumn_transparent._lut[256,:] = 0
autumn_transparent._lut[257,:] = autumn_transparent._lut[255,:]
autumn_transparent._lut[258,:] = 0
#autumn_transparent._lut *= np.outer(np.linspace(0.1,1,autumn_transparent.N),np.ones(4))

high_lut = {
        'red':[(0,autumn_transparent(1-1e-5)[0],autumn_transparent(1-1e-5)[0]),(1,1,1)],
        'green':[(0,autumn_transparent(1-1e-5)[1],autumn_transparent(1-1e-5)[1]),(1,0.5,0.5)],
        'blue':[(0,autumn_transparent(1-1e-5)[2],autumn_transparent(1-1e-5)[2]),(1,0,0)],
        }
high = matplotlib.colors.LinearSegmentedColormap('high',high_lut)
high._lut = high(np.linspace(0,1,high.N))
high._lut[:,3] = np.linspace(0.8,1.0,high.N)

rgb[:,:,3] = rgb[:,:,:3].mean(axis=2)


# print "Creating scaled image ",time.time()-t0
# v2img = autumn_transparent(v2resmooth)
# v2img = autumn_transparent(v2mid)*(v2mid>1e-6)[:,:,newaxis]+high(v2high)*((v2mid<=1e-6)*(v2high>1e-6))[:,:,newaxis]
# #v2img = autumn_transparent((v2scaled-np.log10(display_cutoff))/(np.nanmax(v2scaled)-np.log10(display_cutoff)))
# #print autumn_transparent._lut[:,3], autumn_transparent._isinit
# if v2img.sum() == float(v2img.shape[0])**2: raise
# #v2img = autumn_transparent((v2scaled-np.nanmin(v2scaled))/(np.nanmax(v2scaled)-np.nanmin(v2scaled)))
# #v2img[:,:,:3] = v2img[:,:,:3]*(v2img[:,:,3][:,:,np.newaxis])**0.25
# rgb2 = rgb.copy()
# # reduce blueness...
# # rgb2[:,:,2] -= v2img[:,:,:2].mean(axis=2)
# #rgb2[v2scaled>log10(display_cutoff),:] += v2img[v2scaled>log10(display_cutoff),:] 
# #rgb2[v2scaled>log10(display_cutoff),:3] *= np.min( np.concatenate([[v2img[:,:,:3]/ (v2img[:,:,3][:,:,np.newaxis])**0.5], [np.ones(v2img.shape[:2]+(3,))]]), axis=0 )[v2scaled>log10(display_cutoff)] 
# #rgb2[v2scaled>log10(display_cutoff),3] += (v2img[v2scaled>log10(display_cutoff),3])**2.0
# colorscale = np.nanmin( np.concatenate([[v2img[:,:,:3]/ (v2img[:,:,3][:,:,newaxis])**1.0], [np.ones(v2img.shape[:2]+(3,))]]), axis=0 )
# rgb2[:,:,:2] *= colorscale[:,:,:2]
# rgb2[:,:,2] *= colorscale[:,:,2] + colorscale[:,:,2]==0
# rgb2[:,:,3] += (v2img[:,:,3])**2.0
# rgb2[rgb2>1] = 1
# 

print "Beginning PIL operations ",time.time()-t0
import PIL,ImageEnhance,ImageOps
rgb_pil = rgb[pilslice,:,:]
rgb_pil = rgb_pil[::-1,:,:]
#rgb_pil[np.max(rgb_pil,axis=2)>=255,:] = 255
#rgb_pil[:,:,3] = np.uint8(256)-rgb_pil[:,:,3]
im1 = PIL.Image.fromarray(rgb_pil)
print "Saving GEMS mosaic ",time.time()-t0
im1.save(prefix+'Trapezium_GEMS_mosaic.png')
#rgb_pil = ((1-rgb[:,:,:3])*(2**8))
#rgb_pil -= (256*rgb[:,:,3])[:,:,newaxis]
#rgb_pil[rgb_pil>255] = 255
#rgb_pil = rgb_pil.astype('uint8')
#im1 = PIL.Image.fromarray(rgb_pil)
#im1.save(prefix+'Trapezium_GEMS_mosaic_try2.png')
print "Saving GEMS mosaic with white bg ",time.time()-t0
wbackground = PIL.Image.new("RGB", im1.size, (255, 255, 255))
wbackground.paste(im1, mask=im1.split()[3])
wbackground.save(prefix+'Trapezium_GEMS_mosaic_whitebg.png')
kbackground = PIL.Image.new("RGB", im1.size, (0, 0, 0))
kbackground.paste(im1, mask=im1.split()[3])
print "Saving GEMS mosaic with black bg ",time.time()-t0
kbackground.save(prefix+'Trapezium_GEMS_mosaic_blackbg.png')
kbackground_contrast = ImageOps.autocontrast(kbackground)
kbackground_contrast.save(prefix+'Trapezium_GEMS_mosaic_blackbg_contrast.png')
kbackground_bright = ImageEnhance.Brightness(kbackground_contrast).enhance(1.5)
kbackground_bright.save(prefix+'Trapezium_GEMS_mosaic_blackbg_contrast_bright.png')

#print "doing Bolocam PIL stuff ",time.time()-t0
#v2pil = (v2img*255).astype('uint8')[pilslice,:,:]
#v2pil = v2pil[::-1,:,:]
#boloim = PIL.Image.fromarray(v2pil)
#boloim.save(prefix+'Trapezium_bolo.png')
#kbackground.paste(boloim, mask=boloim.split()[3])
#print "Saving Bolocam + GEMS mosaic with black bg (PIL) ",time.time()-t0
#kbackground.save(prefix+'Trapezium_GEMS_bolo_mosaic_blackbg.png')

print "Done ",time.time()-t0

rotated = rgb_pil.copy()
rotated[:,:,0] = rgb_pil[:,:,2]
rotated[:,:,1] = rgb_pil[:,:,0]
rotated[:,:,2] = rgb_pil[:,:,1]
im2 = PIL.Image.fromarray(rotated)
print "Saving GEMS mosaic ",time.time()-t0
im2.save(prefix+'Trapezium_GEMS_mosaic_rotated.png')
kbackground2 = PIL.Image.new("RGB", im2.size, (0, 0, 0))
kbackground2.paste(im2, mask=im2.split()[3])
print "Saving GEMS mosaic with black bg ",time.time()-t0
kbackground2.save(prefix+'Trapezium_GEMS_mosaic_rotated_blackbg.png')
kbackground2_small = kbackground2.resize([s/4 for s in kbackground2.size])
kbackground2_small.save(prefix+'Trapezium_GEMS_mosaic_rotated_blackbg_small.png',quality=10)
print "Saving Bolocam + GEMS mosaic with black bg (PIL) ",time.time()-t0
kbackground2_contrast = ImageOps.autocontrast(kbackground2)
kbackground2_contrast.save(prefix+'Trapezium_GEMS_mosaic_rotated_blackbg_contrast.png')
kbackground2_bright = ImageEnhance.Brightness(kbackground2_contrast).enhance(1.5)
kbackground2_bright.save(prefix+'Trapezium_GEMS_mosaic_rotated_blackbg_contrast_bright.png')
kbackground2_small_bright = kbackground2_bright.resize([s/4 for s in kbackground2.size])
kbackground2_small_bright.save(prefix+'Trapezium_GEMS_mosaic_rotated_blackbg_bright_small.png',quality=10)
#kbackground2_bright.paste(boloim, mask=boloim.split()[3])
kbackground2_bright.save(prefix+'Trapezium_GEMS_bolo_mosaic_rotated_blackbg.png')
kbackground2_small = kbackground2_bright.resize([s/4 for s in kbackground2.size])
kbackground2_small.save(prefix+'Trapezium_GEMS_bolo_mosaic_rotated_blackbg_small.png',quality=10)
print "Done rotated ",time.time()-t0
