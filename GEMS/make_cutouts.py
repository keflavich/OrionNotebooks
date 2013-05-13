import aplpy
import pylab as pl
import os
import psi.process

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
F.show_rgb()
print "Memory Check - loaded img (ps): ",get_mem()/1024.**3

F.recenter(083.81417,-05.35392,5/3600.) # IR source [HAB84] 65
F.recenter(083.814550,-05.354239,5/3600.) # X-ray source COUP J053515.4-052115
F.recenter(083.81404,-05.35392 ,5/3600.) # V* V2270 Ori
F.save('V2270_ori.png')
F.recenter(83.813285, -5.3453289, 0.001961) # No associated sources (HH210 goes through here though)
F.save('BowBubble.png')
F.recenter(83.811216, -5.3723283, 0.0005) # [OW94] 147-220 (maybe)
F.save('Disk.png')
F.recenter(83.798999, -5.3658097, 0.0032) 
F.save('FastJet.png')
F.close()
print "Memory Check - closed img (ps): ",get_mem()/1024.**3

F2 = aplpy.FITSFigure('big_mosaic_h2.fits')
print "Memory Check - loaded h2 (ps): ",get_mem()/1024.**3
F2.show_grayscale()
F2.recenter(83.811216, -5.3723283, 0.0005) # [OW94] 147-220 (maybe)
F2.recenter(83.798999, -5.3658097, 0.0032)
F2.save('FastJetH2.png')
F2.close()
print "Memory Check - closed h2 (ps): ",get_mem()/1024.**3

F3 = aplpy.FITSFigure('HST_ACS_F658n_bigGEMS.fits')
print "Memory Check - loaded acs (ps): ",get_mem()/1024.**3
F3.show_grayscale(vmin=5,vmax=120,stretch='log')
F3.recenter(83.798999, -5.3658097, 0.0032)
F3.save('FastJetHA.png')
F3.close()
print "Memory Check - closed acs (ps): ",get_mem()/1024.**3

F4 = aplpy.FITSFigure('big_mosaic_feii.fits')
print "Memory Check - loaded feii (ps): ",get_mem()/1024.**3
F4.show_grayscale()
F4.recenter(83.811216, -5.3723283, 0.0005) # [OW94] 147-220 (maybe)
F4.recenter(83.798999, -5.3658097, 0.0032)
F4.save('FastJetFe.png')
F4.close()
print "Memory Check - closed feii (ps): ",get_mem()/1024.**3

pl.show()
