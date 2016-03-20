se = '../science_goal.uid___A001_X122_X362/group.uid___A001_X122_X363/merge/Orion_SE_merge_7m_12m.ms'
nw = '../science_goal.uid___A001_X122_X35c/group.uid___A001_X122_X35d/merge/Orion_NW_merge_7m_12m.ms'

cvel(vis=se,
     outputvis='SE_merge_7m12m_CO2-1.ms',
     field='OMC1_SE',
     spw='0,4',
     mode='velocity',
     start='-240km/s',
     width='1.46km/s',
     nchan=300,
     outframe='LSRK',
     veltype='radio',
     restfreq='230.538GHz',
     phasecenter="J2000 05h35m17.448044 -05d22m43.00000",
    )

cvel(vis=nw,
     outputvis='NW_merge_7m12m_CO2-1.ms',
     field='OMC1_NW',
     spw='0,4,8,12,16,20,24,28,32,36',
     mode='velocity',
     start='-240km/s',
     width='1.46km/s',
     nchan=300,
     outframe='LSRK',
     veltype='radio',
     restfreq='230.538GHz',
     phasecenter='J2000 05h35m12.023 -05d21m33.65',
    )


concatvis = 'NWSE_12CO2-1_merge_7m_12m.ms'
inputvis = ['SE_merge_7m12m_CO2-1.ms', 'NW_merge_7m12m_CO2-1.ms']
if not os.path.exists(concatvis):
    concat(vis=inputvis, concatvis=concatvis)

uvcontsub(vis=concatvis, fitspw='0:0~20;280~300', fitorder=0)
# or fitspw='0:0~20,0:280~300'

lineimagename='Orion_NWSE_12CO2-1_merge_7m_12m'
for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(lineimagename+ext)

clean(vis=concatvis+".contsub",
      imagename=lineimagename,
      field='',
      spw='',
      phasecenter='J2000 5h35m14.581 -5d21m42.18',
      mode='velocity',
      start='-240km/s',
      width='1.46km/s',
      nchan=300,
      outframe='LSRK',
      veltype='radio',
      restfreq='230.538GHz',
      niter=1000000,
      threshold='30mJy',
      interactive=False,
      cell='0.2arcsec',
      imsize=[1280,1536],
      weighting='briggs',
      robust=0.5,
      imagermode='mosaic',
      minpb=0.4,
      usescratch=False)

exportfits(lineimagename+".image", lineimagename+".image.fits", dropdeg=True, overwrite=True)


lineimagename='Orion_NWSE_12CO2-1_merge_7m_12m_longbaselinesonly'
for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(lineimagename+ext)

tclean(vis=concatvis+".contsub",
       imagename=lineimagename,
       deconvolver='hogbom',
       field='',
       spw='',
       phasecenter='J2000 5h35m14.581 -5d21m42.18',
       specmode='cube',
       start='-240km/s',
       width='1.46km/s',
       nchan=300,
       outframe='LSRK',
       veltype='radio',
       restfreq='230.538GHz',
       niter=1000000,
       threshold='30mJy',
       uvrange='40~1000000m',
       interactive=False,
       cell='0.2arcsec',
       imsize=[1280,1536],
       weighting='briggs',
       robust=0.5,
       gridder='mosaic',
       pblimit=0.4)
   
exportfits(lineimagename+".image", lineimagename+".image.fits", dropdeg=True, overwrite=True)
exportfits(lineimagename+".model", lineimagename+".model.fits", dropdeg=True, overwrite=True)
