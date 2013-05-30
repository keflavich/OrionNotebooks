import sys
sys.path.append("/duanestorage/home/student/ginsbura/SCRATCH/irafscripts/scripts")
import my_geotran
import iraf
#import iraf.images
#import iraf.images.imutil

prefix = 'rgS20121229S'
numbers = [ '0112', '0113', '0114', '0115', '0116', '0117', '0118', '0119',
            '0120', '0121', '0132', '0133', '0134', '0135', '0136', '0137',
            '0138', '0139', '0140', '0141', ]


# in the southeast, had to scale the H2 images
# the lower-case 's' stands for 'scaled'
for nn in numbers:
    try:
        iraf.images.imutil.imdel("geo%s%s.fits" % (prefix,nn), verify=False)
        my_geotran.my_geotran("%s%s.fits" % (prefix,nn),"geo%s%s.fits" % (prefix,nn))
    except Exception as E:
        print "Failed for file %s%s.fits" % (prefix,nn)
        print E


# then do montage_script.sh
