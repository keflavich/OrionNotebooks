import sys
sys.path.append("/duanestorage/home/student/ginsbura/SCRATCH/irafscripts/scripts")
import my_geotran
import iraf
#import iraf.images
#import iraf.images.imutil

# in the southeast, had to scale the H2 images
# the lower-case 's' stands for 'scaled'
for nn in [30, 31, 33, 34, 35, ]:
    try:
        iraf.images.imutil.imdel("georgsS20130228S01%02i.fits" % nn, verify=False)
        my_geotran.my_geotran("rgsS20130228S01%02i.fits" % nn,"georgsS20130228S01%02i.fits" % nn)
    except Exception as E:
        print "Failed for file rgsS20130228S01%02i.fits" % nn
        print E

for nn in [51, 53, 54, 55, 56, 46, 47, 48, 49, 50]:
    try:
        iraf.images.imutil.imdel("georgS20130228S01%02i.fits" % nn, verify=False)
        my_geotran.my_geotran("rgS20130228S01%02i.fits" % nn,"georgS20130228S01%02i.fits" % nn)
    except Exception as E:
        print "Failed for file rgS20130228S01%02i.fits" % nn
        print E

# then do montage_script.sh
