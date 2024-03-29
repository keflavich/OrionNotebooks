# Copyright(c) 2012 Association of Universities for Research in Astronomy, Inc.

###############################################################################
# Gemini GSAOI example data reduction script                                  #
# Typical reduction for: Science and Calibration Data                         #
#                                                                             #
# This script is provided to guide the user through the GSAOI data reduction  #
# process and may not be optimized to give the best results. It shows the     #
# reduction steps using GSAOI data and provides explanatory comments at each  #
# step.                                                                       #
#                                                                             #
# It is strongly recommended that the user read the embedded comments and     #
# understand the processing steps, since the optimum steps for a given        #
# dataset may differ, e.g., improved cleaning of cosmic rays and bad pixels   #
# and improved signal-to-noise will most likely be possible. The user can     #
# then edit this script to match their dataset.                               #
#                                                                             #
# Once this script has been properly edited, it can be run by copying and     #
# pasting each command into an IRAF or PyRAF session, or by defining this     #
# script as a task by typing:                                                 #
#                                                                             #
#   ecl> task $thisscript="thisscript.cl"                                     #
#   ecl> thisscript                                                           #
#                                                                             #
# in the IRAF or PyRAF session. It is NOT recommended to run this script      #
# using redirection i.e., cl < thisscript.cl.                                 #
#                                                                             #
# Note that this script is designed to be re-run as needed, so each step is   #
# preceded by a command to delete the files created in that step.             #
###############################################################################

# The data files have been separated by filter and exposure time, where
# appropriate. This information can be found in the primary header unit (PHU)
# of each data file. The imhead or fitsutil.fxhead tasks can be used to view
# the header information in the PHU (or any other extension) of the data file. 
# The hselect task can be used to obtain specific keyword values from the
# headers. Read the help files for these tasks for more information.
#
# Dataset:
#
# Note: This is commissioning data and will be updated with more recent data
# when available.
#
# Observation UT date : 2012 Apr 27
# Data filename prefix: S20120427S
# File numbers -
#   Darks             : 8-18           (10s)
#
# Observation UT date : 2012 Apr 10
# Data filename prefix: S20120410S
# File numbers -
#   Dome flats        : 121-127        (Kshort_G1105, 15s)
#
# Observation UT date : 2012 Jan 08
# Data filename prefix: S20120108S
# File numbers -
#   Sky images        : 34,37,42       (Kshort_G1105, 10s)
#   Science images    : 33,35-36,38-41 (Kshort_G1105, 10s)
# 
# Observation UT Date : 2013 Feb 01
# 

###############################################################################
# STEP 1: Initialize the required packages                                    #
###############################################################################

# Load the required packages
gemini
gsaoi

# If copying and pasting these commands into an interactive PyRAF session, use
# the following lines to import the required packages
#from pyraf.iraf import gemini
#from pyraf.iraf import gsaoi

# Use the default parameters except where specified on command lines below
print ("\nEXAMPLE: Unlearning tasks")
unlearn ("gemini")
unlearn ("gsaoi")

###############################################################################
# STEP 2: Define any variables, the database and the logfile                  #
###############################################################################

# Define any variables (not required if copying and pasting into an interactive
# PyRAF session)
string rawdir, image
int num
struct *scanfile

# Define the logfile
gsaoi.logfile = "gsaoi_imaging_example.log"

# To start from scratch, delete the existing logfile
printf ("EXAMPLE: Deleting %s\n", gsaoi.logfile)
delete (gsaoi.logfile, verify=no)

# To start from scratch, delete the existing database files

# Define the directory where the raw data is located
# Don't forget the trailing slash!
rawdir = "./"
printf ("EXAMPLE: Raw data is located in %s\n", rawdir)

###############################################################################
# STEP 3: Create the reduction lists                                          #
###############################################################################

delete ("h2obj.lis,h2sky.lis,h2flat.lis,h2dark.lis,h2all.lis", verify=no)
delete ("feobj.lis,fesky.lis,feflat.lis,fedark.lis,feall.lis", verify=no)
delete ("ksobj.lis,kssky.lis,ksflat.lis,ksdark.lis,ksall.lis", verify=no)

# The user should edit the parameter values in the gemlist calls below to match
# their own dataset.
print ("EXAMPLE: Creating the reduction lists")
gemlist "S20130131S" "68-72" > "feobj.lis"
gemlist "S20130131S" "63-67" > "ksobj.lis"
gemlist "S20130131S" "47-50,52" > "h2obj.lis" # 51 is bad
gemlist "S20130201S" "101-110" > "ksflat.lis"
gemlist "S20130201S" "131-138" > "h2flat.lis"
gemlist "S20130201S" "61-70" > "feflat.lis"
gemlist "S20130131S" "53-57" > "h2sky.lis" 
gemlist "S20130131S" "58-62" > "kssky.lis" 
gemlist "S20130131S" "73-78" > "fesky.lis" 
#gemlist "S20130131S" "34,37,42" > "sky.lis"
#gemlist "S20130131S" "8-18" > "dark.lis"

concat ("h2obj.lis,h2sky.lis,h2flat.lis,h2dark.lis", "all.lis")
concat ("feobj.lis,fesky.lis,feflat.lis,fedark.lis", "all.lis")
concat ("ksobj.lis,kssky.lis,ksflat.lis,ksdark.lis", "all.lis")
#concat ("obj.lis","all.lis")

###############################################################################
# STEP 4: Visually inspect the data                                           #
###############################################################################

# Visually inspect all the data. In addition, all data should be visually
# inspected after every processing step. Once the data has been prepared, it is
# recommended to use the syntax [EXTNAME,EXTVER] e.g., [SCI,1], when defining
# the extension.

# Please make sure a display tool (e.g., ds9, ximtool) is already open.

#gadisplay ("@h2obj.lis", 1, fl_imexam=no, time_gap=5)
#gadisplay ("@ksobj.lis", 1, fl_imexam=no, time_gap=5)
#gadisplay ("@feobj.lis", 1, fl_imexam=no, time_gap=5)
#gadisplay ("@all.lis", 1, fl_imexam=no, time_gap=5)

# If 'fl_imexam' is set to yes, 'time_gap' is ignored.

###############################################################################
# NOTE:
#
#     Most of the tasks can handle wild cards and are able to determine whether
#     the input files are appropriate for that task. This is partly due to the
#     METACONF keyword in prepared files. The METACONF will also be used to
#     sort valid inputs into appropriate groups to be acted upon separately.
#     The help for gaprepare gives a description of the METACONF keyword.
#
###############################################################################

###############################################################################
# STEP 5: Create master dark image                                            #
###############################################################################

# imdelete ("g//@dark.lis,gS________S0008_dark.fits", verify=no)

# It is unlikely that dark subtraction with a master dark will be required due
# to the low dark current within GSAOI and should be easily handled by the sky
# subtraction. However, for completeness the creation of a master dark is shown
# here.

# GADARK has some smart sorting capabilities, as such wild cards can be
# supplied if desired, e.g., "*.fits". It is also possible to define a minimum
# number of  darks to combine 'mindark' and sort by relative time from the
# first image in the input list and subsequent sorted lists (within the same
# call). The latter means more than one master dark could be created in one
# call, from the input list for this example. Finally, all inputs are sorted by
# their METACONF keyword. Only darks with the same exposure time for a given
# configuration will be combined.

# The inputs are raw and as such gaprepare will be called with the parameters
# set in the gadark parameters relating to gaprepare. By default the inputs
# will be trimmed ('fl_trim'), non-linear corrected ('fl_nlc') and non-linear
# and saturated pixels will be flagged in the DQ planes ('fl_sat').

# gadark ("@dark.lis", fl_vardq=yes, fl_dqprop=yes)

# The output in this example is "gS________S0008_dark.fits"

###############################################################################
# STEP 6: Create a master flat image                                          #
###############################################################################

imdelete ("g//@flat.lis,gS20130201SS0121_flat.fits", verify=no)

# GAFLAT has some smart sorting capabilities, as such wild cards can be
# supplied if desired, e.g., "*.fits". It is also possible to define a minimum
# number of flats to combine 'minflat' and sort by relative time from the first
# image in the input list and subsequent sorted lists (within the same
# call). The latter means more than one master flat could be created in one
# call, from the input list for this example. Finally, all inputs are sorted by
# their METACONF keyword.

# The inputs are raw and as such gaprepare will be called with the parameters
# set in the gaflat parameters relating to gaprepare. By default the inputs
# will be trimmed ('fl_trim'), non-linear corrected ('fl_nlc') and non-linear
# and saturated pixels will be flagged in the DQ planes ('fl_sat').

# GCAL flats require that there are both shutter open and shutter closed
# flats. Their number need not match but there must be more than 'minflat' for
# each type. By default, for GCAL and dome flats only images with the same
# exposure time will be combined. However, for twilight flats their exposure
# time will be ignored.

gaflat ("@h2flat.lis", fl_vardq=yes, fl_dqprop=yes)
gaflat ("@ksflat.lis", fl_vardq=yes, fl_dqprop=yes)
gaflat ("@feflat.lis", fl_vardq=yes, fl_dqprop=yes)

# The output in this example is "gS________S0121_flat.fits"

###############################################################################
# STEP 7: Create a master sky frame                                           #
###############################################################################

imdelete ("g//@h2sky.lis,rg//@h2sky.lis,gS20130201S0131_h2sky.fits", verify=no)
imdelete ("g//@kssky.lis,rg//@kssky.lis,gS20130201S0131_kssky.fits", verify=no)
imdelete ("g//@fesky.lis,rg//@fesky.lis,gS20130201S0131_fesky.fits", verify=no)

# Call gaprepare to prepare the sky frames. Flagging saturated pixels in the DQ
# planes. By default the inputs will be trimmed ('fl_trim'), non-linear
# corrected ('fl_nlc') and non-linear and saturated pixels will be flagged in
# the DQ planes ('fl_sat').

gaprepare ("@h2sky.lis", fl_vardq=yes)
gaprepare ("@kssky.lis", fl_vardq=yes)
gaprepare ("@fesky.lis", fl_vardq=yes)

# This will produce files with the same name as the input but prefixed with "g"
# (by default).

# For this example, i.e., if dark subtracting the sky images, the sky
# images should be dark subtracted before combing to create a master sky frame.
# Do not convert them to electrons 'fl_mult'.

gareduce ("g@h2sky.lis", fl_vardq=yes, fl_dqprop=yes, fl_mult=no)
gareduce ("g@kssky.lis", fl_vardq=yes, fl_dqprop=yes, fl_mult=no)
gareduce ("g@fesky.lis", fl_vardq=yes, fl_dqprop=yes, fl_mult=no)

# All inputs to gasky are sorted by their METACONF keyword, in this example
# all of the the input to gasky have the same METACONF value. Supply the master
# flat image to use whilst partially reducing the the sky frames during source
# detection.

gasky ("g//@h2sky.lis", outimage="h2sky.fits", fl_vardq=yes, \
    fl_dqprop=yes, flatimg="gS20130201S0131_flat.fits", logfile='h2_logfile')
gasky ("g//@fesky.lis", outimage="fesky.fits", fl_vardq=yes, \
    fl_dqprop=yes, flatimg="gS20130201S0061_flat.fits", logfile='fe_logfile')
gasky ("g//@kssky.lis", outimage="kssky.fits", fl_vardq=yes, \
    fl_dqprop=yes, flatimg="gS20130201S0101_flat.fits", logfile='ks_logfile')

# The output in this example is "gS20130201S0131_h2sky.fits"

###############################################################################
# STEP 8: Reduce science images                                               #
###############################################################################

imdelete ("g//@h2obj.lis,rg//@h2obj.lis", verify=no)

# In this example the master dark and master flat images are found
# automatically from within the current working directory ('calpath'). It is
# possible to supply them directly with the 'dark' and 'flat' parameters. It
# may be appropriate to change the 'fl_calrun' to yes, should more dark or flat
# images have been created since the last time gareduce has been run.

# The inputs are raw and as such gaprepare will be called with the parameters
# set in the gaflat parameters relating to gaprepare. By default the inputs
# will be trimmed ('fl_trim'), non-linear corrected ('fl_nlc') and non-linear
# and saturated pixels will be flagged in the DQ planes ('fl_sat').

# By default the output will be converted to electrons.

#gareduce ("@h2obj.lis", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0131_flat.fits", fl_sky=yes, fl_flat=yes, skyimg="h2sky.fits", calpath="./")
#gareduce ("@feobj.lis", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0061_flat.fits", fl_sky=yes, fl_flat=yes, skyimg="fesky.fits", calpath="./")
#gareduce ("@ksobj.lis", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0101_flat.fits", fl_sky=yes, fl_flat=yes, skyimg="kssky.fits", calpath="./")

gareduce ("@h2obj.lis", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0131_flat.fits", fl_sky=no, fl_flat=yes, skyimg="h2sky.fits", calpath="./")
gareduce ("@feobj.lis", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0061_flat.fits", fl_sky=no, fl_flat=yes, skyimg="fesky.fits", calpath="./")
gareduce ("@ksobj.lis", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0101_flat.fits", fl_sky=no, fl_flat=yes, skyimg="kssky.fits", calpath="./")

# The outputs will, by default, have names the same as the inputs but prefixed
# with "rg".

# It is possible to perform the above call in more than one step, i.e.,
# gareduce will not complain if the file has passed through gareduce before, so
# long as there is one requested action that has not already be applied to the
# input image.

# It is also possible to use the input science frames as sky images in the same
# call. This is done by setting 'skyimg' to "time" or "distance". The former
# will sort the input images according to the 'maxtime' value either side
# of the current image, in seconds, to be used to create a sky image for that
# file. The latter will sort the input images according to distance beyond
# 'minoffs', in arc seconds, from the current image to create a sky image for
# that image. In either case there must be 'minsky' frames selected by the
# sorting to create a sky frame for the current image being reduced.

###############################################################################
# STEP 9: Mosaic reduced science images                                       #
###############################################################################

imdelete ("mrg//@h2obj.lis", verify=no)

# Mosaic the four individual data extensions into one extension. This is done
# for each of the extensions within the image, e.g., "SCI", "VAR" and "DQ".

gamosaic ("rg@h2obj.lis", fl_vardq=yes)
gamosaic ("rg@feobj.lis", fl_vardq=yes)
gamosaic ("rg@ksobj.lis", fl_vardq=yes)

imcopy ("mrgS20130131S0065.fits[SCI]", "mask.fits[type=mask]")
hedit ("mrgS20130131S00*fits[SCI]","BPM","mask.fits", add=yes, ver=no)

# This, by default, will create files with names the same as the input with "m"
# prefixed to them.

#hedit("mrgS20130131S0048.fits[SCI]", "CRPIX1",  2102.29218917 , ver=no)
#hedit("mrgS20130131S0048.fits[SCI]", "CRPIX2",  2974.35484079 , ver=no)
#hedit("mrgS20130131S0049.fits[SCI]", "CRPIX1",  2107.99148106 , ver=no)
#hedit("mrgS20130131S0049.fits[SCI]", "CRPIX2",  2966.49542506 , ver=no)
#hedit("mrgS20130131S0050.fits[SCI]", "CRPIX1",  2121.19466364 , ver=no)
#hedit("mrgS20130131S0050.fits[SCI]", "CRPIX2",  2960.47588239 , ver=no)
#hedit("mrgS20130131S0052.fits[SCI]", "CRPIX1",  2112.91756148 , ver=no)
#hedit("mrgS20130131S0052.fits[SCI]", "CRPIX2",  2968.31566533 , ver=no)

for(n=47;n<=52;n+=1)
{
    if (n != 51) {
        ccfind("coords","found"//str(n), "mrgS20130131S00"//str(n)//".fits[SCI]", usewcs=yes)
        ccmap("found"//str(n), "ccmap"//str(n)//".db", images="mrgS20130131S00"//str(n)//".fits[SCI]", xcol=3, ycol=4, lngcol=1, latcol=2)
    }
}

imcombine ("mrg//@h2obj.lis//\[SCI]", "H2_Jan31_comb.fits", combine="median", offset="wcs", masktype="badvalue")
imcombine ("mrg//@ksobj.lis//\[SCI]", "ks_Jan31_comb.fits", combine="median", offset="wcs", masktype="badvalue")
imcombine ("mrg//@feobj.lis//\[SCI]", "fe_Jan31_comb.fits", combine="median", offset="wcs", masktype="badvalue")



imcopy ("mrg//@h2obj.lis//\[SCI]","mrg//@h2obj.lis//_SCI")

###############################################################################
# STEP 10: Tidy up                                                            #
###############################################################################

delete ("obj.lis,sky.lis,flat.lis,dark.lis,all.lis", verify=no)

###############################################################################
# Finished!                                                                   #
###############################################################################
