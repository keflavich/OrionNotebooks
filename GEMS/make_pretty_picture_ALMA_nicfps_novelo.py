from makepp_support import mask_image,avm
import os
import numpy as np
from astropy.convolution import convolve_fft, Gaussian2DKernel
import PIL
from PIL import ImageEnhance
from astropy.io import fits
from astropy.io import fits as pyfits
import FITS_tools
prefix=""



if 'h2nicfps' not in locals():
    h2f = pyfits.open('/Users/adam/Dropbox/2012_GeMS_OMC1/omc1_h2_041122.fits')
    h2nicfps = h2f[0].data
    h2nicfps[np.isnan(h2nicfps)] = 0
    header = h2f[0].header
#if not 'fe' in locals():
#    fef = pyfits.open('big_mosaic_feii.fits')
#    header = fef[0].header
#    fe = fef[0].data
#    if os.path.exists('big_mosaic_feii_unsharp.fits'):
#        feunsharp = pyfits.getdata('big_mosaic_feii_unsharp.fits')
#        fenormed = pyfits.getdata('big_mosaic_feii_normed.fits')
#    else:
#        #kernel = astropy.nddata.convolution.make_kernel.make_kernel([151,151],kernelwidth=50)
#        #fesmooth = astropy.nddata.convolve(fe,kernel)
#        mimg = mask_image(fe,downsample=4)
#        fesmooth = convolve_fft(mimg, Gaussian2DKernel(250), fft_pad=False,
#                                interpolate_nan=True, psf_pad=False,
#                                ignore_edge_zeros=True, normalize_kernel=True,
#                                use_numpy_fft=True, nthreads=1, use_rfft=True,
#                                complextype=np.float32, silent=False,
#                                boundary='fill')
#        feunsharp = fe
#        for ii in range(4):
#            for jj in range(4):
#                shape = feunsharp[ii::4,jj::4].shape
#                feunsharp[ii::4,jj::4] -= fesmooth[:shape[0],:shape[1]]
#        fef[0].data = feunsharp
#        fef.writeto("big_mosaic_feii_unsharp.fits",clobber=True)
#        fenormed = fe
#        for ii in range(4):
#            for jj in range(4):
#                shape = fenormed[ii::4,jj::4].shape
#                fenormed[ii::4,jj::4] /= fesmooth[:shape[0],:shape[1]]
#        fef[0].data = fenormed
#        fef.writeto("big_mosaic_feii_normed.fits",clobber=True)
    # too big fesmooth = astropy.smooth(fe,100,ignore_nan=True)
    #b2 = pyfits.open('GEMS_B2_Trapezium_mosaic_bgmatch.fits')
    #h2f = pyfits.open('big_mosaic_h2.fits')
    #h2 = h2f[0].data
    #if os.path.exists('big_mosaic_h2_unsharp.fits'):
    #    h2unsharp = pyfits.getdata('big_mosaic_h2_unsharp.fits')
    #    h2normed = pyfits.getdata('big_mosaic_h2_normed.fits')
    #else:
    #    #kernel = astropy.nddata.convolution.make_kernel.make_kernel([151,151],kernelwidth=50)
    #    #h2smooth = astropy.nddata.convolve(h2,kernel)
    #    h2smooth = convolve_fft(mask_image(h2,downsample=4),
    #                            Gaussian2DKernel(250), fft_pad=False,
    #                            interpolate_nan=True, psf_pad=False,
    #                            ignore_edge_zeros=True, normalize_kernel=True,
    #                            use_numpy_fft=True, nthreads=1, use_rfft=True,
    #                            complextype=np.float32, silent=False,
    #                            boundary='fill')
    #    h2unsharp = h2
    #    for ii in range(4):
    #        for jj in range(4):
    #            shape = h2unsharp[ii::4,jj::4].shape
    #            h2unsharp[ii::4,jj::4] -= h2smooth[:shape[0],:shape[1]]
    #    h2f[0].data = h2unsharp
    #    h2f.writeto("big_mosaic_h2_unsharp.fits",clobber=True)
    #    h2normed = h2
    #    for ii in range(4):
    #        for jj in range(4):
    #            shape = h2normed[ii::4,jj::4].shape
    #            h2normed[ii::4,jj::4] /= h2smooth[:shape[0],:shape[1]]
    #    h2f[0].data = h2normed
    #    h2f.writeto("big_mosaic_h2_normed.fits",clobber=True)
    ## too big h2smooth = AG_fft_tools.smooth(h2,100,ignore_nan=True)
    #ks = pyfits.getdata('big_mosaic_ks.fits')
    almared_hdul_nf = fits.open("/Users/adam/work/orion/alma/FITS/Orion_NWSE_12CO2-1_merge_7m_12m_red30to125.max.fits")
    almablue_hdul_nf = fits.open("/Users/adam/work/orion/alma/FITS/Orion_NWSE_12CO2-1_merge_7m_12m_bluem10tom150.max.fits")

    almablue_r_nf = FITS_tools.hcongrid.hcongrid_hdu(almablue_hdul_nf[0], header=header)
    almared_r_nf = FITS_tools.hcongrid.hcongrid_hdu(almared_hdul_nf[0], header=header)

    almablue_nf = almablue_r_nf.data
    almared_nf = almared_r_nf.data


#print "Memory Check (ps): ",get_mem()/1024.**3

import numpy as np

display_cutoff = 0.10
mid_cut = 2.0

# Follow the ds9 definition: y = log(ax+1)/log(a)
# or do this:
#femin = 140; femax=800; fescale=4.0
#h2min = 240; h2max=4000; h2scale=5.0 #1.25
#ksmin = 140; ksmax=1500; ksscale=4.0 #0.86
femin = 1650; femax=5000; fescale=4.0
h2min = 1000; h2max=35000; h2scale=3.0
#h2scale = 2.0 # when feii is excluded
ksmin = 500; ksmax=2500; ksscale=4.0
# for mom0
almabluemin = 0.5; almabluemax = 100; almabluescale = 1.2
almaredmin = 0.5; almaredmax = 100; almaredscale = 1.2
# for max / peak
almabluemin = 0.1; almabluemax = 4.5; almabluescale = 0.9
almaredmin = 0.1; almaredmax = 4.5; almaredscale = 0.8
hamin = 5; hamax=120; hascale=5.0
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

def expscale(arr, exp=2, toint=True, **kwargs):
    linarr = linearize(arr, **kwargs)
    if toint:
        lla = linearize(linarr**exp)*255
        return lla.astype('uint8')
    else:
        return linarr**exp


# myshape=ks.shape
# myslice = slice(None,None,None),slice(None,None,None)
# rgb = np.ones([myshape[0],myshape[1],4],dtype='uint8')
# rgb[:,:,1] = logscale(ks,xmin=ksmin,xmax=ksmax,logexp=ksscale)
# rgb[:,:,0] = logscale(h2,xmin=h2min,xmax=h2max,logexp=h2scale)
# rgb[:,:,2] = logscale(fe,xmin=femin,xmax=femax,logexp=fescale)
# rgb[rgb!=rgb]=0

from matplotlib.colors import rgb_to_hsv,hsv_to_rgb

logii=1

# smallshape = ks[::4,::4].shape
# rgb_float = np.ones([smallshape[0],smallshape[1],3],dtype='float')
# rgb_float[:,:,0] = logscale(ks[::4,::4],xmin=ksmin,xmax=ksmax,logexp=logii,toint=False)
# rgb_float[:,:,1] = logscale(h2[::4,::4],xmin=h2min,xmax=h2max,logexp=logii,toint=False)
# rgb_float[:,:,2] = logscale(fe[::4,::4],xmin=femin,xmax=femax,logexp=logii,toint=False)
# rgb_float[rgb_float!=rgb_float] = 0
# hsv_small = rgb_to_hsv(rgb_float[:,:,:3])


for h2x,fex,almaB_,almaR_,txt in ((h2nicfps,None,almablue_nf,almared_nf,""),): #(h2,fe,ks,""),(h2unsharp,feunsharp,ks,"unsharp_")):

    almaboth_nf = almaB_ + almaR_

    for downsample,size in ((4,'small'),(1,'large')):

        print("Downsample: ",downsample," size: ",size," style: ",txt)
        #print "Memory Check (ps): ",get_mem()/1024.**3

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
        h2_green = np.zeros([shape[0],shape[1],3],dtype='float')
        h2_green[:,:,1] = h2s[:,:,0]
        h2_blue = np.zeros([shape[0],shape[1],3],dtype='float')
        h2_blue[:,:,2] = h2s[:,:,0]
        h2s_hsv = rgb_to_hsv(h2s)
        h2s_hsv[:,:,0] = 40/360.
        #h2s_hsv[:,:,0] = 70/360. # when feii is excluded
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
        #fes = np.zeros([shape[0],shape[1],3],dtype='float')
        #fes[:,:,0] = logscale(fex[::downsample,::downsample],xmin=minv,xmax=maxv,logexp=logii,toint=False)
        #fes_hsv = rgb_to_hsv(fes)
        #fes_hsv[:,:,0] = 210/360.
        #fes_blue = hsv_to_rgb(fes_hsv)

        # square cropping
        yslice,xslice = slice(1100,2600), slice(500,2000)
        yslice,xslice = (slice(int(428/downsample),int(838/downsample)),
                         slice(int(345/downsample),int(745/downsample)))



        almaboth_nf[np.isnan(almaboth_nf)] = 0.0
        almaboth_nf_rgb = np.zeros([shape[0],shape[1],3],dtype='float')
        almaboth_nf_rgb[:,:,0] = logscale(almaboth_nf[::downsample,::downsample],
                                       xmin=almabluemin, xmax=almabluemax,
                                       logexp=almabluescale, toint=False)
        almaboth_nf_red = almaboth_nf_rgb.copy()
        almaboth_nf_hsv = rgb_to_hsv(almaboth_nf_rgb)
        almaboth_nf_hsv[:,:,0] = 340/360.
        almaboth_nf_rgb = hsv_to_rgb(almaboth_nf_hsv)

        #alma_red = alma
        #alma_hsv = rgb_to_hsv(alma)
        #alma_hsv[:,:,0] = 0/360.
        #alma_red = hsv_to_rgb(alma_hsv)

        print("Downsample: ",downsample," size: ",size," style: ",txt)
        #print "Memory Check (ps): ",get_mem()/1024.**3

        # redblueorange = almaB+almaR+h2s_orange#+fes_blue
        redblueorange = almaboth_nf_rgb+h2s_orange+h2_blue
        redblueorange[redblueorange>1] = 1

        redgreenblue = almaboth_nf_red + h2_green + h2_blue
        redgreenblue[redgreenblue>1] = 1

        im = PIL.Image.fromarray((redblueorange*255).astype('uint8')[::-1,:])
        im.save(prefix+'Trapezium_NICFPS_mosaic_redblueorange_ALMA_novelo_%s%s.png' % (txt,size))
        im = ImageEnhance.Contrast(im).enhance(1.5)
        im.save(prefix+'Trapezium_NICFPS_mosaic_redblueorange_ALMA_novelo_%s%s_contrast.png' % (txt,size))
        im = ImageEnhance.Brightness(im).enhance(1.5)
        im.save(prefix+'Trapezium_NICFPS_mosaic_redblueorange_ALMA_novelo_%s%s_contrast_bright.png' % (txt,size))


        im = PIL.Image.fromarray((redgreenblue*255).astype('uint8')[::-1,:])
        im.save(prefix+'Trapezium_NICFPS_mosaic_redgreenblue_ALMA_novelo_%s%s.png' % (txt,size))
        im = ImageEnhance.Contrast(im).enhance(1.5)
        im.save(prefix+'Trapezium_NICFPS_mosaic_redgreenblue_ALMA_novelo_%s%s_contrast.png' % (txt,size))
        im = ImageEnhance.Brightness(im).enhance(1.5)
        im.save(prefix+'Trapezium_NICFPS_mosaic_redgreenblue_ALMA_novelo_%s%s_contrast_bright.png' % (txt,size))



        cropped_im = PIL.Image.fromarray((redblueorange[yslice, xslice]*255).astype('uint8')[::-1,:])
        cropped_im.save(prefix+'cropped_Trapezium_NICFPS_mosaic_redblueorange_ALMA_novelo_%s%s.png' % (txt,size))

        print("Downsample: ",downsample," size: ",size," style: ",txt)
        #print "Memory Check (ps): ",get_mem()/1024.**3

        output = prefix+'Trapezium_NICFPS_mosaic_redblueorange_ALMA_novelo_%s%s.png' % (txt,size)
        avm.embed(output, output)
        output = prefix+'Trapezium_NICFPS_mosaic_redblueorange_ALMA_novelo_%s%s_contrast.png' % (txt,size)
        avm.embed(output, output)
        output = prefix+'Trapezium_NICFPS_mosaic_redblueorange_ALMA_novelo_%s%s_contrast_bright.png' % (txt,size)
        avm.embed(output, output)

        blueorange = h2s_orange#+fes_blue
        blueorange[blueorange>1] = 1
        im1 = PIL.Image.fromarray((blueorange*255).astype('uint8')[::-1,:])
        im1 = ImageEnhance.Contrast(im1).enhance(1.5)
        im1 = ImageEnhance.Brightness(im1).enhance(1.5)
        im = (np.array(im1, dtype='float') + (almaboth_nf_rgb)[::-1,:,:]*256)
        im[im>255] = 255
        im = PIL.Image.fromarray(im.astype('uint8'))
        im.save(prefix+'Trapezium_NICFPS_mosaic_redblueorange_ALMA_novelo_%s%s_contrast_bright2.png' % (txt,size))

        cropped = PIL.Image.fromarray((blueorange[yslice, xslice]*255).astype('uint8')[::-1,:])
        cropped = ImageEnhance.Contrast(cropped).enhance(1.5)
        cropped = ImageEnhance.Brightness(cropped).enhance(1.5)
        cropped = (np.array(cropped, dtype='float') + (almaboth_nf_rgb)[yslice,xslice][::-1,:,:]*256)
        cropped[cropped>255] = 255
        cropped_im = PIL.Image.fromarray(cropped.astype('uint8'))
        cropped_im.save(prefix+'cropped_Trapezium_NICFPS_mosaic_redblueorange_ALMA_novelo_%s%s_contrast_bright2.png' % (txt,size))

#smallshape = ks[::4,::4].shape
#rgb_ha_float = np.ones([smallshape[0],smallshape[1],3],dtype='float')
#rgb_ha_float[:,:,2] = logscale(ha[::4,::4],xmin=hamin,xmax=hamax,logexp=logii,toint=False)
#rgb_ha_float[:,:,0] = logscale(h2[::4,::4],xmin=h2min,xmax=h2max,logexp=logii,toint=False)
#rgb_ha_float[:,:,1] = logscale(fe[::4,::4],xmin=femin,xmax=femax,logexp=logii,toint=False)
#rgb_ha_float[rgb_ha_float!=rgb_ha_float] = 0
#im = PIL.Image.fromarray((rgb_ha_float*255).astype('uint8')[::-1,:])
#im.save(prefix+'TrapeziumHA_GEMS_mosaic_test.png')
##hsv_small = rgb_to_hsv(rgb_ha_float[:,:,:3])


