# Script to reduce ALMA data for 2013.1.00546.S

########################################
# Check CASA version

# We need to use CASA 4.2.2 to get the improved weighting scheme.

import re

if re.search('^4.2', casadef.casa_version) == None:
 sys.exit('ERROR: PLEASE USE THE SAME VERSION OF CASA THAT YOU USED FOR GENERATING THE SCRIPT: 4.2')

###################################
# Splitting off science target data

# Taking a look at the data
vis='uid___A002_X86dcae_X416.ms.split.cal'
listobs(vis=vis, listfile=vis+'.listobs')


# Clear the pointing table to speed clean and fix mosaicing issues

tb.open('uid___A002_X86dcae_X416.ms.split.cal/POINTING', nomodify = False)
a = tb.rownumbers()
tb.removerows(a)
tb.close()

# INCLUDE LISTOBS OUTPUT FOR SCIENCE TARGET AND SPW IDS HERE.
# science target: field 5~18, spw 0~3

# Doing the split
sourcevis='source_calibrated.ms'
field='5~18'  # change to relevant field id number(s)
os.system('rm -rf '+sourcevis)
split(vis=vis,
      outputvis=sourcevis,
      datacolumn='data', # depending on how the data were produced may need datacolumn='corrected' instead
      field=field)

# Check that split worked as desired.
listobs(vis=sourcevis, listfile=sourcevis+'.listobs') 

# Rename and backup data set

# If you have a single execution:
os.system('mv -i ' + sourcevis + ' ' + 'calibrated_final.ms')

# At this point you should create a backup of your final data set in
# case the ms you are working with gets corrupted by clean. Uncomment
# the correct command depending on your case.

os.system('cp -ir calibrated_final.ms calibrated_final.ms.backup')

##################################################
# Identify Line-free SPWs and channels

finalvis='calibrated_final.ms' # This is your output ms from the data
                               # preparation script.

# Use plotms to identify line and continuum spectral windows
plotms(vis=finalvis, xaxis='channel', yaxis='amplitude',
       ydatacolumn='corrected', # may need to be changed to 'data'
       avgtime='1e8', avgscan=True, avgchannel='2', # you should only lightly average over frequency
       iteraxis='spw' )

##################################################
# Create an Averaged Continuum MS

# Continuum images can be sped up considerably by averaging the data
# together to reduce overall volume.

# Complex Line Emission
# --------------------

# If you have complex line emission and no dedicated continuum
# windows, you will need to flag the line channels prior to averaging.

# Note: this dataset has extremely complex line emission! There are no dedicated continuum windows. 
# Need to try to flag all visible lines. 

# Set continuum spws here based on plotms output.
contspws = '0,1,2,3' 	# Note: there are no continuum-only SPWs, so we will find continuum channels in all four line SPWs

flagmanager(vis=finalvis,mode='save',
            versionname='before_cont_flags')

# Flag the "line channels"
flagchannels='0:21~29; 82~116; 156~168; 191~194; 222~237; 262~434; 459~474; 530~557; 593~600; 614~618; 680~705; 737~776; 785~805; 824~834; 851~934; 956~965; 998~1193; 1227~1333; 1380~1384; 1407~1424; 1434~1513; 1548~1599; 1613~1843; 1867~1878; 1907~1915; 1944~1973; 1995~2039, 1:27~37; 58~76; 104~132; 155~276; 318~319; 342~344; 369~385; 405~439; 471~498; 536~549; 575~587; 602~606; 620~694; 723~765; 790~823; 835~879; 935~1714; 1744~2039, 2:34~120; 137~141; 157~202; 235~312; 354~410; 445~462; 514~524; 559~672; 696~722; 755~851; 888~920; 985~1022; 1043~1055; 1103~1124; 1154~1234; 1257~1259; 1271~1407; 1422~1426; 1449~1518; 1547~1550; 1579~1624; 1649~1829; 1842~1934; 1999~2039, 3:21~59; 106~131; 155~173; 202~302; 341~343; 375~587; 617~668; 691~749; 772~775; 796~817; 845~895; 929~1005; 1024~1070; 1118~1121; 1142~1145; 1174~1195; 1214~1260; 1301~1398; 1451~1500; 1538~1564; 1608~1661; 1701~1725; 1739~1857; 1895~1964; 1981~1991; 2001~2039'
 
# Flag lines in SPW 0: 21~29, 82~116, 156~168, 191~194, 222~237, 262~434, 459~474, 530~557, 593~600, 614~618, 680~705, 737~776, 785~805, 824~834, 851~934, 956~965, 998~1193, 1227~1333, 1380~1384, 1407~1424, 1434~1513, 1548~1599, 1613~1843, 1867~1878, 1907~1915, 1944~1973, 1996~2039
# Flag lines in SPW 1: 27~37, 58~76, 104~132, 155~276, 318~319, 342~344, 369~385, 405~439, 471~498, 536~549, 575~587, 602~606, 620~694, 723~765, 796~823, 835~879, 935~1714, 1744~2039
# Flag lines in SPW 2: 34~120, 137~141, 159~202, 235~312, 354~410, 445~462, 516~524, 559~672, 696~722, 755~851, 888~920, 985~1022, 1043~1055, 1103~1124, 1154~1231, 1257~1259, 1271~1407, 1422~1426, 1449~1518, 1547~1550, 1579~1624, 1649~1829, 1842~1934, 1999~2039
# Flag lines in SPW 3: 21~59, 106~131, 155~173, 202~302, 341~343, 375~587, 617~668, 691~749, 772~775, 796~817, 845~894, 929~1005, 1024~1070, 1118~1121, 1142~1145, 1174~1195, 1214~1260, 1301~1398, 1451~1500, 1538~1564, 1608~1661, 1701~1725, 1739~1857, 1895~1962, 1981~1991, 2001~2039

flagdata(vis=finalvis,mode='manual',
          spw=flagchannels,flagbackup=False)

# check that flags are as expected, NOTE must check reload on plotms
# gui if its still open.
plotms(vis=finalvis,yaxis='amp',xaxis='channel',
       avgchannel='2',avgtime='1e8',avgscan=True,iteraxis='spw') 

# Average the channels within spws
contvis='calibrated_final_cont.ms'
os.system('rm -rf ' + contvis)
split(vis=finalvis,
      spw=contspws,      
      outputvis=contvis,
      width=2040, # number of channels to average together. change to appropriate value for data set.
      datacolumn='data')

# Restore the flags
flagmanager(vis=finalvis,mode='restore',
            versionname='before_cont_flags')

# Inspect continuum for any problems
plotms(vis=contvis,xaxis='uvdist',yaxis='amp',coloraxis='spw')

# #############################################
# Image Parameters

# You're now ready to image. Review the science goals in the OT and
# set the relevant imaging parameters below. 

# source parameters
# ------------------

field='0~13' # science field(s). For a mosaic, select all mosaic fields.
# imagermode='csclean' # uncomment if single field
imagermode='mosaic' # uncomment if mosaic

# image parameters.
# ----------------

# Generally, you want ~5 cells across the beam. The beam size is
# 206265.0/(longest baseline in wavelengths). Divide by ~five to get
# your cell size. You can use plotms with xaxis='uvwave' and
# yaxis='amp' to see what the longest baseline is.

# Note: max UV baseline is ~36 klambda, so beam size is ~5.7". use a pixel size of 1.0". 

# For single fields, the ALMA 12m beam in arcsec scales as 6300 /
# nu[GHz]. For mosaics, you can get the mosaic size from the OT.

# Note: requested mosaic size is 70" on a side, plus half primary beams on both sides (~45").
# Note: 120" square should cover the map, but need a bigger imsize (256,256) to avoid imaging artifacts. 
# Note: center of mosaic is not with any particular pointing; closest to pointing #10 position (phasecenter=5 in split file).

cell='1arcsec' # cell size for imaging.
imsize = [256,256] # size of image in pixels. 
phasecenter=5
#phasecenter = 'J2000 05h17m35.5 -05d22m45'


# velocity parameters
# -------------------

#start='-100km/s' # start velocity. See science goals for appropriate value.
width='1.4km/s' # velocity width. See science goals. 1.13 MHz --> 1.47 km/s channels
#nchan = 100  # number of channels. See science goals for appopriate value.
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type. See science goals.
restfreq='230.538GHz' # rest frequency of primary line of interest. See science goals.

# imaging control
# ----------------

# The cleaning below is done interactively, so niter and threshold can
# be controlled within clean. 

weighting = 'briggs'
robust=0.5
niter=1000
threshold = '0.0mJy'

#############################################
# Imaging the Continuuum 

contimagename = 'calibrated_final_cont_image'
os.system('rm -rf ' + contimagename + '.*')
delmod(vis=contvis)
clean(vis=contvis,
      imagename=contimagename,
      field=field, 
      mode='mfs',
      psfmode='clark',
      imsize = [256,256], 
      cell= cell, 
      weighting = weighting, 
      robust = robust,
      niter = niter, 
      threshold = threshold, 
      interactive = True,
      imagermode = imagermode,
      phasecenter=phasecenter)

# If interactively cleaning (interactive=True), then note number of
# iterations at which you stop for the PI. This number will help the
# PI replicate the delivered images.

# Cleaned a total of 17.5075 Jy. 19 iterations in major cycle 0, 100 iterations in major cycle 1.
# rms ~ 10 mJy

########################################
# Continuum Subtraction for Line Imaging

# If you have observations that include both line and strong (>3 sigma
# per final line image channel) continuum emission, you need to
# subtract the continuum from the line data. You should not continuum
# subtract if the line of interest is in absorption.

# Channels to use for continuum subtraction (may have small lines but no major ones):
# SPW 0: 436~515, 570~815, 1200~1500, 1860~1930
# SPW 1: 290~390, 500~700, 835~915
# SPW 2: 250~500, 660~950, 1375~1430, 1940~2000
# SPW 3: 315~360, 1080~1200

fitspw = '0:436~515;570~815;1200~1500;1860~1930, 1:290~390;500~700;835~915, 2:250~500;660~950;1375~1430;1940~2000, 3:315~360;1080~1200' 
	# line-free channel for fitting continuum
linespw = '0,1,2,3' # line spectral windows. You can subtract the continuum from multiple spectral line windows at once.

uvcontsub(vis=finalvis,
          spw=linespw, # spw to do continuum subtraction on
          fitspw=fitspw, # select spws to fit continuum. exclude regions with strong lines.
          combine='spw', 
          solint='int',
          fitorder=2,
          want_cont=False) # This value should not be changed.

# NOTE: Imaging the continuum produced by uvcontsub with
# want_cont=True will lead to extremely poor continuum images because
# of bandwidth smearing effects. For imaging the continuum, you should
# always create a line-free continuum data set using the process
# outlined above.

linevis = finalvis+'.contsub'

##############################################
# Image line emission [REPEAT AS NECESSARY]

# Note: there are a *lot* of faint lines in each SPW. I will just image representative cubes from each according to the lines requested in the proposal: CO 2-1 (SPW 0, 230.538 GHz, channel 200~500), SiO (SPW 2, 217.105 GHz, channel 1200~1500), and SO (SPW 3, 219.949 GHz, channel 100~400). 

lineimagename = 'source_calibrated_CO' # name of each line image

os.system('rm -rf ' + lineimagename + '.*')
delmod(vis=linevis)		# do this every time to remove existing model column
clean(vis=linevis,
      imagename=lineimagename, 
      field=field,
      spw='0',			
      mode='velocity',
      start='-100km/s',		
      width=width,
      nchan=180, 		
      outframe=outframe, 
      veltype=veltype, 
      restfreq='230.538GHz', 	
      niter=niter,  
      threshold=threshold, 
      interactive=True,
      cell=cell,
      imsize=imsize, 
      phasecenter=phasecenter,
      weighting=weighting, 
      robust=robust,
      imagermode=imagermode,
      usescratch=True)

lineimagename = 'source_calibrated_SiO'

os.system('rm -rf ' + lineimagename + '.*')
delmod(vis=linevis)             # do this every time to remove existing model column
clean(vis=linevis,
      imagename=lineimagename,
      field=field,
      spw='2',                  
      mode='velocity',
      start='-120km/s',          
      width=width,
      nchan=125,                
      outframe=outframe,
      veltype=veltype,
      restfreq='217.105GHz',    
      niter=niter,
      threshold=threshold,
      interactive=True,
      cell=cell,
      imsize=imsize,
      weighting=weighting,
      robust=robust,
      imagermode=imagermode,
      phasecenter=phasecenter,
      usescratch=True)

# SiO SPW: rms ~30 mJy. cleaned a total of 4203.43 Jy. 

lineimagename = 'source_calibrated_SO'

os.system('rm -rf ' + lineimagename + '.*')
delmod(vis=linevis)             # do this every time to remove existing model column
clean(vis=linevis,
      imagename=lineimagename,
      field=field,
      spw='3',                  
      mode='velocity',
      start='-80km/s',          
      width=width,
      nchan=115,                
      outframe=outframe,
      veltype=veltype,
      restfreq='219.949GHz',    
      niter=niter,
      threshold=threshold,
      interactive=True,
      cell=cell,
      imsize=imsize,
      weighting=weighting,
      robust=robust,
      imagermode=imagermode,
      phasecenter=phasecenter,
      usescratch=True)

# SO SPW: rms ~30 mJy. cleaned a total of 7514.1 Jy. 

##############################################
# Apply a primary beam correction

import glob
myimages = glob.glob("*.image")

os.system('rm -rf *.pbcor')
for image in myimages:
    impbcor(imagename=image, pbimage=image.replace('.image','.flux'), outfile = image.replace('.image','.pbcor'))

##############################################
# Export the images

myimages = glob.glob("*.image")
for image in myimages:
    exportfits(imagename=image, fitsimage=image+'.fits',overwrite=True)

myimages = glob.glob("*.pbcor")
for image in myimages:
    exportfits(imagename=image, fitsimage=image+'.fits',overwrite=True)

myimages = glob.glob("*.flux")
for image in myimages:
    exportfits(imagename=image, fitsimage=image+'.fits',overwrite=True) 

##############################################
# Analysis

# For examples of how to get started analyzing your data, see 
#     http://casaguides.nrao.edu/index.php?title=TWHydraBand7_Imaging_4.2


