import montage
import pyfits
import glob
import numpy as np

filenamesh2 = glob.glob("georgs20130228S013[01345].fits")

# the q1-q4 "names" do not match anything; you have to look at the pixels in the actual images
# (the montage and georg disagree badly)
def rescale(filenames,cutoff=2100,q4cut=None,q3cut=None,q2cut=None, q1add=None,q4add=None):
    files = [pyfits.open(fn) for fn in filenames]

    data = [f[0].data for f in files]
    medians = [np.percentile(d[d==d],10) for d in data]
    med = np.median(medians)
    scales = med/np.array(medians)
    print "Scales: ",scales
    print "median: ",med," medians: ",medians
    for f,fn,s in zip(files,filenames,scales):
        data = f[0].data
        data[data<cutoff] = np.nan
        if q2cut is not None:
            q2 = data[:2290,:2290] 
            q2[q2<q2cut] = np.nan
        if q3cut is not None:
            q3 = data[2290:,2290:] 
            q3[q3<q3cut] = np.nan
        if q4cut is not None:
            q4 = data[:2290,2290:] 
            q4[q4<q4cut] = np.nan
        data *= s
        if q1add is not None:
            data[2290:,:2290] += q1add
        if q4add is not None:
            data[:2290,2290:] += q4add
        f.writeto(fn.replace(".fits","_scaled.fits"),clobber=True)

    outfilenames = [f.replace(".fits","_scaled.fits") for f in filenames]
    return outfilenames

outfilenames = rescale(filenamesh2,cutoff=2124, q2cut=2220, q3cut=2250, q4cut=2450, q1add=75,q4add=-210)
import os
cmdstr = "montage %s --outfile=h2_montage_georgs_southeast.fits --combine=median --header=gemsoutheast.hdr" % (" ".join(outfilenames))
os.system(cmdstr)
print cmdstr
#montage georgs20130228S013[01345]_scaled.fits --outfile=h2_montage_georgs_southeast.fits --combine=median --header=gemsoutheast.hdr 

outfilenames = rescale(glob.glob('georg20130228S015[13456].fits'),cutoff=1600, q4cut=1700, q4add=-50)
cmdstr = "montage %s --outfile=fe_montage_georgs_southeast.fits --combine=median --header=gemsoutheast.hdr" % (" ".join(outfilenames))
os.system(cmdstr)
print cmdstr
#montage georg20130228S015[13456].fits --outfile=fe_montage_georgs_southeast.fits --combine=median --header=gemsoutheast.hdr &

outfilenames = rescale(glob.glob('georg20130228S014[5789].fits')+['georg20130228S0150.fits'],cutoff=500, q4cut=300, q3cut=524, q1add=25, q4add=-75)
cmdstr = "montage %s --outfile=ks_montage_georgs_southeast.fits --combine=median --header=gemsoutheast.hdr" % (" ".join(outfilenames))
os.system(cmdstr)
print cmdstr
#montage georg20130228S014[5789].fits georg20130228S0150.fits --outfile=ks_montage_georgs_southeast.fits --combine=median --header=gemsoutheast.hdr&
