"""
Joint imaging of 7m and 12m data
"""

# scp /Volumes/passport/alma/sgrb2_b3/2013.1.00269.S/science_goal.uid___A001_X121_X4b6/group.uid___A001_X121_X4b7/member.uid___A001_X121_X4bc/calibrated/calibrated.ms cleese:/scratch/aginsbur/sgrb2/2013.1.00269.S/science_goal.uid___A001_X121_X4b6/group.uid___A001_X121_X4b7/member.uid___A001_X121_X4bc/calibrated/SgrB2_a_03_7M.calibrated.ms
# member.uid___A001_X122_X35e  member.uid___A001_X122_X360
inputvis = [
            '../member.uid___A001_X122_X364/calibrated/calibrated_final.ms',
            '../member.uid___A001_X122_X366/calibrated/calibrated_final.ms',
            ]
concatvis = 'Orion_SE_merge_7m_12m.ms'
if not os.path.exists(concatvis):
    concat(vis=inputvis, concatvis=concatvis)
    plotms(vis=concatvis,yaxis='wt',xaxis='uvdist',spw='0~2:200',
           coloraxis='spw',plotfile='combine_WT.png', showgui=False)

lineimagename = 'Orion_SE_7m_12m_merge_12CO_2-1' # name of line image
print("Cleaning CO: {0}".format(lineimagename))
niter = 10000
threshold = '30mJy'

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(lineimagename+ext)

phasecenter = "J2000 05h35m17.448044 -05d22m43.00000"

linevis=concatvis
clean(vis=linevis,
      imagename=lineimagename,
      field='OMC1_SE',
      spw='0,4',
      phasecenter=phasecenter,
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
      imsize=[1024,1024],
      weighting='briggs',
      robust=0.5,
      imagermode='mosaic',
      minpb=0.4,
      usescratch=False)

exportfits(lineimagename+".image", lineimagename+".image.fits", dropdeg=True, overwrite=True)
