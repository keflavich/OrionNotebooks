# Copyright Adam.  I wrote most of this anyway.
# Observation UT date : 2013 Feb 28

###############################################################################
# STEP 1: Initialize the required packages                                    #
###############################################################################

# Load the required packages
gemini
gemini112beta # calculon
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
logfile = "Feb28data_GEMS_h2feks.log"
gsaoi.logfile = logfile

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

delete ("h2obj.lis,h2sky.lis,h2all.lis", verify=no)
delete ("feobj.lis,fesky.lis,feall.lis", verify=no)
delete ("ksobj.lis,kssky.lis,ksall.lis", verify=no)

# The user should edit the parameter values in the gemlist calls below to match
# their own dataset.
print ("EXAMPLE: Creating the reduction lists")
gemlist "S20130228S" "151,153-156" > "feobj.lis"
gemlist "S20130228S" "145-150" > "ksobj.lis"
gemlist "S20130228S" "130,131,133-135" > "h2obj.lis" # 132 is missing
#gemlist "S20130201S" "" > "ksflat.lis"
#gemlist "S20130201S" "" > "h2flat.lis"
#gemlist "S20130201S" "" > "feflat.lis"
gemlist "S20130228S" "136-140" > "h2sky.lis" 
gemlist "S20130228S" "141-145" > "kssky.lis" 
gemlist "S20130228S" "157-161" > "fesky.lis" 
#gemlist "S20130228S" "34,37,42" > "sky.lis"
#gemlist "S20130228S" "8-18" > "dark.lis"

concat ("h2obj.lis,h2sky.lis", "h2all.lis")
concat ("feobj.lis,fesky.lis", "feall.lis")
concat ("ksobj.lis,kssky.lis", "ksall.lis")
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

#imdelete ("g//@h2flat.lis,gS20121220S0332_flat.fits", verify=no)
#imdelete ("g//@feflat.lis,gS20121220S0262_flat.fits", verify=no)
#imdelete ("g//@ksflat.lis,gS20121220S0302_flat.fits", verify=no)

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

#gaflat ("@h2flat.lis", fl_vardq=yes, fl_dqprop=yes)
#gaflat ("@ksflat.lis", fl_vardq=yes, fl_dqprop=yes)
#gaflat ("@feflat.lis", fl_vardq=yes, fl_dqprop=yes)

# The output in this example is "gS________S0121_flat.fits"

###############################################################################
# STEP 7: Create a master sky frame                                           #
###############################################################################

imdelete ("g//@h2sky.lis,rg//@h2sky.lis,gS20130201S0131_h2sky.fits,h2sky.fits", verify=no)
imdelete ("g//@kssky.lis,rg//@kssky.lis,gS20130201S0131_kssky.fits,kssky.fits", verify=no)
imdelete ("g//@fesky.lis,rg//@fesky.lis,gS20130201S0131_fesky.fits,fesky.fits", verify=no)

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

gamosaic ("h2sky.fits", fl_vardq=yes, fl_paste=no, fl_fluxcon=yes) #colgap=147, linegap=147, 

# The output in this example is "gS20130201S0131_h2sky.fits"

###################
# SOLVE WCS!! #####
###################

#msctpeak S20130228S0047[1].fits muench.txt msctpeak.db
#msctpeak S20130228S0047[2].fits muench.txt msctpeak.db
#msctpeak S20130228S0047[3].fits muench.txt msctpeak.db
#msctpeak S20130228S0047[4].fits muench.txt msctpeak.db
#msctpeak S20130228S0048[1].fits muench.txt msctpeak.db
#msctpeak S20130228S0048[2].fits muench.txt msctpeak.db
#msctpeak S20130228S0048[3].fits muench.txt msctpeak.db
#msctpeak S20130228S0048[4].fits muench.txt msctpeak.db
#msctpeak S20130228S0049[1].fits muench.txt msctpeak.db
#msctpeak S20130228S0049[2].fits muench.txt msctpeak.db
#msctpeak S20130228S0049[3].fits muench.txt msctpeak.db
#msctpeak S20130228S0049[3].fits muench.txt msctpeak.db
#msctpeak S20130228S0049[4].fits muench.txt msctpeak.db
#msctpeak S20130228S0050[4].fits muench.txt msctpeak.db
#msctpeak S20130228S0050[1].fits muench.txt msctpeak.db
#msctpeak S20130228S0050[2].fits muench.txt msctpeak.db
#msctpeak S20130228S0050[3].fits muench.txt msctpeak.db
#msctpeak S20130228S0052[1].fits muench.txt msctpeak.db
#msctpeak S20130228S0052[2].fits muench.txt msctpeak.db
#msctpeak S20130228S0052[3].fits muench.txt msctpeak.db
#msctpeak S20130228S0052[4].fits muench.txt msctpeak.db


# my personal solver
#for fn in glob.glob("*_imexam.log"):
#    try: 
#        e = int(ext.findall(fn)[0])
#        n = int(fnum.findall(fn)[0])
#        fullname = "S20130228S%04i.fits[%i]" % (n,e)
#        fit_coords.fit_coords(fullname, "s%i_%i_" % (n,e), interactive=False, pixmapextension="2")
#    except:
#        print "skipped ",fn
#        pass








###############################################################################
# STEP 8: Reduce science images                                               #
###############################################################################

imdelete ("g//@h2obj.lis,rg//@h2obj.lis", verify=no)
imdelete ("g//@ksobj.lis,rg//@ksobj.lis", verify=no)


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

# The sky frames are 1/3 the exposure time, therefore need to multiply by 3 before subtracting
# however, sky subtraction clearly makes everything worse - just adds noise.

# because average, not product, don't need to do any multiplication
# gemexpr("a*3",output="h2sky_mult.fits",a="h2sky.fits",var_expr="a[VAR]*9",fl_vardq=yes)
# hedit("h2sky.fits[0]",fields="METACONF",value='78._16_3+Clear_H2(1-0)_G1121+SKY+FF+TRIM+NLC',verify=no)
# gemexpr("a*3",output="kssky_mult.fits",a="kssky.fits",var_expr="a[VAR]*9",fl_vardq=yes)
#oldhedit("kssky.fits[0]",fields="METACONF",value='43.4_16_3+Clear_ks(1-0)_G1121+SKY+FF+TRIM+NLC',verify=no)
hedit("kssky.fits[0]",fields="METACONF",value='15._2_3+Kcntshrt_G1111_Clear+SKY+FF+TRIM+NLC',verify=no)
#                                              15._2_3+Kcntshrt_G1111_Clear+OBJ_fg+FF+TRIM+NLC
# gemexpr("a*3",output="fesky_mult.fits",a="fesky.fits",var_expr="a[VAR]*9",fl_vardq=yes)
hedit("fesky.fits[0]",fields="METACONF",value='44.5_16_3+Clear_FeII_G1118+SKY+FF+TRIM+NLC',verify=no)

#gareduce ("@h2obj.lis", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0131_flat.fits", fl_sky=yes,\
#          fl_flat=yes, skyimg="h2sky_mult.fits", calpath="./")
#gareduce ("@feobj.lis", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0061_flat.fits", fl_sky=yes,\
#          fl_flat=yes, skyimg="fesky_mult.fits", calpath="./")
#gareduce ("@ksobj.lis", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0101_flat.fits", fl_sky=yes,\
#          fl_flat=yes, skyimg="kssky_mult.fits", calpath="./")

# WRONG APPROACH:
# Scale the images, not the skys - need to combine the images later anyway
#   ####imarith h2sky.fits * 1.813 h2sky_30.fits # 78/43:   good for 30
#   gemexpr("a*1.813",output="h2sky_30.fits",a="h2sky.fits",var_expr="a[VAR]*9",fl_vardq=yes)
#   hedit("h2sky_30.fits[0]",fields="METACONF",value='78._16_3+Clear_H2(1-0)_G1121+SKY+FF+TRIM+NLC',verify=no)
#   ####imarith h2sky.fits * 1.607 h2sky_31.fits # 69.1/43: good for 31,34
#   gemexpr("a*1.607",output="h2sky_31.fits",a="h2sky.fits",var_expr="a[VAR]*9",fl_vardq=yes)
#   hedit("h2sky_31.fits[0]",fields="METACONF",value='69.1_16_3+Clear_H2(1-0)_G1121+SKY+FF+TRIM+NLC',verify=no)
#   ####imarith h2sky.fits * 1.026 h2sky_33.fits # 44.1/43: good for 33 (negligible correction, needed for hdr)
#   gemexpr("a*1.026",output="h2sky_33.fits",a="h2sky.fits",var_expr="a[VAR]*9",fl_vardq=yes)
#   hedit("h2sky_33.fits[0]",fields="METACONF",value='44.1_16_3+Clear_H2(1-0)_G1121+SKY+FF+TRIM+NLC',verify=no)
#   ####imarith h2sky.fits * 1.009 h2sky_35.fits # 44.1/43: good for 35 (negligible correction, needed for hdr)
#   gemexpr("a*1.009",output="h2sky_35.fits",a="h2sky.fits",var_expr="a[VAR]*9",fl_vardq=yes)
#   hedit("h2sky_35.fits[0]",fields="METACONF",value='43.4_16_3+Clear_H2(1-0)_G1121+SKY+FF+TRIM+NLC',verify=no)

# scale h2 images based on their exposure times
gemexpr("a/1.813",output="sS20130228S0130",a="S20130228S0130",var_expr="a[VAR]/3.287")
hedit("sS20130228S0130.fits[0]",fields="METACONF",value='43.0_16_1+Clear_H2(1-0)_G1121+OBJ+FF+TRIM+NLC',verify=no, add=yes)
gemexpr("a/1.607",output="sS20130228S0131",a="S20130228S0131",var_expr="a[VAR]/2.582")
hedit("sS20130228S0131.fits[0]",fields="METACONF",value='43.0_16_1+Clear_H2(1-0)_G1121+OBJ+FF+TRIM+NLC',verify=no, add=yes)
gemexpr("a/1.026",output="sS20130228S0133",a="S20130228S0133",var_expr="a[VAR]/1.053")
hedit("sS20130228S0133.fits[0]",fields="METACONF",value='43.0_16_1+Clear_H2(1-0)_G1121+OBJ+FF+TRIM+NLC',verify=no, add=yes)
gemexpr("a/1.607",output="sS20130228S0134",a="S20130228S0134",var_expr="a[VAR]/2.582")
hedit("sS20130228S0134.fits[0]",fields="METACONF",value='43.0_16_1+Clear_H2(1-0)_G1121+OBJ+FF+TRIM+NLC',verify=no, add=yes)
gemexpr("a/1.009",output="sS20130228S0135",a="S20130228S0135",var_expr="a[VAR]/1.018")
hedit("sS20130228S0135.fits[0]",fields="METACONF",value='43.0_16_1+Clear_H2(1-0)_G1121+OBJ+FF+TRIM+NLC',verify=no, add=yes)
hedit("s//@h2obj.lis//\[0]", fields="METACONF",value='43.0_16_1+Clear_H2(1-0)_G1121+OBJ+FF+TRIM+NLC',verify=no, add=yes)
hedit("s//@h2obj.lis//\[0]", fields="EXPTIME", value=43.0, verify=no)

# reset h2sky to "original"
hedit("h2sky.fits[0]",fields="METACONF",value='43.0_16_3+Clear_H2(1-0)_G1121+SKY+FF+TRIM+NLC',verify=no)

# April version stored in backup_may10
# "new" version should, in principle, do the appropriate sky subtraction...
gareduce ("s//@h2obj.lis", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0131_flat.fits", fl_sky=yes, fl_flat=yes, skyimg="h2sky.fits", calpath="./", logfile="h2cal.log")
#gareduce("S20130228S0130", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0131_flat.fits", fl_sky=yes, fl_flat=yes, skyimg="h2sky_30.fits", calpath="./")
#gareduce("S20130228S0131", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0131_flat.fits", fl_sky=yes, fl_flat=yes, skyimg="h2sky_31.fits", calpath="./")
#gareduce("S20130228S0133", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0131_flat.fits", fl_sky=yes, fl_flat=yes, skyimg="h2sky_33.fits", calpath="./")
#gareduce("S20130228S0134", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0131_flat.fits", fl_sky=yes, fl_flat=yes, skyimg="h2sky_31.fits", calpath="./")
#gareduce("S20130228S0135", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0131_flat.fits", fl_sky=yes, fl_flat=yes, skyimg="h2sky_35.fits", calpath="./")


#                                             '43._16_1+Clear_FeII_G1118+SKY+FF+TRIM+NLC'
hedit("fesky.fits[0]",fields="METACONF",value="44.5_16_3+Clear_FeII_G1118+SKY+FF+TRIM+NLC",verify=no)
gareduce ("@feobj.lis", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0061_flat.fits", fl_sky=yes, fl_flat=yes, skyimg="fesky.fits", calpath="./", logfile="fecal.log")
# METACONF= '15._2_1+Kcntshrt_G1111_Clear+SKY+FF+TRIM+NLC' / Data Reduction Metada
hedit("kssky.fits[0]",fields="METACONF",value="15._2_3+Kcntshrt_G1111_Clear+SKY+FF+TRIM+NLC",verify=no)
gareduce ("@ksobj.lis", fl_vardq=yes, fl_dqprop=yes, flatimg="gS20130201S0101_flat.fits", fl_sky=yes, fl_flat=yes, skyimg="kssky.fits", calpath="./", logfile="kscal.log")

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
imdelete ("mrg//@ksobj.lis", verify=no)
imdelete ("mrg//@feobj.lis", verify=no)

# Mosaic the four individual data extensions into one extension. This is done
# for each of the extensions within the image, e.g., "SCI", "VAR" and "DQ".

# cat ../GEMSSouth/s*_1_pixpixmap.txt ../GemsNorth/s*_1_pixpixmap.txt > pixpix1both.txt
# cat ../GEMSSouth/s*_2_pixpixmap.txt ../GemsNorth/s*_2_pixpixmap.txt > pixpix2both.txt
# cat ../GEMSSouth/s*_3_pixpixmap.txt ../GemsNorth/s*_3_pixpixmap.txt > pixpix3both.txt
# cat ../GEMSSouth/s*_4_pixpixmap.txt ../GemsNorth/s*_4_pixpixmap.txt > pixpix4both.txt
# geomap pixpix4both.txt pixpix4both.db xmin=-50 xmax=4300 ymin=-50 ymax=4300 transforms=frame4 maxiter=1 xxorder=3 xyorder=3 yyorder=3 yxorder=3 inter-
# geomap pixpix3both.txt pixpix3both.db xmin=-50 xmax=4300 ymin=-50 ymax=4300 transforms=frame3 maxiter=3 xxorder=3 xyorder=3 yyorder=3 yxorder=3 inter-
# geomap pixpix2both.txt pixpix2both.db xmin=-50 xmax=4300 ymin=-50 ymax=4300 transforms=frame2 maxiter=1 xxorder=3 xyorder=3 yyorder=3 yxorder=3 inter-
# geomap pixpix1both.txt pixpix1both.db xmin=-50 xmax=4300 ymin=-50 ymax=4300 transforms=frame1 maxiter=1 xxorder=3 xyorder=3 yyorder=3 yxorder=3 inter-

#for nn in [47,48,49,50,52,63,64,65,66,67,68,69,70,71,72]:
#    iraf.images.imutil.imdel("georgS20130228S00%02i.fits" % nn, verify=False)
#    my_geotran.my_geotran("rgS20130228S00%02i.fits" % nn,"georgS20130228S00%02i.fits" % nn)
#
#
#imcombine("georg//@h2obj.lis","h2_mosaic_georg.fits",combine="median",offset="wcs")
#imcombine("georg//@feobj.lis","fe_mosaic_georg.fits",combine="median",offset="wcs")
#imcombine("georg//@ksobj.lis","ks_mosaic_georg.fits",combine="median",offset="wcs")

##geotran("rgS20130228S0047.fits[1]", "mrgS20130228S0047.fits[1]", database="pixpix1both.db", transforms="frame1", boundary="constant",nxblock=2048,nyblock=2048)
#geotran("rgS20130228S0047.fits[2]", "mrgS20130228S0047.fits[2]", database="pixpix2both.db", transforms="frame2", boundary="constant",nxblock=2048,nyblock=2048)
#geotran("rgS20130228S0047.fits[3]", "mrgS20130228S0047.fits[3]", database="pixpix3both.db", transforms="frame3", boundary="constant",nxblock=2048,nyblock=2048)
#geotran("rgS20130228S0047.fits[4]", "mrgS20130228S0047.fits[4]", database="pixpix4both.db", transforms="frame4", boundary="constant",nxblock=2048,nyblock=2048)
#geotran("rgS20130228S0047.fits[1]", "test1.fits", database="pixpix1both.db", transforms="frame1", boundary="constant",nxblock=2048,nyblock=2048)
#geotran("rgS20130228S0047.fits[2]", "test2.fits", database="pixpix2both.db", transforms="frame2", boundary="constant",nxblock=2048,nyblock=2048)
#geotran("rgS20130228S0047.fits[3]", "test3.fits", database="pixpix3both.db", transforms="frame3", boundary="constant",nxblock=2048,nyblock=2048)
#geotran("rgS20130228S0047.fits[4]", "test4.fits", database="pixpix4both.db", transforms="frame4", boundary="constant",nxblock=2048,nyblock=2048)
#geotran("rgtest4.fits", "test4a.fits", database="pixpix4both.db", transforms="frame4a", boundary="constant",nxblock=2048,nyblock=2048,verbose=yes)
#for s in "abcdef":  iraf.images.hedit("test4%s.fits" % s,"CCDSEC",delete=yes,verify=no)
#for s in "abcdef":  iraf.images.hedit("test4%s.fits" % s,"DATASEC",delete=yes,verify=no)
#geotran("rgtest4.fits", "test4b.fits", database="pixpix4both.db", transforms="frame4b", boundary="constant",nxblock=2048,nyblock=2048,verbose=yes)
#geotran("rgtest4.fits", "test4c.fits", database="pixpix4both.db", transforms="frame4c", boundary="constant",nxblock=2048,nyblock=2048,verbose=yes)
#geotran("rgtest4.fits", "test4d.fits", database="pixpix4both.db", transforms="frame4d", boundary="constant",nxblock=2048,nyblock=2048,verbose=yes)
#geotran("rgtest4.fits", "test4e.fits", database="pixpix4both.db", transforms="frame4e", boundary="constant",nxblock=2048,nyblock=2048,verbose=yes)
#geotran("rgtest4.fits", "test4f.fits", database="pixpix4both.db", transforms="frame4f", boundary="constant",nxblock=2048,nyblock=2048,verbose=yes)
#geotran("rgtest4.fits", "test4g.fits", database="pixpix4both.db", transforms="frame4g", boundary="constant",nxblock=2048,nyblock=2048,verbose=yes)

# imcreate("test.fits",naxis=2,naxis1=4300,naxis2=4300)
# gregister("rgS20130228S0047.fits[1]", "mrgS20130228S0047.fits[1]", database="pixpix1both.db", transforms="frame1", boundary="constant",nxblock=2048,nyblock=2048)
# gregister("rgS20130228S0047.fits[2]", "mrgS20130228S0047.fits[2]", database="pixpix2both.db", transforms="frame2", boundary="constant",nxblock=2048,nyblock=2048)
# gregister("rgS20130228S0047.fits[3]", "mrgS20130228S0047.fits[3]", database="pixpix3both.db", transforms="frame3", boundary="constant",nxblock=2048,nyblock=2048)
# gregister("rgS20130228S0047.fits[4]", "mrgS20130228S0047.fits[4]", database="pixpix4both.db", transforms="frame4", boundary="constant",nxblock=2048,nyblock=2048)
# 
# imcombine("mrgS20130228S0047.fits[1],mrgS20130228S0047.fits[2],mrgS20130228S0047.fits[3],mrgS20130228S0047.fits[4]","mosS20130228S0047.fits",combine="sum",offset="none")
# 
# geotran("rg@h2obj.lis//\[1]", "mrg@h2obj.lis//\[1]", database="pixpix1both.db", transforms="frame1", boundary="constant",nxblock=2048,nyblock=2048)
# geotran("rg@h2obj.lis//\[2]", "mrg@h2obj.lis//\[2]", database="pixpix2both.db", transforms="frame2", boundary="constant",nxblock=2048,nyblock=2048)
# geotran("rg@h2obj.lis//\[3]", "mrg@h2obj.lis//\[3]", database="pixpix3both.db", transforms="frame3", boundary="constant",nxblock=2048,nyblock=2048)
# geotran("rg@h2obj.lis//\[4]", "mrg@h2obj.lis//\[4]", database="pixpix4both.db", transforms="frame4", boundary="constant",nxblock=2048,nyblock=2048)

gamosaic ("rg@h2obj.lis", fl_vardq=yes, fl_paste=no, fl_fluxcon=yes) #colgap=147, linegap=147, 
gamosaic ("rg@feobj.lis", fl_vardq=yes, fl_paste=no, fl_fluxcon=yes) #colgap=147, linegap=147, 
gamosaic ("rg@ksobj.lis", fl_vardq=yes, fl_paste=no, fl_fluxcon=yes) #colgap=147, linegap=147, 

#imcopy ("mrgS20130228S0065.fits[SCI]", "mask.fits[type=mask]")
#hedit ("mrgS20130228S00*fits[SCI]","BPM","mask.fits", add=yes, ver=no)

#for(n=1;n<=4;n+=1)
#{
#    wcscopy('rg//@h2obj.lis//['.str(n).']','@h2obj.lis//['.str(n).']')
#}
#for n in xrange(1,5):
#    str1="rg//@h2obj.lis//[%i]" % n
#    str2="@h2obj.lis//[%i]" % n
#    wcscopy(str1,str2)


# !rm rgS20130228S004[789]_[1234].fits
# !rm rgS20130228S005[02]_[1234].fits
# 
# imcopy("rgS20130228S0047.fits[1]","rgS20130228S0047_1.fits")
# imcopy("rgS20130228S0047.fits[2]","rgS20130228S0047_2.fits")
# imcopy("rgS20130228S0047.fits[3]","rgS20130228S0047_3.fits")
# imcopy("rgS20130228S0047.fits[4]","rgS20130228S0047_4.fits")
# imcombine("rgS20130228S0047_1.fits,rgS20130228S0047_2.fits,rgS20130228S0047_3.fits,rgS20130228S0047_4.fits","test.fits",offset="wcs",combine="sum")
# imcopy("rgS20130228S0048.fits[1]","rgS20130228S0048_1.fits")
# imcopy("rgS20130228S0048.fits[2]","rgS20130228S0048_2.fits")
# imcopy("rgS20130228S0048.fits[3]","rgS20130228S0048_3.fits")
# imcopy("rgS20130228S0048.fits[4]","rgS20130228S0048_4.fits")
# imcombine("rgS20130228S0048_1.fits,rgS20130228S0048_2.fits,rgS20130228S0048_3.fits,rgS20130228S0048_4.fits","test.fits",offset="wcs",combine="sum")
# imcopy("rgS20130228S0049.fits[1]","rgS20130228S0049_1.fits")
# imcopy("rgS20130228S0049.fits[2]","rgS20130228S0049_2.fits")
# imcopy("rgS20130228S0049.fits[3]","rgS20130228S0049_3.fits")
# imcopy("rgS20130228S0049.fits[4]","rgS20130228S0049_4.fits")
# imcombine("rgS20130228S0049_1.fits,rgS20130228S0049_2.fits,rgS20130228S0049_3.fits,rgS20130228S0049_4.fits","test.fits",offset="wcs",combine="sum")
# imcopy("rgs20130228s0050.fits[1]","rgs20130228s0050_1.fits")
# imcopy("rgs20130228s0050.fits[2]","rgs20130228s0050_2.fits")
# imcopy("rgs20130228s0050.fits[3]","rgs20130228s0050_3.fits")
# imcopy("rgs20130228s0050.fits[4]","rgs20130228s0050_4.fits")
# imcombine("rgS20130228S0050_1.fits,rgS20130228S0050_2.fits,rgS20130228S0050_3.fits,rgS20130228S0050_4.fits","test.fits",offset="wcs",combine="sum")
# imcopy("rgS20130228S0052.fits[1]","rgS20130228S0052_1.fits")
# imcopy("rgS20130228S0052.fits[2]","rgS20130228S0052_2.fits")
# imcopy("rgS20130228S0052.fits[3]","rgS20130228S0052_3.fits")
# imcopy("rgS20130228S0052.fits[4]","rgS20130228S0052_4.fits")
# imcombine("rgS20130228S0052_1.fits,rgS20130228S0052_2.fits,rgS20130228S0052_3.fits,rgS20130228S0052_4.fits","test.fits",offset="wcs",combine="sum")
# !PATH=/Users/adam/virtual-python/bin:$PATH /Users/adam/bin/montage rgS20130228S0047_[1234].fits --outfile=montage_47_skysub.fits --header=full.hdr 
# !PATH=/Users/adam/virtual-python/bin:$PATH /Users/adam/bin/montage rgS20130228S0048_[1234].fits --outfile=montage_48_skysub.fits --header=full.hdr 
# !PATH=/Users/adam/virtual-python/bin:$PATH /Users/adam/bin/montage rgS20130228S0049_[1234].fits --outfile=montage_49_skysub.fits --header=full.hdr 
# !PATH=/Users/adam/virtual-python/bin:$PATH /Users/adam/bin/montage rgS20130228S0050_[1234].fits --outfile=montage_50_skysub.fits --header=full.hdr 
# !PATH=/Users/adam/virtual-python/bin:$PATH /Users/adam/bin/montage rgS20130228S0052_[1234].fits --outfile=montage_52_skysub.fits --header=full.hdr 
# !PATH=/Users/adam/virtual-python/bin:$PATH /Users/adam/bin/montage rgS20130228S0047_[1234].fits rgS20130228S0048_[1234].fits rgS20130228S0049_[1234].fits --outfile=montage_H2.fits --header=full.hdr 
# !PATH=/Users/adam/virtual-python/bin:$PATH /Users/adam/bin/montage rgS20130228S0047_[1234].fits rgS20130228S0048_[1234].fits rgS20130228S0049_[1234].fits rgS20130228S005[02]_[1234].fits --outfile=montage_H2.fits --header=full.hdr 
#   
# 
# # This, by default, will create files with names the same as the input with "m"
# # prefixed to them.
# 
# #hedit("mrgS20130228S0048.fits[SCI]", "CRPIX1",  2102.29218917 , ver=no)
# #hedit("mrgS20130228S0048.fits[SCI]", "CRPIX2",  2974.35484079 , ver=no)
# #hedit("mrgS20130228S0049.fits[SCI]", "CRPIX1",  2107.99148106 , ver=no)
# #hedit("mrgS20130228S0049.fits[SCI]", "CRPIX2",  2966.49542506 , ver=no)
# #hedit("mrgS20130228S0050.fits[SCI]", "CRPIX1",  2121.19466364 , ver=no)
# #hedit("mrgS20130228S0050.fits[SCI]", "CRPIX2",  2960.47588239 , ver=no)
# #hedit("mrgS20130228S0052.fits[SCI]", "CRPIX1",  2112.91756148 , ver=no)
# #hedit("mrgS20130228S0052.fits[SCI]", "CRPIX2",  2968.31566533 , ver=no)
# 
# #for(n=47;n<=52;n+=1)
# #{
# #    if (n != 51) {
# #        ccfind("coords","found"//str(n), "mrgS20130228S00"//str(n)//".fits[SCI]", usewcs=yes)
# #        ccmap("found"//str(n), "ccmap"//str(n)//".db", images="mrgS20130228S00"//str(n)//".fits[SCI]", xcol=3, ycol=4, lngcol=1, latcol=2)
# #    }
# #}
# 
pyexecute('zero_to_nan.py')
#!montage.py `sed -e s/^/mrg/ -e 's/ *$/[SCI]/' feobj.lis` --outfile=fe_gamosaic_montage.fits
!montage.py `sed -e s/^/mrg/ -e 's/ *$/.fits/' feobj.lis` --outfile=fe_gamosaic_montage.fits 
!montage.py `sed -e s/^/mrg/ -e 's/ *$/.fits/' ksobj.lis` --outfile=ks_gamosaic_montage.fits --tmpdir=tmpb
!montage.py `sed -e s/^/mrg/ -e 's/ *$/.fits/' h2obj.lis` --outfile=h2_gamosaic_montage.fits --tmpdir=tmpc
#imcombine ("mrg//@h2obj.lis//\[SCI]", "H2_Feb28_comb.fits", combine="median", offset="wcs", masktype="badvalue")
#imcombine ("mrg//@ksobj.lis//\[SCI]", "ks_Feb28_comb.fits", combine="median", offset="wcs", masktype="badvalue")
#imcombine ("mrg//@feobj.lis//\[SCI]", "fe_Feb28_comb.fits", combine="median", offset="wcs", masktype="badvalue")
# 
# # sort of OK - only works for some, not all, of the quadrants
# imcoadd ("mrg//@h2obj.lis", outimage="H2_Jan31_coadd_mrg.fits", geofitgeom="general", alignmethod="wcs", fl_overwrite=yes, fl_mark=yes, fl_refmark=yes, fl_inter=yes, logfile=logfile)
# imcoadd ("mrg//@ksobj.lis", outimage="ks_Jan31_coadd_mrg.fits", geofitgeom="general", alignmethod="wcs", fl_overwrite=yes, fl_mark=yes, fl_refmark=yes, fl_inter=yes, logfile=logfile)
# imcoadd ("mrg//@feobj.lis", outimage="fe_Jan31_coadd_mrg.fits", geofitgeom="general", alignmethod="wcs", fl_overwrite=yes, fl_mark=yes, fl_refmark=yes, fl_inter=yes, logfile=logfile)
# 
# # FAIL imcoadd ("mrg//@h2obj.lis", outimage="H2_Jan31_coadd_xc.fits", geofitgeom="general", alignmethod="twodx", fl_overwrite=yes, fl_mark=yes, fl_refmark=yes, fl_inter=yes)
# 
# # first time solve and all that
# # imcoadd ("rg//@h2obj.lis", outimage="H2_Jan31_coadd_indivframes1.fits", geofitgeom="general", alignmethod="user", fl_overwrite=yes, fl_mark=yes, fl_refmark=yes, fl_inter=no, sci_ext=1, var_ext=5, dq_ext=9)
# # imcoadd ("rg//@h2obj.lis", outimage="H2_Jan31_coadd_indivframes2.fits", geofitgeom="general", alignmethod="user", fl_overwrite=yes, fl_mark=yes, fl_refmark=yes, fl_inter=no, sci_ext=2, var_ext=6, dq_ext=10)
# # imcoadd ("rg//@h2obj.lis", outimage="H2_Jan31_coadd_indivframes3.fits", geofitgeom="general", alignmethod="user", fl_overwrite=yes, fl_mark=yes, fl_refmark=yes, fl_inter=no, sci_ext=3, var_ext=7, dq_ext=11)
# # imcoadd ("rg//@h2obj.lis", outimage="H2_Jan31_coadd_indivframes4.fits", geofitgeom="general", alignmethod="user", fl_overwrite=yes, fl_mark=yes, fl_refmark=yes, fl_inter=no, sci_ext=4, var_ext=8, dq_ext=12)
# # imcoadd ("rg//@h2obj.lis", outimage="H2_Jan31_coadd_indivframes1.fits", geofitgeom="general", alignmethod="user", fl_overwrite=yes, fl_find=no, fl_map=no, fl_trn=no, fl_med=no, fl_add=yes, fl_avg=yes, fl_mark=yes, fl_refmark=yes, fl_inter=no, sci_ext=1, var_ext=5, dq_ext=9)
# # imcoadd ("rg//@h2obj.lis", outimage="H2_Jan31_coadd_indivframes2.fits", geofitgeom="general", alignmethod="user", fl_overwrite=yes, fl_find=no, fl_map=no, fl_trn=no, fl_med=no, fl_add=yes, fl_avg=yes, fl_mark=yes, fl_refmark=yes, fl_inter=no, sci_ext=2, var_ext=6, dq_ext=10)
# # imcoadd ("rg//@h2obj.lis", outimage="H2_Jan31_coadd_indivframes3.fits", geofitgeom="general", alignmethod="user", fl_overwrite=yes, fl_find=no, fl_map=no, fl_trn=no, fl_med=no, fl_add=yes, fl_avg=yes, fl_mark=yes, fl_refmark=yes, fl_inter=no, sci_ext=3, var_ext=7, dq_ext=11)
# # imcoadd ("rg//@h2obj.lis", outimage="H2_Jan31_coadd_indivframes4.fits", geofitgeom="general", alignmethod="user", fl_overwrite=yes, fl_find=no, fl_map=no, fl_trn=no, fl_med=no, fl_add=yes, fl_avg=yes, fl_mark=yes, fl_refmark=yes, fl_inter=no, sci_ext=4, var_ext=8, dq_ext=12)
# # imcoadd("H2_Jan31_coadd_indivframes*fits",outimage="H2_Jan31_coadd_allB.fits", alignmethod="wcs", sci_ext=1)
# 
# # # don't do this imcombine("H2_Jan31_coadd_indivframes*fits[1]","H2_Jan31_coadd_all.fits",offset="wcs",combine="median")
# 
# # for when I want to hack things myself imcopy ("mrg//@h2obj.lis//\[SCI]","mrg//@h2obj.lis//_SCI")
# 
# ###############################################################################
# # STEP 10: Tidy up                                                            #
# ###############################################################################
# 
# # delete ("obj.lis,sky.lis,flat.lis,dark.lis,all.lis", verify=no)
# 
# ###############################################################################
# # Finished!                                                                   #
# ###############################################################################


# make the geotran'd "rg" reduced files, aka georg
# files:
# 51, 52, 53, 54, 55, 56, 30, 31, 33, 34, 35, 45, 46, 47, 48, 49, 50   
# 
#for nn in [51, 52, 53, 54, 55, 56, 30, 31, 33, 34, 35, 45, 46, 47, 48, 49, 50]:
#    iraf.images.imutil.imdel("georgS20130228S01%02i.fits" % nn, verify=False)
#    my_geotran.my_geotran("rgS20130228S01%02i.fits" % nn,"george20130228S01%02i.fits" % nn)
