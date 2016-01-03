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
     phasecenter='J2000 5h35m12.023 -5d21m33.65',
    )


concatvis = 'NWSE_12CO2-1_merge_7m_12m.ms'
if not os.path.exists(concatvis):
    concat(vis=inputvis, concatvis=concatvis)

lineimagename='Orion_NWSE_12CO2-1_merge_7m_12m'
clean(vis=concatvis,
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
      niter=10000,
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
