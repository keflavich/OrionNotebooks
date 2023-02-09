# Imaging Script
# 2013.1.00546.S
# Title: The Explosive OMC1 Outflow
# PI: John Bally
# SB: OMC1_SE_a_06_TE
# MOUS: uid___A001_X122_X364
# GOUS: uid___A001_X122_X363
# Pipeline-assisted data reduction

# Preparing Data for Imaging

########################################
# Check CASA version

# CASA version 4.2.2 was used for the pipeline reduction and imaging of these data.
# It's recommended that you use this version to recreate the data, or at least
# not a version earlier than this.  If using version 4.3, it maybe possible to
# comment out the following and run as is, but some parameter names, etc., may have
# changed causing the script to fail.  Consult with your contact scientist through
# the Helpdesk in this case.

import re

if re.search('^4.2', casadef.casa_version) == None:
 sys.exit('ERROR: PLEASE USE THE SAME VERSION OF CASA THAT YOU USED FOR GENERATING THE SCRIPT: 4.2')

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
    listobs(vis=vis)

#Fields: 42
#  ID   Code Name                RA               Decl           Epoch   SrcId      nRows
#  0    none J0607-0834          06:07:59.699230 -08.34.49.97810 J2000   0         133200
#  1    none J0423-013           04:23:15.800726 -01.20.33.06548 J2000   1          66600
#  2    none J0541-0541          05:41:38.083370 -05.41.49.42850 J2000   2         119880
#  4    none OMC1_SE             05:35:15.291906 -05.23.16.46165 J2000   3          31968
#  5    none OMC1_SE             05:35:16.154341 -05.23.16.46195 J2000   3          31968
#  6    none OMC1_SE             05:35:17.016776 -05.23.16.46224 J2000   3          31968
#  7    none OMC1_SE             05:35:17.879211 -05.23.16.46253 J2000   3          31968
#  8    none OMC1_SE             05:35:18.741645 -05.23.16.46283 J2000   3          31968
#  9    none OMC1_SE             05:35:19.604080 -05.23.16.46312 J2000   3          31968
#  10   none OMC1_SE             05:35:15.723141 -05.23.05.30767 J2000   3          31968
#  11   none OMC1_SE             05:35:16.585576 -05.23.05.30796 J2000   3          31968
#  12   none OMC1_SE             05:35:17.448010 -05.23.05.30826 J2000   3          31968
#  13   none OMC1_SE             05:35:18.310445 -05.23.05.30855 J2000   3          31968
#  14   none OMC1_SE             05:35:19.172880 -05.23.05.30884 J2000   3          31968
#  15   none OMC1_SE             05:35:15.291941 -05.22.54.15339 J2000   3          31968
#  16   none OMC1_SE             05:35:16.154375 -05.22.54.15369 J2000   3          31968
#  17   none OMC1_SE             05:35:17.016810 -05.22.54.15398 J2000   3          31968
#  18   none OMC1_SE             05:35:17.879245 -05.22.54.15428 J2000   3          31968
#  19   none OMC1_SE             05:35:18.741679 -05.22.54.15457 J2000   3          31968
#  20   none OMC1_SE             05:35:19.604114 -05.22.54.15486 J2000   3          31968
#  21   none OMC1_SE             05:35:15.723175 -05.22.42.99941 J2000   3          31968
#  22   none OMC1_SE             05:35:16.585610 -05.22.42.99971 J2000   3          31968
#  23   none OMC1_SE             05:35:17.448044 -05.22.43.00000 J2000   3          31968
#  24   none OMC1_SE             05:35:18.310479 -05.22.43.00029 J2000   3          31968
#  25   none OMC1_SE             05:35:19.172914 -05.22.43.00059 J2000   3          31968
#  26   none OMC1_SE             05:35:15.291975 -05.22.31.84514 J2000   3          31968
#  27   none OMC1_SE             05:35:16.154409 -05.22.31.84543 J2000   3          31968
#  28   none OMC1_SE             05:35:17.016844 -05.22.31.84572 J2000   3          31968
#  29   none OMC1_SE             05:35:17.879279 -05.22.31.84602 J2000   3          31968
#  30   none OMC1_SE             05:35:18.741713 -05.22.31.84631 J2000   3          31968
#  31   none OMC1_SE             05:35:19.604148 -05.22.31.84661 J2000   3          31968
#  32   none OMC1_SE             05:35:15.723209 -05.22.20.69116 J2000   3          31968
#  33   none OMC1_SE             05:35:16.585644 -05.22.20.69145 J2000   3          31968
#  34   none OMC1_SE             05:35:17.448078 -05.22.20.69174 J2000   3          31968
#  35   none OMC1_SE             05:35:18.310513 -05.22.20.69204 J2000   3          31968
#  36   none OMC1_SE             05:35:19.172948 -05.22.20.69233 J2000   3          31968
#  37   none OMC1_SE             05:35:15.292009 -05.22.09.53688 J2000   3          31968
#  38   none OMC1_SE             05:35:16.154443 -05.22.09.53717 J2000   3          31968
#  39   none OMC1_SE             05:35:17.016878 -05.22.09.53747 J2000   3          31968
#  40   none OMC1_SE             05:35:17.879313 -05.22.09.53776 J2000   3          31968
#  41   none OMC1_SE             05:35:18.741747 -05.22.09.53805 J2000   3          31968
#  42   none OMC1_SE             05:35:19.604182 -05.22.09.53835 J2000   3          31968
#Spectral Windows:  (4 unique spectral windows and 1 unique polarization setups)
#  SpwID  Name                           #Chans   Frame   Ch0(MHz)  ChanWid(kHz)  TotBW(kHz) BBC Num  Corrs  
#  0      ALMA_RB_06#BB_1#SW-01#FULL_RES   1920   TOPO  230249.215       976.562   1875000.0       1  XX  YY
#  1      ALMA_RB_06#BB_2#SW-01#FULL_RES   1920   TOPO  232046.754       976.562   1875000.0       2  XX  YY
#  2      ALMA_RB_06#BB_3#SW-01#FULL_RES   1920   TOPO  218316.278      -976.562   1875000.0       3  XX  YY
#  3      ALMA_RB_06#BB_4#SW-01#FULL_RES   1920   TOPO  220117.317      -976.562   1875000.0       4  XX  YY



# Doing the split
for vis in vislist:
    sourcevis=vis+'.source'
#    rmtables(sourcevis)
    os.system('rm -rf '+sourcevis)
    split(vis=vis,
          intent='*TARGET*', # split off the target sources
          outputvis=sourcevis,
          datacolumn='data')

    # Check that split worked as desired.
    listobs(vis=sourcevis) 

#Fields: 39
#  ID   Code Name                RA               Decl           Epoch   SrcId      nRows
#  4    none OMC1_SE             05:35:15.291906 -05.23.16.46165 J2000   3          31968
#  5    none OMC1_SE             05:35:16.154341 -05.23.16.46195 J2000   3          31968
#  6    none OMC1_SE             05:35:17.016776 -05.23.16.46224 J2000   3          31968
#  7    none OMC1_SE             05:35:17.879211 -05.23.16.46253 J2000   3          31968
#  8    none OMC1_SE             05:35:18.741645 -05.23.16.46283 J2000   3          31968
#  9    none OMC1_SE             05:35:19.604080 -05.23.16.46312 J2000   3          31968
#  10   none OMC1_SE             05:35:15.723141 -05.23.05.30767 J2000   3          31968
#  11   none OMC1_SE             05:35:16.585576 -05.23.05.30796 J2000   3          31968
#  12   none OMC1_SE             05:35:17.448010 -05.23.05.30826 J2000   3          31968
#  13   none OMC1_SE             05:35:18.310445 -05.23.05.30855 J2000   3          31968
#  14   none OMC1_SE             05:35:19.172880 -05.23.05.30884 J2000   3          31968
#  15   none OMC1_SE             05:35:15.291941 -05.22.54.15339 J2000   3          31968
#  16   none OMC1_SE             05:35:16.154375 -05.22.54.15369 J2000   3          31968
#  17   none OMC1_SE             05:35:17.016810 -05.22.54.15398 J2000   3          31968
#  18   none OMC1_SE             05:35:17.879245 -05.22.54.15428 J2000   3          31968
#  19   none OMC1_SE             05:35:18.741679 -05.22.54.15457 J2000   3          31968
#  20   none OMC1_SE             05:35:19.604114 -05.22.54.15486 J2000   3          31968
#  21   none OMC1_SE             05:35:15.723175 -05.22.42.99941 J2000   3          31968
#  22   none OMC1_SE             05:35:16.585610 -05.22.42.99971 J2000   3          31968
#  23   none OMC1_SE             05:35:17.448044 -05.22.43.00000 J2000   3          31968
#  24   none OMC1_SE             05:35:18.310479 -05.22.43.00029 J2000   3          31968
#  25   none OMC1_SE             05:35:19.172914 -05.22.43.00059 J2000   3          31968
#  26   none OMC1_SE             05:35:15.291975 -05.22.31.84514 J2000   3          31968
#  27   none OMC1_SE             05:35:16.154409 -05.22.31.84543 J2000   3          31968
#  28   none OMC1_SE             05:35:17.016844 -05.22.31.84572 J2000   3          31968
#  29   none OMC1_SE             05:35:17.879279 -05.22.31.84602 J2000   3          31968
#  30   none OMC1_SE             05:35:18.741713 -05.22.31.84631 J2000   3          31968
#  31   none OMC1_SE             05:35:19.604148 -05.22.31.84661 J2000   3          31968
#  32   none OMC1_SE             05:35:15.723209 -05.22.20.69116 J2000   3          31968
#  33   none OMC1_SE             05:35:16.585644 -05.22.20.69145 J2000   3          31968
#  34   none OMC1_SE             05:35:17.448078 -05.22.20.69174 J2000   3          31968
#  35   none OMC1_SE             05:35:18.310513 -05.22.20.69204 J2000   3          31968
#  36   none OMC1_SE             05:35:19.172948 -05.22.20.69233 J2000   3          31968
#  37   none OMC1_SE             05:35:15.292009 -05.22.09.53688 J2000   3          31968
#  38   none OMC1_SE             05:35:16.154443 -05.22.09.53717 J2000   3          31968
#  39   none OMC1_SE             05:35:17.016878 -05.22.09.53747 J2000   3          31968
#  40   none OMC1_SE             05:35:17.879313 -05.22.09.53776 J2000   3          31968
#  41   none OMC1_SE             05:35:18.741747 -05.22.09.53805 J2000   3          31968
#  42   none OMC1_SE             05:35:19.604182 -05.22.09.53835 J2000   3          31968
#Spectral Windows:  (4 unique spectral windows and 1 unique polarization setups)
#  SpwID  Name                           #Chans   Frame   Ch0(MHz)  ChanWid(kHz)  TotBW(kHz) BBC Num  Corrs  
#  0      ALMA_RB_06#BB_1#SW-01#FULL_RES   1920   TOPO  230249.215       976.562   1875000.0       1  XX  YY
#  1      ALMA_RB_06#BB_2#SW-01#FULL_RES   1920   TOPO  232046.754       976.562   1875000.0       2  XX  YY
#  2      ALMA_RB_06#BB_3#SW-01#FULL_RES   1920   TOPO  218316.278      -976.562   1875000.0       3  XX  YY
#  3      ALMA_RB_06#BB_4#SW-01#FULL_RES   1920   TOPO  220117.317      -976.562   1875000.0       4  XX  YY

############################################
# Rename and backup data set

os.system('mv -i ' + sourcevis + ' ' + 'calibrated_final.ms')
os.system('cp -ir calibrated_final.ms calibrated_final.ms.backup')


###########################
#  Continuum Imaging

# Identify spectral lines in spectral windows

##################################################
# Identify Line-free SPWs and channels

finalvis='calibrated_final.ms' # This is your output ms from the data
                               # preparation script.

# Use plotms to identify line and continuum spectral windows
plotms(vis=finalvis, xaxis='channel', yaxis='amplitude',
       ydatacolumn='data',
       avgtime='1e8', avgscan=True, avgchannel='2',
       iteraxis='spw' )

# Wow.  Line forest is right.
# The following is a very rough estimate of where the "line-free" regions are based
# on the plotms output and is by no means definitive.
#
# Channels with line emission:
#
# spw 0:
# 40~60,9~110,18~370,470~500,690~710,730~840,960~1120,1260~1280,1480~1800,1840~1860
# spw 1:
# 0~20,90~220,300~320,350~390,470~490,720~760,880~1120,1140~1200,1230~1280,1310~1380,1400~1530,1560~1640,1720~1780,1820~1840,1860~1880
# spw 2:
# 0~60,95~140,300~320,380~400,450~470,500~550,700~720,780~800,950~970,1050~1070,1110~1140,1220~1300,1390~1440,1520~1550,1640~1760,1800~1860
# spw 3:
# 50~70,160~260,330~360,390~430,480~500,570~600,630~660,680~700,740~760,780~840,860~940,970~1000,1170~1200,1240~1330,1380~1440,1480~1500,1540~1610,1640~1800,1830~1910

#  Flagging complex line emission prior to continuum imaging.
#
# Set continuum spws based on plotms output.
contspws = '0,1,2,3'

flagmanager(vis=finalvis,mode='save',
            versionname='before_cont_flags')

# Flag channels as in the mess above 

flagchannels='0:40~60,0:95~110,0:180~370,0:470~500,0:620~630,0:690~710,0:730~840,0:960~1120,0:1260~1280,0:1480~1800,0:1840~1860,0:1900~1910,1:0~20,1:90~220,1:300~320,1:350~390,1:470~490,1:720~760,1:880~1120,1:1140~1200,1:1230~1280,1:1310~1380,1:1400~1530,1:1560~1640,1:1700~1780,1:1820~1840,1:1860~1880,1:1890~1900,2:0~60,2:95~140,2:205~215,2:300~320,2:380~400,2:450~470,2:500~550,2:700~720,2:780~800,2:850~860,2:920~970,2:1040~1070,2:1110~1150,2:1160~1180,2:1220~1300,2:1340~1350,2:1390~1440,2:1520~1550,2:1610~1630,2:1640~1760,2:1800~1860,3:50~70,3:140~260,3:330~360,3:390~440,3:470~500,3:570~600,3:630~660,3:680~700,3:740~760,3:780~840,3:860~940,3:970~1000,3:1170~1200,3:1240~1330,3:1380~1440,3:1480~1500,3:1540~1610,3:1640~1800,3:1830~1910'

flagdata(vis=finalvis,mode='manual',
          spw=flagchannels,flagbackup=False)

# check that flags are as expected, NOTE must check reload on plotms
# gui if it's still open.
plotms(vis=finalvis,yaxis='amp',xaxis='channel',
       avgchannel='2',avgtime='1e8',avgscan=True,iteraxis='spw') 

# Average the channels within spws
contvis='calibrated_final_cont.ms'
rmtables(contvis)
os.system('rm -rf ' + contvis + '.flagversions')
split(vis=finalvis,
      spw=contspws,      
      outputvis=contvis,
      width=1920, # number of channels to average together
      datacolumn='data')

# Restore the flags
flagmanager(vis=finalvis,mode='restore',
            versionname='before_cont_flags')

# Continuum image
# There are sources and extended emission all over the emission, with a large dynamic range.
# Cleaning over whole image.
# Synthesized beam 1.84"x0.75" (Bragg weighting, robust=0.5)
# 10 cycles of 100; cleaned 3.16Jy
# RMS 0.5 mJy (over the rather indeterminate bandwidth, something less than 7.5 GHz)
# These data would probably benefit from self-Cal and are missing significant low-order spacings

clean(vis='calibrated_final_cont.ms',    # using split off continuum data
      imagename='OMC1-SE-cont',
      field='4~42',                      # 39 centre mosaic
      spw='0~3',                         # using all four spectral windows (pre-averaged)
      mode='mfs',                        # continuum imaging
      niter=1000,                        
      interactive=True,
      npercycle=100,
      mask='OMC1-SE-cont.mask',          # Mask covers entire image
      imagermode='mosaic',               # mosaic mode
      cell=['0.2arcsec'],
      imsize=[1024,1024],                  # map size 3.4'x3.4'
      phasecenter='23',                  # field ID 23 is the mosaic center
      weighting='briggs',
      robust=0.5)                         # Briggs weighting, robust=0.5
      
# Subtract continuum from line data

fitspw='0:0~40,0:60~95,0:110~180,0:370~470,0:500~620,0:630~690,0:710~730,0:840~960,0:1120~1260,0:1280~1480,0:1800~1840,0:1860~1900,1:20~90,1:220~300,1:320~350,1:390~470,1:490~720,1:760~880,1:1120~1140,1:1200~1230,1:1280~1310,1:1380~1400,1:1530~1560,1:1640~1700,1:1780~1820,1:1840~1860,1:1880~1890,2:60~95,2:140~205,2:215~300,2:320~380,2:400~450,2:470~500,2:550~700,2:720~780,2:800~850,2:860~920,2:970~1040,2:1070~1110,2:1150~1160,2:1180~1220,2:1300~1340,2:1350~1390,2:1440~1520,2:1550~1610,2:1630~1640,2:1760~1800,2:1860~1910,3:0~50,3:70~140,3:260~330,3:360~390,3:440~470,3:500~570,3:600~630,3:660~680,3:700~740,3:760~780,3:840~860,3:940~970,3:1000~1170,3:1200~1240,3:1330~1380,3:1440~1480,3:1500~1540,3:1610~1640,3:1800~1830'       # The inverse of the spectral line flagging regions.
linespw='0~3'

uvcontsub(vis=finalvis,
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

# Imaging line data.
# Note: there are a *lot* of faint lines in each SPW. I will just image representative cubes from each according to the lines requested in the proposal: CO 2-1 (SPW 0, 230.538 GHz), SiO (SPW 2, 217.105 GHz), and SO (SPW 3, 219.949 GHz). 

# 12CO J=2-1 (spw 1, 230.538GHz, resolution 1.129MHz (1.464 km/s)
# Channel-by-channel clean mask stored as 'OMC1-SE-CO21.mask'
# synthesized beamsize 1.82"x0.73"  (requested angular resolution 1")
# Cleaned for 10 cycles of 100
# Cleaned a total of 1691Jy, RMS 6.2mJy per channel (requested 6.8 mJy)
# 

clean(vis='calibrated_final.ms.contsub',    # continuum subtracted
      imagename='OMC1-SE-CO21',
      field='4~42',
      spw='0',
      mode='velocity',
      nchan=200,
      start='-137.0km/s',
      width='1.464km/s',
      outframe='lsrk',
      veltype='radio',
      niter=1000,
      threshold='0.0mJy',                   # set via interactive clean
      imagermode='mosaic',
      interactive=True,
      npercycle=100,
      mask='OMC1-SE-CO21.mask',                              # set interactively
      imsize=[1024,1024],
      cell=['0.2arcsec'],
      phasecenter='23',
      restfreq='230.538GHz',
      weighting='briggs',
      robust=0.5,
      usescratch=True)

# SiO v=0 J=5-4 (217.105GHz)
# Channel-by-channel clean mask stored as 'OMC1-SE-SiO54.mask'
# Synthesized beam (Briggs weighting, robust=0.5) 1.94"x0.78"
# five cycles of 100 clean iterations
# cleaned 613 Jy
# RMS 5.1 mJy

clean(vis='calibrated_final.ms.contsub',    # continuum subtracted
      imagename='OMC1-SE-SiO54',
      field='4~42',
      spw='2',
      mode='velocity',
      nchan=110,
      start='-72.0km/s',
      width='1.557km/s',                    # 1.129 MHz resolution
      outframe='lsrk',
      veltype='radio',
      niter=1000,
      threshold='0.0mJy',                   # set via interactive clean
      imagermode='mosaic',
      interactive=True,
      npercycle=100,
      mask='OMC1-SE-SiO54.mask',            # set interactively
      imsize=[1024,1024],
      cell=['0.2arcsec'],
      phasecenter='23',
      restfreq='217.105GHz',
      weighting='briggs',
      robust=0.5,
      usescratch=True)

# SO v=0 J=6(5)-5(5) (219.949GHz)
# synthesized beam size (Briggs weighting, robust=0.5) 1.90"x0.76"
# 5 cycles of 100 iterations
# cleaned 672 Jy
# RMS 7.0 mJy

clean(vis='calibrated_final.ms.contsub',    # continuum subtracted
      imagename='OMC1-SE-SO65',
      field='4~42',
      spw='3',
      mode='velocity',
      nchan=110,
      start='-72.0km/s',
      width='1.557km/s',                    # 1.129 MHz resolution
      outframe='lsrk',
      veltype='radio',
      niter=1000,
      threshold='0.0mJy',                   # set via interactive clean
      imagermode='mosaic',
      interactive=True,
      npercycle=100,
      mask='OMC1-SE-SO65.mask',            # set interactively
      imsize=[1024,1024],
      cell=['0.2arcsec'],
      phasecenter='23',
      restfreq='219.949GHz',
      weighting='briggs',
      robust=0.5,
      usescratch=True)

##############################################
# Apply a primary beam correction

import glob

myimages = glob.glob("*.image")

rmtables('*.pbcor')
for image in myimages:
    impbcor(imagename=image, pbimage=image.replace('.image','.flux'), outfile = image.replace('.image','.pbcor'))


##############################################
# Export the images and mask files

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

myimages = glob.glob("*.mask")
for image in myimages:
    exportfits(imagename=image, fitsimage=image+'.fits',overwrite=True) 

