
# coding: utf-8

# Querying ALMA archive for OrionKL pointings and plotting them on a 2MASS image

# In[91]:

from astroquery.alma import Alma
from astroquery.skyview import SkyView
import string
from astropy import units as u
from astropy import coordinates
import pylab as pl
import aplpy


# Retrieve OrionKL 2MASS K-band image:

# In[92]:

orionkl_coords = coordinates.SkyCoord.from_name('Orion KL')


# In[93]:

orionkl_images = SkyView.get_images(position='Orion KL', survey=['2MASS-K'], pixels=500)
orionkl_images


# Retrieve ALMA archive information *including* private data and non-science fields:
# 

# In[94]:

orionkl = Alma.query_region(coordinate=orionkl_coords, radius=4*u.arcmin, public=False, science=False)


# In[95]:

orionkl


# Parse components of the ALMA data.  Specifically, find the frequency support - the frequency range covered - and convert that into a central frequency for beam radius estimation.

# In[96]:

def parse_frequency_support(frequency_support_str):
    supports = frequency_support_str.split("U")
    freq_ranges = [(float(sup.strip('[] ').split("..")[0]),
                    float(sup.strip('[] ').split("..")[1].split(',')[0].strip(string.letters)))
                   *u.Unit(sup.strip('[] ').split("..")[1].split(',')[0].strip(string.punctuation+string.digits))
                   for sup in supports]
    return u.Quantity(freq_ranges)

def approximate_primary_beam_sizes(frequency_support_str):
    freq_ranges = parse_frequency_support(frequency_support_str)
    beam_sizes = [(1.22*fr.mean().to(u.m, u.spectral())/(12*u.m)).to(u.arcsec,
                                                                     u.dimensionless_angles())
                  for fr in freq_ranges]
    return u.Quantity(beam_sizes)


# In[97]:

primary_beam_radii = [approximate_primary_beam_sizes(row['Frequency support']) for row in orionkl]


# Compute primary beam parameters for the public and private components of the data for plotting below.

# In[109]:

bands = np.unique(orionkl['Band'])
print "The bands used include: "
print bands
band_colors_priv = dict(zip(bands, ('red','darkred','orange','brown','maroon')))
band_colors_pub = dict(zip(bands, ('blue','cyan','green','turquoise','teal')))


# In[99]:

private_circle_parameters = {band: [(row['RA'],row['Dec'],np.mean(rad).to(u.deg).value)
                             for row,rad in zip(orionkl, primary_beam_radii)
                             if row['Release date']!='' and row['Band']==band]
                             for band in bands}
public_circle_parameters = {band: [(row['RA'],row['Dec'],np.mean(rad).to(u.deg).value)
                             for row,rad in zip(orionkl, primary_beam_radii)
                             if row['Release date']=='' and row['Band']==band]
                             for band in bands}

unique_private_circle_parameters = {band: np.array(list(set(private_circle_parameters[band])))
                                    for band in bands}
unique_public_circle_parameters = {band: np.array(list(set(public_circle_parameters[band])))
                                   for band in bands}

for band in bands:
    print "BAND {0}".format(band)
    privrows = sum((orionkl['Band']==band) & (orionkl['Release date'] != ''))
    pubrows  = sum((orionkl['Band']==band) & (orionkl['Release date'] == ''))
    print "PUBLIC:  Number of rows: {0}.  Unique pointings: {1}".format(pubrows, len(unique_public_circle_parameters[band]))
    print "PRIVATE: Number of rows: {0}.  Unique pointings: {1}".format(privrows, len(unique_private_circle_parameters[band]))


# Show all of the private observation pointings that have been acquired

# In[110]:

fig = aplpy.FITSFigure(orionkl_images[0])
fig.show_grayscale(stretch='arcsinh')
for band in bands:
    if unique_private_circle_parameters[band].any():
        fig.show_circles(unique_private_circle_parameters[band][:,0],
                         unique_private_circle_parameters[band][:,1],
                         unique_private_circle_parameters[band][:,2],
                         color=band_colors_priv[band], alpha=0.2)


# In principle, all of the pointings shown below should be downloadable from the archive:

# In[111]:

fig = aplpy.FITSFigure(orionkl_images[0])
fig.show_grayscale(stretch='arcsinh')
for band in bands:
    if unique_public_circle_parameters[band].any():
        fig.show_circles(unique_public_circle_parameters[band][:,0],
                         unique_public_circle_parameters[band][:,1],
                         unique_public_circle_parameters[band][:,2],
                         color=band_colors_pub[band], alpha=0.2)


# Use pyregion to write the observed regions to disk.  Pyregion has a very awkward API; there is (in principle) work in progress to improve that situation but for now one must do all this extra work.

# In[112]:

import pyregion
from pyregion.parser_helper import Shape
prv_regions = {band: pyregion.ShapeList([Shape('circle',[x,y,r]) for x,y,r in private_circle_parameters[band]])
               for band in bands}
pub_regions = {band: pyregion.ShapeList([Shape('circle',[x,y,r]) for x,y,r in public_circle_parameters[band]])
               for band in bands}
for band in bands:
    circle_pars = np.vstack([x for x in (private_circle_parameters[band],
                                    public_circle_parameters[band]) if any(x)])
    for r,(x,y,c) in zip(prv_regions[band]+pub_regions[band],
                         circle_pars):
        r.coord_format = 'fk5'
        r.coord_list = [x,y,c]
        r.attr = ([], {'color': 'green',  'dash': '0 ',  'dashlist': '8 3 ',  'delete': '1 ',  'edit': '1 ',
                       'fixed': '0 ',  'font': '"helvetica 10 normal roman"',  'highlite': '1 ',
                       'include': '1 ',  'move': '1 ',  'select': '1 ',  'source': '1',  'text': '',
                       'width': '1 '})
        
    if prv_regions[band]:
        prv_regions[band].write('OrionKL_observed_regions_band{0}_private_March2015.reg'.format(band))
    if pub_regions[band]:
        pub_regions[band].write('OrionKL_observed_regions_band{0}_public_March2015.reg'.format(band))


# In[113]:

from astropy.io import fits


# In[114]:

prv_mask = {band: fits.PrimaryHDU(prv_regions[band].get_mask(orionkl_images[0][0]).astype('int'),
                           header=orionkl_images[0][0].header) for band in bands
            if prv_regions[band]}
pub_mask = {band: fits.PrimaryHDU(pub_regions[band].get_mask(orionkl_images[0][0]).astype('int'),
                           header=orionkl_images[0][0].header) for band in bands
            if pub_regions[band]}


# In[115]:

for band in pub_mask:
    pub_mask[band].writeto('public_orionkl_band{0}_almaobs_mask.fits'.format(band), clobber=True)
for band in prv_mask:
    prv_mask[band].writeto('private_orionkl_band{0}_almaobs_mask.fits'.format(band), clobber=True)    


# In[117]:

fig = aplpy.FITSFigure(orionkl_images[0])
fig.show_grayscale(stretch='arcsinh')
for band in bands:
    if band in prv_mask:
        fig.show_contour(prv_mask[band], levels=[0.5,1], colors=[band_colors_priv[band]]*2)
    if band in pub_mask:
        fig.show_contour(pub_mask[band], levels=[0.5,1], colors=[band_colors_pub[band]]*2)


# ## More advanced ##
# 
# Now we create a 'hit mask' showing the relative depth of each observed field in each band

# In[118]:

hit_mask_public = {band: np.zeros_like(orionkl_images[0][0].data) for band in pub_mask}
hit_mask_private = {band: np.zeros_like(orionkl_images[0][0].data) for band in prv_mask}
from astropy import wcs
mywcs = wcs.WCS(orionkl_images[0][0].header)


# In[119]:

for band in bands:
    for row,rad in zip(orionkl, primary_beam_radii):
        shape = Shape('circle', (row['RA'], row['Dec'],np.mean(rad).to(u.deg).value))
        shape.coord_format = 'fk5'
        shape.coord_list = (row['RA'], row['Dec'],np.mean(rad).to(u.deg).value)
        shape.attr = ([], {'color': 'green',  'dash': '0 ',  'dashlist': '8 3 ',  'delete': '1 ',  'edit': '1 ',
                       'fixed': '0 ',  'font': '"helvetica 10 normal roman"',  'highlite': '1 ',
                       'include': '1 ',  'move': '1 ',  'select': '1 ',  'source': '1',  'text': '',
                       'width': '1 '})
        if row['Release date']=='' and row['Band']==band and band in prv_mask:
            (xlo,xhi,ylo,yhi),mask = pyregion_subset(shape, hit_mask_private[band], mywcs) 
            hit_mask_private[band][ylo:yhi,xlo:xhi] += row['Integration']*mask
        if row['Release date']!='' and row['Band']==band and band in pub_mask:
            (xlo,xhi,ylo,yhi),mask = pyregion_subset(shape, hit_mask_public[band], mywcs) 
            hit_mask_public[band][ylo:yhi,xlo:xhi] += row['Integration']*mask


# In[120]:

fig = aplpy.FITSFigure(orionkl_images[0])
fig.show_grayscale(stretch='arcsinh')
for band in bands:
    if band in pub_mask:
        fig.show_contour(fits.PrimaryHDU(data=hit_mask_public[band], header=orionkl_images[0][0].header),
                         levels=np.logspace(0,5,base=2, num=6), colors=[band_colors_pub[band]]*6)
    if band in prv_mask:
        fig.show_contour(fits.PrimaryHDU(data=hit_mask_private[band], header=orionkl_images[0][0].header),
                         levels=np.logspace(0,5,base=2, num=6), colors=[band_colors_priv[band]]*6)


# In[ ]:

from astropy import wcs
import pyregion
from astropy import log

def pyregion_subset(region, data, mywcs):
    """
    Return a subset of an image (`data`) given a region.
    """
    shapelist = pyregion.ShapeList([region])
    if shapelist[0].coord_format not in ('physical','image'):
        # Requires astropy >0.4...
        # pixel_regions = shapelist.as_imagecoord(self.wcs.celestial.to_header())
        # convert the regions to image (pixel) coordinates
        celhdr = mywcs.sub([wcs.WCSSUB_CELESTIAL]).to_header()
        pixel_regions = shapelist.as_imagecoord(celhdr)
    else:
        # For this to work, we'd need to change the reference pixel after cropping.
        # Alternatively, we can just make the full-sized mask... todo....
        raise NotImplementedError("Can't use non-celestial coordinates with regions.")
        pixel_regions = shapelist

    # This is a hack to use mpl to determine the outer bounds of the regions
    # (but it's a legit hack - pyregion needs a major internal refactor
    # before we can approach this any other way, I think -AG)
    mpl_objs = pixel_regions.get_mpl_patches_texts()[0]

    # Find the minimal enclosing box containing all of the regions
    # (this will speed up the mask creation below)
    extent = mpl_objs[0].get_extents()
    xlo, ylo = extent.min
    xhi, yhi = extent.max
    all_extents = [obj.get_extents() for obj in mpl_objs]
    for ext in all_extents:
        xlo = xlo if xlo < ext.min[0] else ext.min[0]
        ylo = ylo if ylo < ext.min[1] else ext.min[1]
        xhi = xhi if xhi > ext.max[0] else ext.max[0]
        yhi = yhi if yhi > ext.max[1] else ext.max[1]

    log.debug("Region boundaries: ")
    log.debug("xlo={xlo}, ylo={ylo}, xhi={xhi}, yhi={yhi}".format(xlo=xlo,
                                                                  ylo=ylo,
                                                                  xhi=xhi,
                                                                  yhi=yhi))

    
    subwcs = mywcs[ylo:yhi, xlo:xhi]
    subhdr = subwcs.sub([wcs.WCSSUB_CELESTIAL]).to_header()
    subdata = data[ylo:yhi, xlo:xhi]
    
    mask = shapelist.get_mask(header=subhdr,
                              shape=subdata.shape)
    log.debug("Shapes: data={0}, subdata={2}, mask={1}".format(data.shape, mask.shape, subdata.shape))
    return (xlo,xhi,ylo,yhi),mask

