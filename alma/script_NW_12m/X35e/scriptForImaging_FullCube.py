field='4~111' # science field(s). For a mosaic, select all mosaic fields. DO
              # NOT LEAVE BLANK ('') OR YOU WILL TRIGGER A BUG IN CLEAN THAT
              # WILL PUT THE WRONG COORDINATE SYSTEM ON YOUR FINAL IMAGE.
phasecenter=51
cell='.2arcsec' # cell size for imaging.
imsize = [700,1200] # size of image in pixels.

# imaging control
# ----------------

# The cleaning below is done interactively, so niter and threshold can
# be controlled within clean.

weighting = 'briggs'
robust=0.5
niter=1000
threshold = '0.0mJy'

spws = {0: '0,4,8,12,16,20',
        1: '1,5,9,13,17,21',
        2: '2,6,10,14,18,22',
        3: '3,7,11,15,19,23',
       }
nchans_total = {0: 1920, 1: 3840, 2: 3840, 3: 3840}
ncubes_per_window = 20
finalvis='calibrated_final.ms'
linevis = finalvis+'.contsub'

for spwnum in '0231':
    print "# running clean on all lines in spw{0}".format(spwnum)
    spw = spws[int(spwnum)]
    nchans_total_thiscube = nchans_total[int(spwnum)]
    nchans_per_cube = nchans_total_thiscube/ncubes_per_window
    inputvis = linevis
    for ii in range(ncubes_per_window):
        start = nchans_per_cube*ii
        end = nchans_per_cube*(ii+1)
        output = 'piece_of_full_orion_cube_NW.spw{0}.channels{1}to{2}'.format(spwnum, start, end)
        #---------------------------------------------------
        # LINE IMAGING (MOSAIC MODE)
        if not os.path.exists(output+".image"):
            print "Imaging {0}".format(output)
            os.system('rm -rf ' + output + '*')
            clean(vis = inputvis,
                  imagename = output,
                  field = field,
                  spw = spw,
                  imagermode = 'mosaic',
                  mode = 'channel',
                  width = 1,
                  start = start,
                  nchan = nchans_per_cube,
                  chaniter = True,
                  veltype = 'radio',
                  outframe = 'LSRK',
                  interactive = F,
                  niter = 2000,
                  imsize = imsize,
                  cell = cell,
                  psfmode='clark',
                  weighting = weighting,
                  phasecenter = phasecenter,
                  robust = robust,
                  threshold = threshold,
                  pbcor = T,
                  usescratch= T)

          
        if not os.path.exists(output+".image.pbcor"):
            myimagebase = output
            impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.flux', outfile=myimagebase+'.image.pbcor', overwrite=True)
            exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', overwrite=True)
            exportfits(imagename=myimagebase+'.flux', fitsimage=myimagebase+'.flux.fits', overwrite=True)


