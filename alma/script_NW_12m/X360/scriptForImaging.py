#======================================================================================#
#                        TEMPLATE IMAGING SCRIPT                                       #
# =====================================================================================#

# Updated: 12/19/2014

#--------------------------------------------------------------------------------------#
#                     Data Preparation                                                 #
# -------------------------------------------------------------------------------------#

# Below are some example commands for combining your data. All of
# these commands will not be relevant for all datasets, so think about
# what would be best for your data before running any commands. For
# more information, see the NA Imaging Guide
# (https://staff.nrao.edu/wiki/bin/view/NAASC/NAImagingScripts).

# These commands should be run prior to undertaking any imaging.

# The NA Imaging team is working on generating best
# practices for this step. Suggestions are welcome!  Please send to
# akepley@nrao.edu and she'll forward them on to the NA Imaging team.

########################################
# Check CASA version


import re

if re.search('^4.3', casadef.casa_version) == None:
 sys.exit('ERROR: PLEASE USE THE SAME VERSION OF CASA THAT YOU USED FOR GENERATING THE SCRIPT: 4.3')

########################################
# Removing pointing table

# This step removes the pointing table from the data to avoid
# a bug with mosaics in CASA 4.2.2

#vislist=glob.glob('*.ms.split.cal')

#for vis in vislist:
#    tb.open( vis + '/POINTING',
#            nomodify = False)
#    a = tb.rownumbers()
#    tb.removerows(a)
#    tb.close()


###################################
# Splitting off science target data

vislist=['calibrated.ms']

for vis in vislist:
    listobs(vis=vis)

    # INCLUDE LISTOBS OUTPUT FOR SCIENCE TARGET AND SPW IDS HERE.

# Doing the split

for vis in vislist:
    sourcevis=vis+'.source'
    os.system('rm -rf '+sourcevis)
    split(vis=vis,
          intent='*TARGET*', # split off the target sources
          outputvis=sourcevis,
          datacolumn='data', # depending on how the data were produced may need datacolumn='corrected' instead
          field=field)

    # Check that split worked as desired.
    listobs(vis=sourcevis) 


############################################
# Rename and backup data set

# If you have a single execution:
os.system('mv -i ' + sourcevis + ' ' + 'calibrated_final.ms')

# If you have multiple executions:
#os.system('mv -i ' + regridvis + ' ' + 'calibrated_final.ms')

# At this point you should create a backup of your final data set in
# case the ms you are working with gets corrupted by clean. 

os.system('cp -ir calibrated_final.ms calibrated_final.ms.backup')


#--------------------------------------------------------------------------------------#
#                             Imaging Template                                         #
#--------------------------------------------------------------------------------------#

# The commands below serve as a guide to best practices for imaging
# ALMA data. It does not replace careful thought on your part while
# imaging the data. You can remove or modify sections as necessary
# depending on your particular imaging case (e.g., no
# self-calibration, continuum only.) Please read the NA Imaging Guide
# (https://staff.nrao.edu/wiki/bin/view/NAASC/NAImagingScripts) for
# more information.

# Before imaging, you should use the commands the first section of
# this script to prep the data for imaging.  The commands in both file
# should be able to be run as as standard Python script. However, the
# cleaning in this script is done interactively making the final
# product somewhat dependent on the individual doing the clean --
# please clean conservatively (i.e., don't box every possible
# source). The final data products are the cleaned images (*.image),
# the primary beam corrected images (*.pbcor), and the primary beams
# (*.flux). These images should be converted to fits at the end of the
# script (see example at the end of this file).

# This script (and the associated guide) are under active
# development. Please contact Amanda Kepley (akepley@nrao.edu) if you
# have any suggested changes or find any bugs that are almost
# certainly there.

##################################################
# Identify Line-free SPWs and channels

finalvis='calibrated_final.ms' # This is your output ms from the data
                               # preparation script.

# Use plotms to identify line and continuum spectral windows
plotms(vis=finalvis, xaxis='channel', yaxis='amplitude',
       ydatacolumn='data',
       avgtime='1e8', avgscan=True, avgchannel='2',
       iteraxis='spw' )


##################################################
# Create an Averaged Continuum MS

# Continuum images can be sped up considerably by averaging the data
# together to reduce overall volume.

# Project includes Continuum-only SPWs
# ----------------------------------------

# Complex Line Emission
# --------------------

# If you have complex line emission and no dedicated continuum
# windows, you will need to flag the line channels prior to averaging.

# Set continuum spws here based on plotms output.
contspws = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'

linechan='0:0~610;670~900;990~1200;1260~1340;1360~2039,1:0~280;350~860;930~1730;1740~2039,2:0~125;140~610;670~710;730~900;970~1240;1260~2039,3:0~60;100~320;370~1080;1110~1410;1440~1670;1690~1870;1880~2039,4:0~610;670~900;990~1200;1260~1340;1360~2039,5:0~280;350~860;930~1730;1740~2039,6:0~125;140~610;670~710;730~900;970~1240;1260~2039,7:0~60;100~320;370~1080;1110~1410;1440~1670;1690~1870;1880~2039,8:0~610;670~900;990~1200;1260~1340;1360~2039,9:0~280;350~860;930~1730;1740~2039,10:0~125;140~610;670~710;730~900;970~1240;1260~2039,11:0~60;100~320;370~1080;1110~1410;1440~1670;1690~1870;1880~2039,12:0~610;670~900;990~1200;1260~1340;1360~2039,13:0~280;350~860;930~1730;1740~2039,14:0~125;140~610;670~710;730~900;970~1240;1260~2039,15:0~60;100~320;370~1080;1110~1410;1440~1670;1690~1870;1880~2039'

flagmanager(vis=finalvis,mode='save',
            versionname='before_cont_flags')

# Flag the "line channels"
flagchannels= linechan 

flagdata(vis=finalvis,mode='manual',
          spw=flagchannels,flagbackup=False)

# check that flags are as expected, NOTE must check reload on plotms
# gui if its still open.
plotms(vis=finalvis,yaxis='amp',xaxis='channel',
       avgchannel='2',avgtime='1e8',avgscan=True,iteraxis='spw') 

# Average the channels within spws
contvis='calibrated_final'

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

field='' # science field(s). For a mosaic, select all mosaic fields.
# imagermode='csclean' # uncomment if single field
imagermode='mosaic' # uncomment if mosaic
phasecenter='J2000 05h35m12 -05d21m30' 

# image parameters.
# ----------------

# Generally, you want ~5 cells across the beam. The beam size is
# 206265.0/(longest baseline in wavelengths). Divide by ~five to get
# your cell size. You can use plotms with xaxis='uvwave' and
# yaxis='amp' to see what the longest baseline is.

# For single fields, the ALMA 12m beam in arcsec scales as 6300 /
# nu[GHz]. For mosaics, you can get the mosaic size from the OT.

# If you're imaging a mosaic, pad the imsize substantially to avoid
# artifacts.

cell='1arcsec' # cell size for imaging.
imsize = [256,256] # size of image in pixels. 

# imaging control
# ----------------

# The cleaning below is done interactively, so niter and threshold can
# be controlled within clean. 

weighting = 'briggs'
robust=0.5
niter=10000
threshold = '10.0mJy'

mask='box[[58pix,7pix],[194pix,242pix]]'

#############################################
# Imaging the Continuuum

# If necessary, run the following commands to get rid of older clean
# data.

#clearcal(vis=contvis)
#delmod(vis=contvis)
         
contimagename = 'calibrated_final_cont_image'

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual']:
    os.system('rm -rf ' + contimagename + ext)

clean(vis=contvis,
      imagename=contimagename,
      field=field,
      phasecenter=phasecenter, # uncomment if mosaic.      
      mode='mfs',
      psfmode='clark',
      imsize = imsize, 
      cell= cell, 
      weighting = weighting, 
      robust = robust,
      niter = niter, 
      mask=mask,
      threshold = threshold, 
      interactive = False,
      imagermode = imagermode)

# If interactively cleaning (interactive=True), then note number of
# iterations at which you stop for the PI. This number will help the
# PI replicate the delivered images.

# Note RMS for PI. 

# save the mask
contmaskname = 'cont.mask'
#os.system('rm -rf ' + contmaskname) # uncomment if you want to overwrite the mask.
os.system('cp -ir ' + contimagename + '.mask ' + contmaskname)


########################################
# Continuum Subtraction for Line Imaging

# If you have observations that include both line and strong (>3 sigma
# per final line image channel) continuum emission, you need to
# subtract the continuum from the line data. You should not continuum
# subtract if the line of interest is in absorption.

# will do an independent subtraction for each (independent) spw

# line-free channel for fitting continuum
fitspw = '0:610~670;900~990;1200~1260;1340~1360,4:610~670;900~990;1200~1260;1340~1360,8:610~670;900~990;1200~1260;1340~1360,12:610~670;900~990;1200~1260;1340~1360'

linespw = '0,4,8,12' # line spectral windows. You can subtract the continuum from multiple spectral line windows at once.

os.system('cp -R '+finalvis+' spw0.ms')

uvcontsub(vis='spw0.ms',
          spw=linespw, # spw to do continuum subtraction on
          fitspw=fitspw, # select spws to fit continuum. exclude regions with strong lines.
          combine='', 
          solint='int',
          fitorder=1,
          want_cont=False) # This value should not be changed.

# NOTE: Imaging the continuum produced by uvcontsub with
# want_cont=True will lead to extremely poor continuum images because
# of bandwidth smearing effects. For imaging the continuum, you should
# always create a line-free continuum data set using the process
# outlined above.

linevis0 = 'spw0.ms.contsub'

##############################################
# Image line emission [REPEAT AS NECESSARY]


# velocity parameters
# -------------------

lineimagename = 'spw0_co21' # name of line image

start='-141km/s' # start velocity. See science goals for appropriate value.
width='1.5km/s' # velocity width. See science goals.
nchan = 200  # number of channels. See science goals for appopriate value.
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type. See science goals.
restfreq='230.538GHz' # rest frequency of primary line of interest. See science goals.

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual']:
    os.system('rm -rf ' + lineimagename + ext)

clean(vis=linevis0,
      imagename=lineimagename, 
      field=field,
#      spw=spw,
      phasecenter=phasecenter, # uncomment if mosaic.      
      mode='velocity',
      start=start,
      width=width,
      nchan=nchan, 
      outframe=outframe, 
      veltype=veltype, 
      restfreq=restfreq, 
      niter=niter,  
      threshold=threshold, 
      interactive=False,
      cell=cell,
      mask=mask,
      imsize=imsize, 
      weighting=weighting, 
      robust=robust,
      imagermode=imagermode)

# If interactively cleaning (interactive=True), then note number of
# iterations at which you stop for the PI. This number will help the
# PI replicate the delivered images.

# save the mask
linemaskname = 'co21.mask'
#os.system('rm -rf ' + linemaskname) # uncomment if you want to overwrite the mask.
os.system('cp -ir ' + lineimagename + '.mask ' + linemaskname)


########################################
# Continuum Subtraction for Line Imaging

# If you have observations that include both line and strong (>3 sigma
# per final line image channel) continuum emission, you need to
# subtract the continuum from the line data. You should not continuum
# subtract if the line of interest is in absorption.

# will do an independent subtraction for each (independent) spw

# line-free channel for fitting continuum
fitspw='2:125~140;610~670;710~730;900~970;1240~1260,6:125~140;610~670;710~730;900~970;1240~1260,10:125~140;610~670;710~730;900~970;1240~1260,14:125~140;610~670;710~730;900~970;1240~1260'

linespw = '2,6,10,14' # line spectral windows. You can subtract the continuum from multiple spectral line windows at once.

os.system('cp -R '+finalvis+' spw2.ms')

uvcontsub(vis='spw2.ms',
          spw=linespw, # spw to do continuum subtraction on
          fitspw=fitspw, # select spws to fit continuum. exclude regions with strong lines.
          combine='', 
          solint='int',
          fitorder=1,
          want_cont=False) # This value should not be changed.

# NOTE: Imaging the continuum produced by uvcontsub with
# want_cont=True will lead to extremely poor continuum images because
# of bandwidth smearing effects. For imaging the continuum, you should
# always create a line-free continuum data set using the process
# outlined above.

linevis2 = 'spw2.ms.contsub'

##############################################
# Image line emission [REPEAT AS NECESSARY]


# velocity parameters
# -------------------

lineimagename = 'spw2_sio54' # name of line image

start='-141km/s' # start velocity. See science goals for appropriate value.
width='1.5km/s' # velocity width. See science goals.
nchan = 200  # number of channels. See science goals for appopriate value.
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type. See science goals.
restfreq='217.10498GHz' # rest frequency of primary line of interest. See science goals.

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual']:
    os.system('rm -rf ' + lineimagename + ext)

clean(vis=linevis2,
      imagename=lineimagename, 
      field=field,
#      spw=spw,
      phasecenter=phasecenter, # uncomment if mosaic.      
      mode='velocity',
      start=start,
      width=width,
      nchan=nchan, 
      outframe=outframe, 
      veltype=veltype, 
      restfreq=restfreq, 
      niter=niter,  
      threshold=threshold, 
      interactive=False,
      mask=mask,
      cell=cell,
      imsize=imsize, 
      weighting=weighting, 
      robust=robust,
      imagermode=imagermode)

# If interactively cleaning (interactive=True), then note number of
# iterations at which you stop for the PI. This number will help the
# PI replicate the delivered images.

# save the mask
linemaskname = 'sio54.mask'
#os.system('rm -rf ' + linemaskname) # uncomment if you want to overwrite the mask.
os.system('cp -ir ' + lineimagename + '.mask ' + linemaskname)

########################################
# Continuum Subtraction for Line Imaging

# If you have observations that include both line and strong (>3 sigma
# per final line image channel) continuum emission, you need to
# subtract the continuum from the line data. You should not continuum
# subtract if the line of interest is in absorption.

# will do an independent subtraction for each (independent) spw

# line-free channel for fitting continuum

fitspw='3:60~100;320~370;1080~1110;1410~1440;1670~1690;1870~1880,7:60~100;320~370;1080~1110;1410~1440;1670~1690;1870~1880,11:60~100;320~370;1080~1110;1410~1440;1670~1690;1870~1880,15:60~100;320~370;1080~1110;1410~1440;1670~1690;1870~1880'

linespw = '3,7,11,15' # line spectral windows. You can subtract the continuum from multiple spectral line windows at once.

os.system('cp -R '+finalvis+' spw3.ms')

uvcontsub(vis='spw3.ms',
          spw=linespw, # spw to do continuum subtraction on
          fitspw=fitspw, # select spws to fit continuum. exclude regions with strong lines.
          combine='', 
          solint='int',
          fitorder=1,
          want_cont=False) # This value should not be changed.

# NOTE: Imaging the continuum produced by uvcontsub with
# want_cont=True will lead to extremely poor continuum images because
# of bandwidth smearing effects. For imaging the continuum, you should
# always create a line-free continuum data set using the process
# outlined above.

linevis3 = 'spw3.ms.contsub'


##############################################
# Image line emission [REPEAT AS NECESSARY]


# velocity parameters
# -------------------

lineimagename = 'spw3_so' # name of line image

start='-141km/s' # start velocity. See science goals for appropriate value.
width='1.5km/s' # velocity width. See science goals.
nchan = 200  # number of channels. See science goals for appopriate value.
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type. See science goals.
restfreq='219.94944GHz' # rest frequency of primary line of interest. See science goals.

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual']:
    os.system('rm -rf ' + lineimagename + ext)

clean(vis=linevis3,
      imagename=lineimagename, 
      field=field,
#      spw=spw,
      phasecenter=phasecenter, # uncomment if mosaic.      
      mode='velocity',
      start=start,
      width=width,
      nchan=nchan, 
      outframe=outframe, 
      veltype=veltype, 
      restfreq=restfreq, 
      niter=niter,  
      mask=mask,
      threshold=threshold, 
      interactive=False,
      cell=cell,
      imsize=imsize, 
      weighting=weighting, 
      robust=robust,
      imagermode=imagermode)

# If interactively cleaning (interactive=True), then note number of
# iterations at which you stop for the PI. This number will help the
# PI replicate the delivered images.

# save the mask
linemaskname = 'so.mask'
#os.system('rm -rf ' + linemaskname) # uncomment if you want to overwrite the mask.
os.system('cp -ir ' + lineimagename + '.mask ' + linemaskname)


##############################################
# Apply a primary beam correction

import glob

myimages = glob.glob("*.image")

os.system('rm -rf *.pbcor')
for image in myimages:
    impbcor(imagename=image, pbimage=image.replace('.image','.flux'), outfile = image.replace('.image','.pbcor'))

##############################################
# Export the images

import glob

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
