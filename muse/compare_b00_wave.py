from astropy.io import fits
import numpy as np
import lines
import glob
import pyregion
import re

wavere = re.compile("([0-9]{4})_angstroms")

region = pyregion.open('B00.reg')

moments085 = glob.glob("moments/*_085_*angstroms.fits")
wavemom085 = {int(wavere.search(fn).groups()[0]):
              fn
              for fn in moments085
              if wavere.search(fn)
              }
k085 = np.array(wavemom085.keys())

matches085 = {name:
              (wl, fits.open(wavemom085[k085[np.argmin(np.abs(wl-k085))]])[0])
              for name,wl in lines.b00lines_measured.items()
              if np.min(np.abs(wl-k085)) < 5}

matched_wls085 = {name: (x[0], x[1].data[region.get_mask(x[1])].mean())
                  for name,x in matches085.items()}
vals085 = np.array(matched_wls085.values())

moments125 = glob.glob("moments/*_125_*angstroms.fits")
wavemom125 = {int(wavere.search(fn).groups()[0]):
              fn
              for fn in moments125
              if wavere.search(fn)
              }
k125 = np.array(wavemom125.keys())

matches125 = {name:
              (wl, fits.open(wavemom125[k125[np.argmin(np.abs(wl-k125))]])[0])
              for name,wl in lines.b00lines_measured.items()
              if np.min(np.abs(wl-k125)) < 5}

matched_wls125 = {name: (x[0], x[1].data[region.get_mask(x[1])].mean())
                  for name,x in matches125.items()}
vals125 = np.array(matched_wls125.values())

import pylab as pl
pl.close(0)
pl.figure(0)
ax1 = pl.gca()
ax2 = ax1.twinx()
def v(x):
    return (x/6562.81 * 299792.458)
def update_ax2(ax1):
   y1, y2 = ax1.get_ylim()
   ax2.set_ylim(v(y1), v(y2))
   ax2.figure.canvas.draw()

# automatically update ylim of ax2 when ylim of ax1 changes.
ax1.callbacks.connect("ylim_changed", update_ax2)

diff085 = vals085[:,1]-vals085[:,0]-(11.9/299792.458*vals085[:,0])
diff125 = vals125[:,1]-vals125[:,0]-(11.9/299792.458*vals125[:,0])
ax1.plot(vals085[:,0], diff085, 'ks', alpha=0.5, label='0.85$\AA$')
ax1.plot(vals125[:,0], diff125, 'ro', alpha=0.5, label='1.25$\AA$')
ax1.set_xlabel("Wavelength ($\AA$)")
ax1.set_ylabel("MUSE - B00 ($\AA$)")
ax2.set_ylabel("MUSE - B00 (km s$^{-1}$)")
ax1.legend(loc='best')
pl.savefig('B00_vs_MUSE_moment_comparison')

pl.close(1)
pl.figure(1)
pl.hist(diff085, color='k', alpha=0.5, label='0.85$\AA$')
pl.hist(diff125, color='r', alpha=0.5, label='1.25$\AA$')
print "085",diff085.mean(), diff085.std(),(diff085/vals085[:,0]*299792.458).mean(), (diff085/vals085[:,0]*299792.458).std()
print "125",diff125.mean(), diff125.std(),(diff125/vals125[:,0]*299792.458).mean(), (diff125/vals125[:,0]*299792.458).std()

pl.draw(); pl.show()
