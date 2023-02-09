import aplpy
import pylab as pl
import os
import psi.process

import pyregion
import astropy.coordinates as coords
import astropy.units as units


def get_mem():
    pid = psi.process.ProcessTable()[os.getpid()]
    return pid.vsz

if False:
    aplpy.make_rgb_image(['big_mosaic_ks.fits','big_mosaic_h2_normed.fits','big_mosaic_feii_normed.fits'],
            'Big_Orion_RGB.png',
            stretch_r='log',vmin_r=220,vmax_r=600,
            stretch_g='log',vmin_g=-0.05,vmax_g=0.4,
            stretch_b='log',vmin_b=-0.05,vmax_b=0.4,
            embed_avm_tags=True,
            )

    F = aplpy.FITSFigure('Big_Orion_RGB.png',convention='calabretta')


print "Memory Check (ps): ",get_mem()/1024.**3
F = aplpy.FITSFigure('Trapezium_GEMS_mosaic_redblueorange_normed_large_contrast_bright.png')

reg = pyregion.open('proplyds.reg')
jetheads = pyregion.open('jetheads.reg')
def plotthings(F,prefix="cutouts/",rgb=True, **kwargs):
    if rgb:
        F.show_rgb()
    else:
        F.show_grayscale(**kwargs)
    print "Memory Check - loaded img (ps): ",get_mem()/1024.**3

    F.recenter(083.81417,-05.35392,5/3600.) # IR source [HAB84] 65
    F.recenter(083.814550,-05.354239,5/3600.) # X-ray source COUP J053515.4-052115
    F.recenter(083.81404,-05.35392 ,5/3600.) # V* V2270 Ori
    F.save(prefix+'V2270_ori.png')
    F.recenter(83.813285, -5.3453289, 0.001961) # No associated sources (HH210 goes through here though)
    F.save(prefix+'BowBubble.png')
    F.recenter(83.811216, -5.3723283, 0.0005) # [OW94] 147-220 (maybe)
    F.save(prefix+'Disk.png')
    F.recenter(83.798999, -5.3658097, 0.0032) 
    F.save(prefix+'FastJet.png')

    for region in reg:
        ra,dec = region.coord_list
        name = region.attr[1]['text'].replace(" ","_")
        try:
            F.recenter(ra,dec,0.002)
            F.save(prefix+name+"_orangergb.png")
            print "Saved %s" % name
        except:
            print "Skipped %s" % name

    for regnum,region in enumerate(jetheads):
        ra,dec,rad = region.coord_list
        F.recenter(ra,dec,rad)
        F.save(prefix+"jethead%02i.png" % regnum)

plotthings(F,prefix="cutouts/")
F.close()
print "Memory Check - closed img (ps): ",get_mem()/1024.**3

print "Memory Check (ps): ",get_mem()/1024.**3
F = aplpy.FITSFigure('TrapeziumHA_GEMS_mosaic_redblueorange_normed_large_contrast_bright.png')
plotthings(F,prefix="cutouts/HA_")
F.close()
print "Memory Check - closed img (ps): ",get_mem()/1024.**3

print "Memory Check (ps): ",get_mem()/1024.**3
FA = aplpy.FITSFigure('AltairTrapezium_GEMS_mosaic_redblueorange_normed_large_contrast_bright.png')

plotthings(FA,prefix="cutouts/Altair_")

FA.close()
print "Memory Check - closed img (ps): ",get_mem()/1024.**3

F2 = aplpy.FITSFigure('big_mosaic_h2.fits')
print "Memory Check - loaded h2 (ps): ",get_mem()/1024.**3
F2.show_grayscale(vmin=1000,vmax=1500,stretch='linear')

plotthings(F2,prefix="cutouts/H2_",rgb=False,vmin=1000,vmax=1500,stretch='linear')

F2.close()
print "Memory Check - closed h2 (ps): ",get_mem()/1024.**3

F2A = aplpy.FITSFigure('altair_big_h2.fits')
print "Memory Check - loaded h2 (ps): ",get_mem()/1024.**3
F2A.show_grayscale(vmin=80,vmax=250,stretch='linear')

plotthings(F2A,prefix="cutouts/Altair_H2_",rgb=False,vmin=80,vmax=250,stretch='linear')

F2A.close()
print "Memory Check - closed h2 (ps): ",get_mem()/1024.**3

F3 = aplpy.FITSFigure('HST_ACS_F658n_bigGEMS.fits')
print "Memory Check - loaded acs (ps): ",get_mem()/1024.**3
F3.show_grayscale(vmin=5,vmax=120,vmid=0,stretch='log')
F3.show_grayscale(vmin=21,vmax=75,vmid=15,stretch='log')

plotthings(F3,prefix="cutouts/HA_monochrome_",rgb=False,vmin=21,vmax=75,vmid=15,stretch='log')

F3.close()
print "Memory Check - closed acs (ps): ",get_mem()/1024.**3

F4 = aplpy.FITSFigure('big_mosaic_feii.fits')
print "Memory Check - loaded feii (ps): ",get_mem()/1024.**3
#F4.show_grayscale(vmin=0,vmax=1518,vmid=-1,stretch='log')
F4.show_grayscale(vmin=750,vmax=2300,vmid=748.5,stretch='log')

plotthings(F4,prefix="cutouts/Fe_",rgb=False,vmin=750,vmax=2300,vmid=748.5,stretch='log')

F4.close()
print "Memory Check - closed feii (ps): ",get_mem()/1024.**3

F5 = aplpy.FITSFigure('altair_big_fe.fits')
print "Memory Check - loaded feii (ps): ",get_mem()/1024.**3
#F5.show_grayscale(vmin=0,vmax=1518,vmid=-1,stretch='log')
F5.show_grayscale(vmin=87,vmax=300,vmid=84.84,stretch='log')

plotthings(F5,prefix="cutouts/Altair_Fe_",rgb=False,vmin=87,vmax=300,vmid=84.84,stretch='log')

F5.close()
print "Memory Check - closed feii (ps): ",get_mem()/1024.**3


pl.show()
