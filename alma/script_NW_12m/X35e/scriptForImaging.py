#======================================================================================#
#                        TEMPLATE IMAGING SCRIPT                                       #
# =====================================================================================#

# Updated: Wed Apr  8 15:13:30 MDT 2015


# Helpful tip: Use the commands %cpaste or %paste to copy and paste
# indented sections of code into the casa command line.

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
import os

# I don't care what version does the imaging.
# if (re.search('^4.2', casadef.casa_version) or re.search('^4.3', casadef.casa_version))  == None:
#  sys.exit('ERROR: PLEASE USE THE SAME VERSION OF CASA THAT YOU USED FOR GENERATING THE SCRIPT: 4.2 or 4.3')

########################################
# Getting a list of ms files to image

import glob

vislist=glob.glob('*.ms.split.cal')

########################################
# Removing pointing table

# This step removes the pointing table from the data to avoid
# a bug with mosaics in CASA 4.2.2

for vis in vislist:
    tb.open( vis + '/POINTING',
            nomodify = False)
    a = tb.rownumbers()
    tb.removerows(a)
    tb.close()


###################################
# Splitting off science target data

for vis in vislist:
    print("Listing observations for {0}".format(vis))
    listobs(vis=vis)

    # INCLUDE LISTOBS OUTPUT FOR SCIENCE TARGET AND SPW IDS HERE.

# Doing the split
for vis in vislist:
    sourcevis=vis+'.source'
    if not os.path.exists(sourcevis):
        print("Splitting {0} into {1}".format(vis,sourcevis))
        rmtables(sourcevis)
        os.system('rm -rf ' + sourcevis + '.flagversions')
        split(vis=vis,
              intent='*TARGET*', # split off the target sources
              outputvis=sourcevis,
              datacolumn='data') # If multiple data sets were rescaled using scriptForFluxCalibration.py, need to get datacolumn='corrected'


        # Check that split worked as desired.
        listobs(vis=sourcevis)


###############################################################
# Combining Measurement Sets from Multiple Executions [OPTIONAL]

# Scheduling blocks with multiple executions can generate multiple
# spectral windows with different sky frequencies, but the same rest
# frequency, due to the motion of the Earth. Due to Doppler setting,
# the number of spectral windows in this case is typically
# spw=(#original science spws) x (number executions).  It is possible
# to combine these spws now to make imaging easier later on. However,
# this step can be skipped and done in the line imaging stage. See the
# NA imaging wiki for a full description of your options and their
# pros/cons:
# https://staff.nrao.edu/wiki/bin/view/NAASC/NAImagingScripts

# The code below provides three different options to do this. Choose
# one depending on your data set and personal preferences! We are
# still generating recommendations for best practices for this
# step. Contact akepley@nrao.edu if you have input.

# Simple concat (spws not combined)
# ---------------------------------

# Ms'es from multiple executions of the same scheduling block can be
# combined into one ms using concat. In this case, you will end up
# with a single ms with n spws, where n is (#original science spws) x
# (number executions). The multiple spws associated with a single
# frequency will not be regridded to a single spectral window in the
# ms.  However, they can be regridded to a single spectral window
# later during cleaning. If you are planning on doing any
# self-calibration, you should do at least this step, although you may
# want to consider one of the other methods outlined below.
'''
sourcevislist = glob.glob("*.ms.split.cal.source")
regridvis='source_calibrated_regrid.ms'

rmtables(regridvis)
os.system('rm -rf ' + regridvis + '.flagversions')
concat(vis=sourcevislist,
       concatvis=regridvis)
'''
# Special concat case (combines spws with small frequency shifts)
# ---------------------------------------------------------------

# Use this code only to combine spws with small changes in the
# frequency axis. In general, freqtol should be no more than 1/5 the
# narrowest channel size.

if not os.path.exists('calibrated_final.ms'):
    sourcevislist = glob.glob("*.ms.split.cal.source")
    regridvis='source_calibrated_regrid.ms'
    print("Concatenating {0} into {1}".format(sourcevislist, regridvis))

    rmtables(regridvis)
    os.system('rm -rf ' + regridvis + '.flagversions')
    concat(vis=sourcevislist,
           concatvis=regridvis,
           freqtol='1kHz') # choose appropriate value for data set. Should be less than 1/5 the narrowest channel size.

    # MSTRANSFORM/CVEL case (combines spws with large frequency shifts)
    # -----------------------------------------------------------------
    '''
    # Use this code only to combine spws with large shifts in the
    # frequency axis, i.e., too large to use the previous option.

    # The cvel task could also be used here. If you have multiple spectral
    # lines, you will need to run the mstransform task once per line.

    regridvis='source_calibrated_regrid.ms'
    veltype='radio' # velocity type.

    # see science goals in OT to set following parameters.
    width='2km/s' # velocity width of channels in output spw.
    nchan = 100  # number of channels in output spw.
    outframe='bary' # velocity reference frame.
    restfreq='115.27120GHz' # rest frequency of primary line of interest.

    sourcevislist = glob.glob("*.ms.split.cal.source")

    myspw = '0' # Set the input spw that you would like to process

    for sourcevis in sourcevislist:
        rmtables(sourcevis+'.cvel')
        os.system('rm -rf ' + regridvis + '.cvel.flagversions')
        mstransform(vis=sourcevis,
                    outputvis=sourcevis+'.cvel',
                    datacolumn='data', # depending on how the data were combined may need datacolumn='corrected'
                    spw=myspw,
                    combinespws=True,
                    regridms=True,
                    mode='velocity',
                    nchan=nchan,
                    width=width,
                    restfreq=restfreq,
                    outframe=outframe,
                    veltype=veltype)

    regridvislist = glob.glob("*ms.split.cal.source.cvel")
    concat(vis=regridvislist,
           concatvis=regridvis)

    # If you have multiple sets of spws that you wish you combine, just
    # repeat the above process with myspw set to the other value.
    '''
    ############################################
    # Rename and backup data set

    # If you have a single execution:
    # os.system('mv -i ' + sourcevis + ' ' + 'calibrated_final.ms')

    # If you have multiple executions:
    os.system('mv -i ' + regridvis + ' ' + 'calibrated_final.ms')

# At this point you should create a backup of your final data set in
# case the ms you are working with gets corrupted by clean.

# DO NOT DO THIS - it's 350 GB!  There is no space for this!
# os.system('cp -ir calibrated_final.ms calibrated_final.ms.backup')


# Please do not modify the final name of the file
# ('calibrated_final.ms'). The packaging process requires a file with
# this name.

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
'''
# plotms can't handle this much data

# Use plotms to identify line and continuum spectral windows
plotms(vis=finalvis, xaxis='channel', yaxis='amplitude',
       ydatacolumn='data',
       avgtime='1e8', avgscan=True, avgchannel='2', # you should only lightly average over frequency
#       avgbaseline=True, # try if you don't see anything with the time and frequency averaging
       iteraxis='spw' )
'''
##################################################
# Create an Averaged Continuum MS

# Continuum images can be sped up considerably by averaging the data
# together to reduce overall volume.

# Project includes Continuum-only SPWs
# ----------------------------------------

# In this case, you just need to average dedicated continuum spws.
'''
# Average channels within spws
contspws='1,5,9,13,17,21' # from plotms output
contvis='calibrated_final_cont.ms'
rmtables(contvis)
os.system('rm -rf ' + contvis + '.flagversions')
split(vis=finalvis,
      spw=contspws,
      outputvis=contvis,
      width=[3840,3840,3840,3840,3840,3840], # number of channels to average together. change to appropriate value for each spectral window in contspws (use listobs to find) and make sure to use the native number of channels per SPW (that is, not the number of channels left after flagging any lines)
      datacolumn='data')
'''
# Complex Line Emission
# --------------------

# If you have complex line emission and no dedicated continuum
# windows, you will need to flag the line channels prior to averaging.

# Wow.  Line forest is right.
# The following is a very rough estimate of where the "line-free" regions are based
# on the plotms output and is by no means definitive.
#
# Channels with line emission:
#
# spw 0,4,8,12,16,20:
# 150~400,780~840, 960~990, 1020~1090,1550~1570, 1610~1690,1720~1780

# spw 1,5,9,13,17,21:
# 0~50, 190~450, 680~750,1450~1500, 1750~3750

# spw 2,6,10,14,18,22:
# 0~120,200~300,600~650,750~800,900~950,1000~1100,1400~1450,1550~1600,1850~1950,2100~2150,2200~2350,2400~2600,2780~2900,3050~3100,3280~3500,3600~3750

# spw 3,7,11,15,19,23:
# 100~150, 300~500, 640~720,800~1000,1150~1200,1250~1320,1350~1400,1450~2000,2350~2400,2500~2650,2800~2850,3070~3200,3280~3839

contvis='calibrated_final_cont.ms'
if not os.path.exists(contvis):
    print("Creating {0} by flagging data.".format(contvis))
    # Set continuum spws here based on plotms output.
    contspws = '0~23'

    flagmanager(vis=finalvis,mode='save',
                versionname='before_cont_flags')

    # Flag the "line channels"
    flagchannels='0:150~400,0:780~840, 0:960~990, 0:1020~1090,0:1550~1570, 0:1610~1690,0:1720~1780,' + \
                 '4:150~400,4:780~840, 4:960~990, 4:1020~1090,4:1550~1570, 4:1610~1690,4:1720~1780,' + \
                 '8:150~400,8:780~840, 8:960~990, 8:1020~1090,8:1550~1570, 8:1610~1690,8:1720~1780,' + \
                 '12:150~400,12:780~840, 12:960~990, 12:1020~1090,12:1550~1570, 12:1610~1690,12:1720~1780,' + \
                 '16:150~400,16:780~840, 16:960~990, 16:1020~1090,16:1550~1570, 16:1610~1690,16:1720~1780,' + \
                 '20:150~400,20:780~840, 20:960~990, 20:1020~1090,20:1550~1570, 20:1610~1690,20:1720~1780,' + \
                 '1:0~50, 1:190~450, 1:680~750,1:1450~1500, 1:1750~3750,' + \
                 '5:0~50, 5:190~450, 5:680~750,5:1450~1500, 5:1750~3750,' + \
                 '9:0~50, 9:190~450, 9:680~750,9:1450~1500, 9:1750~3750,' + \
                 '13:0~50, 13:190~450, 13:680~750,13:1450~1500, 13:1750~3750,' + \
                 '17:0~50, 17:190~450, 17:680~750,17:1450~1500, 17:1750~3750,' + \
                 '21:0~50, 21:190~450, 21:680~750,21:1450~1500, 21:1750~3750,' + \
                 '2:0~120,2:200~300,2:600~650,2:750~800,2:900~950,2:1000~1100,2:1400~1450,2:1550~1600,' + \
                     '2:1850~1950,2:2100~2150,2:2200~2350,2:2400~2600,2:2780~2900,2:3050~3100,2:3280~3500,2:3600~3750,' + \
                 '6:0~120,6:200~300,6:600~650,6:750~800,6:900~950,6:1000~1100,6:1400~1450,6:1550~1600,' + \
                     '6:1850~1950,6:2100~2150,6:2200~2350,6:2400~2600,6:2780~2900,6:3050~3100,6:3280~3500,6:3600~3750,' + \
                 '10:0~120,10:200~300,10:600~650,10:750~800,10:900~950,10:1000~1100,10:1400~1450,10:1550~1600,' + \
                     '10:1850~1950,10:2100~2150,10:2200~2350,10:2400~2600,10:2780~2900,10:3050~3100,10:3280~3500,10:3600~3750,' + \
                 '14:0~120,14:200~300,14:600~650,14:750~800,14:900~950,14:1000~1100,14:1400~1450,14:1550~1600,' + \
                     '14:1850~1950,14:2100~2150,14:2200~2350,14:2400~2600,14:2780~2900,14:3050~3100,14:3280~3500,14:3600~3750,' + \
                 '18:0~120,18:200~300,18:600~650,18:750~800,18:900~950,18:1000~1100,18:1400~1450,18:1550~1600,' + \
                     '18:1850~1950,18:2100~2150,18:2200~2350,18:2400~2600,18:2780~2900,18:3050~3100,18:3280~3500,18:3600~3750,' + \
                 '22:0~120,22:200~300,22:600~650,22:750~800,22:900~950,22:1000~1100,22:1400~1450,22:1550~1600,' + \
                     '22:1850~1950,22:2100~2150,22:2200~2350,22:2400~2600,22:2780~2900,22:3050~3100,22:3280~3500,22:3600~3750,' + \
                 '3:100~150, 3:300~500, 3:640~720,3:800~1000,3:1150~1200,3:1250~1320,3:1350~1400,3:1450~2000,3:2350~2400,3:2500~2650,3:2800~2850,3:3070~3200,3:3280~3839,' + \
                 '7:100~150, 7:300~500, 7:640~720,7:800~1000,7:1150~1200,7:1250~1320,7:1350~1400,7:1450~2000,7:2350~2400,7:2500~2650,7:2800~2850,7:3070~3200,7:3280~3839,' + \
                 '11:100~150, 11:300~500, 11:640~720,11:800~1000,11:1150~1200,11:1250~1320,11:1350~1400,11:1450~2000,11:2350~2400,11:2500~2650,11:2800~2850,11:3070~3200,11:3280~3839,' + \
                 '15:100~150, 15:300~500, 15:640~720,15:800~1000,15:1150~1200,15:1250~1320,15:1350~1400,15:1450~2000,15:2350~2400,15:2500~2650,15:2800~2850,15:3070~3200,15:3280~3839,' + \
                 '19:100~150, 19:300~500, 19:640~720,19:800~1000,19:1150~1200,19:1250~1320,19:1350~1400,19:1450~2000,19:2350~2400,19:2500~2650,19:2800~2850,19:3070~3200,19:3280~3839,' + \
                 '23:100~150, 23:300~500, 23:640~720,23:800~1000,23:1150~1200,23:1250~1320,23:1350~1400,23:1450~2000,23:2350~2400,23:2500~2650,23:2800~2850,23:3070~3200,23:3280~3839'

    flagdata(vis=finalvis,mode='manual',
              spw=flagchannels,flagbackup=False)

    # check that flags are as expected, NOTE must check reload on plotms
    # gui if its still open.
    #plotms(vis=finalvis,yaxis='amp',xaxis='channel',
    #       avgchannel='2',avgtime='1e8',avgscan=True,iteraxis='spw')

    # Average the channels within spws
    rmtables(contvis)
    os.system('rm -rf ' + contvis + '.flagversions')
    split(vis=finalvis,
          spw=contspws,
          outputvis=contvis,
          # number of channels to average together. change to appropriate value for
          # each spectral window in contspws (use listobs to find) and make sure to
          # use the native number of channels per SPW (that is, not the number of
          # channels left after flagging any lines)
          width=[1920,3840,3840,3840,1920,3840,3840,3840,1920,3840,3840,3840,1920,3840,3840,3840,1920,3840,3840,3840,1920,3840,3840,3840],
          datacolumn='data')

    # Note: There is a bug in split that does not average the data
    # properly if the width is set to a value larger than the number of
    # channels in an SPW. Specifying the width of each spw (as done above)
    # is necessary for producing properly weighted data.

    # Restore the flags
    flagmanager(vis=finalvis,mode='restore',
                versionname='before_cont_flags')

# Inspect continuum for any problems
#plotms(vis=contvis,xaxis='uvdist',yaxis='amp',coloraxis='spw')

# #############################################
# Image Parameters

# You're now ready to image. Review the science goals in the OT and
# set the relevant imaging parameters below.

# source parameters
# ------------------

field='4~111' # science field(s). For a mosaic, select all mosaic fields. DO
              # NOT LEAVE BLANK ('') OR YOU WILL TRIGGER A BUG IN CLEAN THAT
              # WILL PUT THE WRONG COORDINATE SYSTEM ON YOUR FINAL IMAGE.
# imagermode='csclean' # uncomment if single field
imagermode='mosaic' # uncomment if mosaic
phasecenter=51  #to move it over a little?
                # uncomment and set to field number for phase
                # center. Note lack of ''.  Use the weblog to
                # determine which pointing to use. Remember that the
                # field ids for each pointing will be re-numbered
                # after your initial split. You can also specify the
                # phase center using coordinates, e.g.,
                # phasecenter='J2000 19h30m00 -40d00m00'

# image parameters.
# ----------------

# Generally, you want 5-8 cells (i.e., pixels) across the narrowest
# part of the beam, which is 206265.0/(longest baseline in
# wavelengths).  You can use plotms with xaxis='uvwave' and
# yaxis='amp' to see what the longest baseline is. Divide by five to
# eight to get your cell size. It's better to error on the side of
# slightly too many cells per beam than too few. Once you have made an
# image, please re-assess the cell size based on the beam of the
# image.

# To determine the image size (i.e., the imsize parameter), you need
# to determine whether or not the ms is a mosaic by either looking out
# the output from listobs or checking the spatial setup in the OT. For
# single fields, the imsize should be about the size of the primary
# beam. The ALMA 12m primary beam in arcsec scales as 6300 / nu[GHz]
# and the ALMA 7m primary beam in arcsec scales as 10608 /
# nu[GHz]. For mosaics, you can get the imsize from the spatial tab of
# the OT. If you're imaging a mosaic, pad the imsize substantially to
# avoid artifacts.

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

#############################################
print("Imaging the Continuuum")

# If necessary, run the following commands to get rid of older clean
# data.

clearcal(vis=contvis)
delmod(vis=contvis)

contimagename = 'calibrated_final_cont_image'

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(contimagename+ext)

clean(vis=contvis,
      imagename=contimagename,
      field='OMC1_NW',
      phasecenter=phasecenter, # uncomment if mosaic.
      mode='mfs',
      psfmode='clark',
      imsize = imsize,
      cell= cell,
      weighting = weighting,
      robust = robust,
      niter = niter,
      threshold = threshold,
      interactive = True,
      imagermode = imagermode)
exportfits(contimagename, contimagename+".fits", dropdeg=True, overwrite=True)

# If interactively cleaning (interactive=True), then note number of
# iterations at which you stop for the PI. This number will help the
# PI replicate the delivered images.

# Note RMS for PI. 500 iterations, 551 uJy

# If you'd like to redo your clean, but don't want to make a new mask
# use the following commands to save your original mask. This is an optional step.
#contmaskname = 'cont.mask'
##rmtables(contmaskname) # if you want to delete the old mask
#os.system('cp -ir ' + contimagename + '.mask ' + contmaskname)

##############################################
# Self-calibration on the continuum [OPTIONAL]
'''
# If the source continuum is bright, you can attempt to self-calibrate
# on it.  The example here obtains solutions from the scan time to
# down to times as short as per integration. Depending on the source,
# you may not be able to find solution on timescales that short and
# may need to adjust the solint parameter.

# set these for self-calibration solutions
refant = 'DV09' # reference antenna. Choose one that's in the array. The tasks plotants and listobs can tell you what antennas are in the array.
spwmap = [0,0,0] # mapping self-calibration solutions to individual spectral windows. Generally an array of n zeroes, where n is the number of spectral windows in the data sets.

# shallow clean on the continuum

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(contimagename + '_p0'+ ext)


clean(vis=contvis,
      imagename=contimagename + '_p0',
      field=field,
#      phasecenter=phasecenter, # uncomment if mosaic.
      mode='mfs',
      psfmode='clark',
      imsize = imsize,
      cell= cell,
      weighting = weighting,
      robust=robust,
      niter=niter,
      threshold=threshold,
      interactive=True,
      imagermode=imagermode)

# Note number of iterations performed.

# per scan solution
rmtables('pcal1')
gaincal(vis=contvis,
        caltable='pcal1',
        field=field,
        gaintype='T',
        refant=refant,
        calmode='p',
        combine='spw',
        solint='inf',
        minsnr=3.0,
        minblperant=6)

# Check the solution
plotcal(caltable='pcal1',
        xaxis='time',
        yaxis='phase',
        timerange='',
        iteration='antenna',
        subplot=421,
        plotrange=[0,0,-180,180])

# apply the calibration to the data for next round of imaging
applycal(vis=contvis,
         field=field,
         spwmap=spwmap,
         gaintable=['pcal1'],
         gainfield='',
         calwt=F,
         flagbackup=F)

# clean deeper
for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(contimagename + '_p1'+ ext)

clean(vis=contvis,
      field=field,
#      phasecenter=phasecenter, # uncomment if mosaic.
      imagename=contimagename + '_p1',
      mode='mfs',
      psfmode='clark',
      imsize = imsize,
      cell= cell,
      weighting = weighting,
      robust=robust,
      niter=niter,
      threshold=threshold,
      interactive=True,
      imagermode=imagermode)

# Note number of iterations performed.

# shorter solution
rmtables('pcal2')
gaincal(vis=contvis,
        field=field,
        caltable='pcal2',
        gaintype='T',
        refant=refant,
        calmode='p',
        combine='spw',
        solint='30.25s', # solint=30.25s gets you five 12m integrations, while solint=50.5s gets you five 7m integration
        minsnr=3.0,
        minblperant=6)

# Check the solution
plotcal(caltable='pcal2',
        xaxis='time',
        yaxis='phase',
        timerange='',
        iteration='antenna',
        subplot=421,
        plotrange=[0,0,-180,180])

# apply the calibration to the data for next round of imaging
applycal(vis=contvis,
         spwmap=spwmap,
         field=field,
         gaintable=['pcal2'],
         gainfield='',
         calwt=F,
         flagbackup=F)

# clean deeper
for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(contimagename + '_p2'+ ext)

clean(vis=contvis,
      imagename=contimagename + '_p2',
      field=field,
#      phasecenter=phasecenter, # uncomment if mosaic.
      mode='mfs',
      psfmode='clark',
      imsize = imsize,
      cell= cell,
      weighting = weighting,
      robust=robust,
      niter=niter,
      threshold=threshold,
      interactive=True,
      imagermode=imagermode)

# Note number of iterations performed.

# shorter solution
rmtables('pcal3')
gaincal(vis=contvis,
        field=field,
        caltable='pcal3',
        gaintype='T',
        refant=refant,
        calmode='p',
        combine='spw',
        solint='int',
        minsnr=3.0,
        minblperant=6)

# Check the solution
plotcal(caltable='pcal3',
        xaxis='time',
        yaxis='phase',
        timerange='',
        iteration='antenna',
        subplot=421,
        plotrange=[0,0,-180,180])

# apply the calibration to the data for next round of imaging
applycal(vis=contvis,
         spwmap=spwmap,
         field=field,
         gaintable=['pcal3'],
         gainfield='',
         calwt=F,
         flagbackup=F)

# do the amplitude self-calibration.
for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(contimagename + '_p3'+ ext)

clean(vis=contvis,
      imagename=contimagename + '_p3',
      field=field,
#      phasecenter=phasecenter, # uncomment if mosaic.
      mode='mfs',
      psfmode='clark',
      imsize = imsize,
      cell= cell,
      weighting = weighting,
      robust=robust,
      niter=niter,
      threshold=threshold,
      interactive=True,
      imagermode=imagermode)

# Note number of iterations performed.

rmtables('apcal')
gaincal(vis=contvis,
        field=field,
        caltable='apcal',
        gaintype='T',
        refant=refant,
        calmode='ap',
        combine='spw',
        solint='inf',
        minsnr=3.0,
        minblperant=6,
#        uvrange='>50m', # may need to use to exclude extended emission
        gaintable='pcal3',
        spwmap=spwmap,
        solnorm=True)

plotcal(caltable='apcal',
        xaxis='time',
        yaxis='amp',
        timerange='',
        iteration='antenna',
        subplot=421,
        plotrange=[0,0,0.2,1.8])

applycal(vis=contvis,
         spwmap=[spwmap,spwmap], # select which spws to apply the solutions for each table
         field=field,
         gaintable=['pcal3','apcal'],
         gainfield='',
         calwt=F,
         flagbackup=F)

# Make amplitude and phase self-calibrated image.
for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(contimagename + '_ap'+ ext)

clean(vis=contvis,
      imagename=contimagename + '_ap',
      field=field,
#      phasecenter=phasecenter, # uncomment if mosaic.
      mode='mfs',
      psfmode='clark',
      imsize = imsize,
      cell= cell,
      weighting = weighting,
      robust=robust,
      niter=niter,
      threshold=threshold,
      interactive=True,
      imagermode=imagermode)

# Note final RMS and number of clean iterations. Compare the RMS to
# the RMS from the earlier, pre-selfcal image.

# Save results of self-cal in a new ms
split(vis=contvis,
      outputvis=contvis+'.selfcal',
      datacolumn='corrected')
'''
########################################
print("Continuum Subtraction for Line Imaging")

# If you have observations that include both line and strong (>3 sigma
# per final line image channel) continuum emission, you need to
# subtract the continuum from the line data. You should not continuum
# subtract if the line of interest is in absorption.

linevis = finalvis+'.contsub'
if not os.path.exists(linevis):
    print("Fitting continuum to create {0}".format(linevis))

    # line-free channel for fitting continuum
    fitspw='0:0~149;401~779;841~959;991~1019;1091~1549;1571~1609;1691~1719;1781~1919,' + \
    '4:0~149;401~779;841~959;991~1019;1091~1549;1571~1609;1691~1719;1781~1919,' + \
    '8:0~149;401~779;841~959;991~1019;1091~1549;1571~1609;1691~1719;1781~1919,' + \
    '12:0~149;401~779;841~959;991~1019;1091~1549;1571~1609;1691~1719;1781~1919,' + \
    '16:0~149;401~779;841~959;991~1019;1091~1549;1571~1609;1691~1719;1781~1919,' + \
    '20:0~149;401~779;841~959;991~1019;1091~1549;1571~1609;1691~1719;1781~1919,' + \
    '1:51~189;451~679;751~1449;1501~1749;1751~3839,' + \
    '5:51~189;451~679;751~1449;1501~1749;1751~3839,' + \
    '9:51~189;451~679;751~1449;1501~1749;1751~3839,' + \
    '13:51~189;451~679;751~1449;1501~1749;1751~3839,' + \
    '17:51~189;451~679;751~1449;1501~1749;1751~3839,' + \
    '21:51~189;451~679;751~1449;1501~1749;1751~3839,' + \
    '2:121~199;299~599;649~749;801~899;951~999;1101~1399;1451~1549;1601~1849;' + \
    '1951~2099;2151~2199;2351~2399;2601~2779;2901~3049;3101~3279;3501~3599;3751~3839,' + \
    '6:121~199;299~599;649~749;801~899;951~999;1101~1399;1451~1549;1601~1849;' + \
    '1951~2099;2151~2199;2351~2399;2601~2779;2901~3049;3101~3279;3501~3599;3751~3839,' + \
    '10:121~199;299~599;649~749;801~899;951~999;1101~1399;1451~1549;1601~1849;' + \
    '1951~2099;2151~2199;2351~2399;2601~2779;2901~3049;3101~3279;3501~3599;3751~3839,' + \
    '14:121~199;299~599;649~749;801~899;951~999;1101~1399;1451~1549;1601~1849;' + \
    '1951~2099;2151~2199;2351~2399;2601~2779;2901~3049;3101~3279;3501~3599;3751~3839,' + \
    '18:121~199;299~599;649~749;801~899;951~999;1101~1399;1451~1549;1601~1849;' + \
    '1951~2099;2151~2199;2351~2399;2601~2779;2901~3049;3101~3279;3501~3599;3751~3839,' + \
    '22:121~199;299~599;649~749;801~899;951~999;1101~1399;1451~1549;1601~1849;' + \
    '1951~2099;2151~2199;2351~2399;2601~2779;2901~3049;3101~3279;3501~3599;3751~3839,' + \
    '3:0~99;151~299;501~639;721~799;1001~1149;1201~1249;1321~1349;1401~1449;2001~2349;2401~2499;2651~2799;2851~3069;3201~3279,' + \
    '7:0~99;151~299;501~639;721~799;1001~1149;1201~1249;1321~1349;1401~1449;2001~2349;2401~2499;2651~2799;2851~3069;3201~3279,' + \
    '11:0~99;151~299;501~639;721~799;1001~1149;1201~1249;1321~1349;1401~1449;2001~2349;2401~2499;2651~2799;2851~3069;3201~3279,' + \
    '15:0~99;151~299;501~639;721~799;1001~1149;1201~1249;1321~1349;1401~1449;2001~2349;2401~2499;2651~2799;2851~3069;3201~3279,' + \
    '19:0~99;151~299;501~639;721~799;1001~1149;1201~1249;1321~1349;1401~1449;2001~2349;2401~2499;2651~2799;2851~3069;3201~3279,' + \
    '23:0~99;151~299;501~639;721~799;1001~1149;1201~1249;1321~1349;1401~1449;2001~2349;2401~2499;2651~2799;2851~3069;3201~3279'


    linespw = '0~23' # line spectral windows. You can subtract the continuum from multiple spectral line windows at once.

    uvcontsub(vis=finalvis,
              spw=linespw, # spw to do continuum subtraction on
              fitspw=fitspw, # select spws to fit continuum. exclude regions with strong lines.
              combine='spw',
              solint='int',
              fitorder=1,
              want_cont=False) # This value should not be changed.

    # NOTE: Imaging the continuum produced by uvcontsub with
    # want_cont=True will lead to extremely poor continuum images because
    # of bandwidth smearing effects. For imaging the continuum, you should
    # always create a line-free continuum data set using the process
    # outlined above.


#########################################################
# Apply continuum self-calibration to line data [OPTIONAL]
'''
spwmap_line = [0] # Mapping self-calibration solution to the individual line spectral windows.
applycal(vis=linevis,
         spwmap=[spwmap_line, spwmap_line], # select which spws to apply the solutions for each table
         field=field,
         gaintable=['pcal3','apcal'],
         gainfield='',
         calwt=F,
         flagbackup=F)

# Save results of self-cal in a new ms and reset the image name.
split(vis=linevis,
      outputvis=linevis+'.selfcal',
      datacolumn='corrected')
linevis=linevis+'.selfcal'

'''
##############################################
# Image line emission [REPEAT AS NECESSARY]

# If you did an mstransform/cvel, use the same velocity parameters in
# the clean that you did for the regridding. If you did not do an
# mstransform and have multiple executions of a scheduling block,
# select the spws with the same rest frequency using the spw parameter
# (currently commented out below). DO NOT INCLUDE SPWS WITH DIFFERENT
# REST FREQUENCIES IN THE SAME RUN OF CLEAN: THEY WILL SLOW DOWN
# IMAGING CONSIDERABLY.

# If necessary, run the following commands to get rid of older clean
# data.

clearcal(vis=linevis)
delmod(vis=linevis)

# velocity parameters
# -------------------

lineimagename = 'source_calibrated_line_image_SiO' # name of line image
print("Cleaning SiO: {0}".format(lineimagename))

start='-240km/s' # start velocity. See science goals for appropriate value.
width='1.46km/s' # velocity width. See science goals.
nchan = 300  # number of channels. See science goals for appopriate value.
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type. See note below.
restfreq='217.10498GHz' # Typically the rest frequency of the line of
                        # interest. If the source has a significant
                        # redshift (z>0.2), use the observed sky
                        # frequency (nu_rest/(1+z)) instead of the
                        # rest frequency of the
                        # line.


# Note on veltype: We recommend keeping veltype set to radio,
# regardless of the velocity frame listed the object in the OT. If the
# sensitivity is defined using a velocity width, then the 'radio'
# definition of the velocity frame is used regardless of the velocity
# definition in the "source parameters" tab of the OT.

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(lineimagename + ext)

clean(vis=linevis,
      imagename=lineimagename,
      field=field,
      spw='2,6,10,14,18,22',
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
      interactive=True,
      cell=cell,
      imsize=imsize,
      weighting=weighting,
      robust=robust,
      imagermode=imagermode,
      usescratch=True)

lineimagename = 'source_calibrated_line_image_H2CO_303_202' # name of line image
print("Cleaning H2CO: {0}".format(lineimagename))

start='-100km/s' # start velocity. See science goals for appropriate value.
width='1.46km/s' # velocity width. See science goals.
nchan = 120  # number of channels. See science goals for appopriate value.
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type. See note below.
restfreq='218.22219GHz' # Typically the rest frequency of the line of
                        # interest. If the source has a significant
                        # redshift (z>0.2), use the observed sky
                        # frequency (nu_rest/(1+z)) instead of the
                        # rest frequency of the
                        # line.


# Note on veltype: We recommend keeping veltype set to radio,
# regardless of the velocity frame listed the object in the OT. If the
# sensitivity is defined using a velocity width, then the 'radio'
# definition of the velocity frame is used regardless of the velocity
# definition in the "source parameters" tab of the OT.

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(lineimagename + ext)

clean(vis=linevis,
      imagename=lineimagename,
      field=field,
      spw='3,7,11,15,19,23',
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
      interactive=True,
      cell=cell,
      imsize=imsize,
      weighting=weighting,
      robust=robust,
      imagermode=imagermode,
      usescratch=True)


lineimagename = 'source_calibrated_line_image_CO' # name of line image
print("Cleaning CO: {0}".format(lineimagename))

start='-240km/s' # start velocity. See science goals for appropriate value.
width='1.46km/s' # velocity width. See science goals.
nchan = 300  # number of channels. See science goals for appopriate value.
outframe='lsrk' # velocity reference frame. See science goals.
veltype='radio' # velocity type. See note below.
restfreq='230.538GHz' # Typically the rest frequency of the line of
                        # interest. If the source has a significant
                        # redshift (z>0.2), use the observed sky
                        # frequency (nu_rest/(1+z)) instead of the
                        # rest frequency of the
                        # line.


# Note on veltype: We recommend keeping veltype set to radio,
# regardless of the velocity frame listed the object in the OT. If the
# sensitivity is defined using a velocity width, then the 'radio'
# definition of the velocity frame is used regardless of the velocity
# definition in the "source parameters" tab of the OT.

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(lineimagename + ext)

clean(vis=linevis,
      imagename=lineimagename,
      field=field,
      spw='0,4,8,12,16,20',
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
      interactive=True,
      cell=cell,
      imsize=imsize,
      weighting=weighting,
      robust=robust,
      imagermode=imagermode,
      usescratch=True)

#niter = 6000, rms 6 mJy

molecules = {'CH3OCHO7(3,5)-6(1,6)E': 217.23756,
            }

spws = {0: '0,4,8,12,16,20',
        1: '1,5,9,13,17,21',
        2: '2,6,10,14,18,22',
        3: '3,7,11,15,19,23',
       }
nchans_total = {0: 1920, 1: 3840, 2: 3840, 3: 3840}
ncubes_per_window = 20
finalvis='calibrated_final.ms'
linevis = finalvis+'.contsub'

for spwnum in '0123':
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
                  outframe = 'LSRK',
                  interactive = F,
                  niter = 2000,
                  imsize = imsize,
                  cell = cell,
                  weighting = 'briggs',
                  phasecenter = phasecenter,
                  robust = 0.5,
                  threshold = threshold,
                  pbcor = F,
                  usescratch= T)
          
        if not os.path.exists(output+".image.pbcor"):
            myimagebase = output
            impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.flux', outfile=myimagebase+'.image.pbcor', overwrite=True)
            exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', overwrite=True)
            exportfits(imagename=myimagebase+'.flux', fitsimage=myimagebase+'.flux.fits', overwrite=True)


# If interactively cleaning (interactive=True), then note number of
# iterations at which you stop for the PI. This number will help the
# PI replicate the delivered images.

# If you'd like to redo your clean, but don't want to make a new mask
# use the following commands to save your original mask. This is an
# optional step.
# linemaskname = 'line.mask'
## rmtables(linemaskname) # uncomment if you want to overwrite the mask.
# os.system('cp -ir ' + lineimagename + '.mask ' + linemaskname)

##############################################
print("Apply a primary beam correction")

import glob

myimages = glob.glob("*.image")

rmtables('*.pbcor')
for image in myimages:
    impbcor(imagename=image, pbimage=image.replace('.image','.flux'), outfile = image.replace('.image','.pbcor'))

##############################################
print("Export the images")

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
