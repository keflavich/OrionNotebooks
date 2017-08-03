import os

vis = [
"calibrated_X360.ms/",
"uid___A002_X86dcae_X416.ms.split.cal/",
"uid___A002_X872bbc_X412.ms.split.cal/",
"uid___A002_X872bbc_X7c.ms.split.cal/",
"uid___A002_X87436c_Xb7a.ms.split.cal/",
"uid___A002_X87c075_X1066.ms.split.cal/",
"uid___A002_X960614_X39db.ms.split.cal/",
"uid___A002_X9630c0_Xc26.ms.split.cal/",
"uid___A002_X966cea_X14a4.ms.split.cal/",
"uid___A002_X9707f1_Xfee.ms.split.cal/",
"uid___A002_X9d26c8_X39a.ms.split.cal/",
"uid___A002_X9d4710_X1a57.ms.split.cal/",
"uid___A002_X9d6f4c_X154.ms.split.cal/",
]

vis_spws = {
    "calibrated_X360.ms/": {0:(0,4,8,12), 1:(1,5,9,13), 2:(2,6,10,14), 3:(3,7,11,15)},
    "uid___A002_X86dcae_X416.ms.split.cal/": {0:(0,), 1:(1,), 2:(2,), 3:(3,)},
    "uid___A002_X872bbc_X412.ms.split.cal/": {0:(0,), 1:(1,), 2:(2,), 3:(3,)},
    "uid___A002_X872bbc_X7c.ms.split.cal/": {0:(0,), 1:(1,), 2:(2,), 3:(3,)},
    "uid___A002_X87436c_Xb7a.ms.split.cal/": {0:(0,), 1:(1,), 2:(2,), 3:(3,)},
    "uid___A002_X87c075_X1066.ms.split.cal/": {0:(0,), 1:(1,), 2:(2,), 3:(3,)},
    "uid___A002_X960614_X39db.ms.split.cal/": {0:(0,), 1:(1,), 2:(2,), 3:(3,)},
    "uid___A002_X9630c0_Xc26.ms.split.cal/": {0:(0,), 1:(1,), 2:(2,), 3:(3,)},
    "uid___A002_X966cea_X14a4.ms.split.cal/": {0:(0,), 1:(1,), 2:(2,), 3:(3,)},
    "uid___A002_X9707f1_Xfee.ms.split.cal/": {0:(0,), 1:(1,), 2:(2,), 3:(3,)},
    "uid___A002_X9d26c8_X39a.ms.split.cal/": {0:(0,), 1:(1,), 2:(2,), 3:(3,)},
    "uid___A002_X9d4710_X1a57.ms.split.cal/": {0:(0,), 1:(1,), 2:(2,), 3:(3,)},
    "uid___A002_X9d6f4c_X154.ms.split.cal/": {0:(0,), 1:(1,), 2:(2,), 3:(3,)},
}

vis7m = [
"calibrated_X360.ms/",
'uid___A002_X86dcae_X416.ms.split.cal',
'uid___A002_X872bbc_X412.ms.split.cal',
'uid___A002_X872bbc_X7c.ms.split.cal',
'uid___A002_X87436c_Xb7a.ms.split.cal',
'uid___A002_X87c075_X1066.ms.split.cal',
]
if not os.path.exists('calibrated_7m.ms'):
    concat(vis=vis7m, concatvis='calibrated_7m.ms')

vis12m = [
"calibrated_X360.ms/",
"uid___A002_X960614_X39db.ms.split.cal/",
"uid___A002_X9630c0_Xc26.ms.split.cal/",
"uid___A002_X966cea_X14a4.ms.split.cal/",
"uid___A002_X9707f1_Xfee.ms.split.cal/",
"uid___A002_X9d26c8_X39a.ms.split.cal/",
"uid___A002_X9d4710_X1a57.ms.split.cal/",
"uid___A002_X9d6f4c_X154.ms.split.cal/",
]
if not os.path.exists('calibrated_12m.ms'):
    concat(vis=vis12m, concatvis='calibrated_12m.ms')


def makefits(myimagebase):
    impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True) # perform PBcorr
    exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', dropdeg=True, overwrite=True) # export the corrected image
    exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.model', fitsimage=myimagebase+'.model.fits', dropdeg=True, overwrite=True) # export the PB image
    exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', dropdeg=True, overwrite=True) # export the PB image



weighting = 'briggs'
robust=0.5
# quoted noise "typically 5 mJy"
threshold = '50mJy'
cell='0.2arcsec'
imsize=[1280,1536]
phasecenter="J2000 05h35m17.448044 -05d22m43.00000"

nchans_total = {0: 1920, 1: 3840, 2: 3840, 3: 3840}

#for ii,startfreq,width, nchan in [(0, 230251.577, 976.562, 1920),
#                                  (1, 232048.811, 488.281, 3840),
#                                  (2, 216443.82396, 488.281, 3840),
#                                  (3, 218244.80196, 488.281, 3840),
#                                 ]:
for ii,startfreq,width, nchan in [(0, 230251.577, 976.7, 1920),
                                  (1, 232048.811, 488.4, 3840),
                                  (2, 216443.82396, 488.4, 3840),
                                  (3, 218244.80196, 488.4, 3840),
                                 ]:
    failure = False
    spw = str(ii)
    spwnum = ii
    concatvis = 'spw{0}_concat.ms'.format(spw)
    if not os.path.exists(concatvis):
        print("# running cvel on all lines in spw{0}".format(spwnum))
        cvelvises = []

        for vv in vis:
            tb.open(os.path.join(vv,'FIELD'))
            vv_fields = tb.getcol('NAME')
            tb.close()
            field = [x for x in ['OMC1_NW', 'OMC1_SE']
                     if x in vv_fields]

            for ss in vis_spws[vv][spwnum]:

                cvelvis = 'spw{0}-{1}_{2}.cvel'.format(spw, ss, vv.strip("/"))
                cvelvises.append(cvelvis)
                if not os.path.exists(cvelvis):
                    print("cvel'ing {0} spw {1}-{2}".format(vv, spw, ss))


                    result = cvel(vis=vv,
                                  outputvis=cvelvis,
                                  passall=False, field=field,
                                  spw=str(ss), selectdata=True,
                                  timerange='', array='', antenna='', scan='',
                                  mode='frequency',
                                  nchan=nchan,
                                  start='{0}MHz'.format(startfreq),
                                  width='{0}kHz'.format(width),
                                  interpolation='linear',
                                  phasecenter='', restfreq='', outframe='LSRK',
                                  veltype='radio',
                                  hanning=False,)
                    print("cvel result: {0}".format(result))
                    if not os.path.exists(cvelvis):
                        print("Cveling {0} to {1} failed".format(vv, cvelvis))
                        failure = True

    if failure:
        break


    output = "Orion_NWSE_mosaic_spw{0}_fullcube".format(ii)

    if any([os.path.exists(output+"."+suffix)
            for suffix in ('psf', 'weight', 'sumwt', 'pb', 'model', 'residual',
                           'mask', 'image.tt0')]):
        print("Skipping {0}".format(output))
        continue

    tclean(vis = cvelvises,
           imagename = output,
           field = '',
           spw = '',
           gridder = 'mosaic',
           specmode = 'cube',
           width = "{0}kHz".format(width),
           start = "{0}MHz".format(startfreq),
           nchan = nchan,
           veltype = 'radio',
           outframe = 'LSRK',
           deconvolver='clark',
           interactive = False,
           niter = 1000000, # force the clean to go to threshold
           imsize = imsize,
           cell = cell,
           weighting = weighting,
           phasecenter = phasecenter,
           robust = robust,
           threshold = threshold,
           savemodel='none')

    makefits(output)
