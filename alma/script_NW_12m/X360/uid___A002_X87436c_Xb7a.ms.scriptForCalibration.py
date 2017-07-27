# ALMA Data Reduction Script

# Calibration

thesteps = []
step_title = {0: 'Import of the ASDM',
              1: 'Fix of SYSCAL table times',
              2: 'Running fixplanets on fields with 0,0 coordinates',
              3: 'listobs',
              4: 'A priori flagging',
              5: 'Generation and time averaging of the WVR cal table',
              6: 'Generation of the Tsys cal table',
              7: 'Generation of the antenna position cal table',
              8: 'Application of the WVR, Tsys and antpos cal tables',
              9: 'Split out science SPWs and time average',
              10: 'Listobs, clear pointing table, and save original flags',
              11: 'Initial flagging',
              12: 'Putting a model for the flux calibrator(s)',
              13: 'Save flags before bandpass cal',
              14: 'Bandpass calibration',
              15: 'Save flags before gain cal',
              16: 'Gain calibration',
              17: 'Save flags before applycal',
              18: 'Application of the bandpass and gain cal tables',
              19: 'Split out corrected column',
              20: 'Save flags after applycal'}

if 'applyonly' not in globals(): applyonly = False
try:
  print 'List of steps to be executed ...', mysteps
  thesteps = mysteps
except:
  print 'global variable mysteps not set.'
if (thesteps==[]):
  thesteps = range(0,len(step_title))
  print 'Executing all steps: ', thesteps

# The Python variable 'mysteps' will control which steps
# are executed when you start the script using
#   execfile('scriptForCalibration.py')
# e.g. setting
#   mysteps = [2,3,4]# before starting the script will make the script execute
# only steps 2, 3, and 4
# Setting mysteps = [] will make it execute all steps.

import re

import os

if applyonly != True: es = aU.stuffForScienceDataReduction() 


# if re.search('^4.3.0', casadef.casa_version) == None:
#  sys.exit('ERROR: PLEASE USE THE SAME VERSION OF CASA THAT YOU USED FOR GENERATING THE SCRIPT: 4.3.0')


# CALIBRATE_AMPLI: Uranus
# CALIBRATE_ATMOSPHERE: J0607-0834,OMC1_NW,Uranus
# CALIBRATE_BANDPASS: J0607-0834
# CALIBRATE_FLUX: Uranus
# CALIBRATE_FOCUS: 
# CALIBRATE_PHASE: J0541-0541
# CALIBRATE_POINTING: J0108+0135,J0541-0541,J0607-0834
# OBSERVE_TARGET: OMC1_NW

# Using reference antenna = CM02

# Import of the ASDM
mystep = 0
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  if os.path.exists('uid___A002_X87436c_Xb7a.ms') == False:
    importasdm('uid___A002_X87436c_Xb7a', asis='Antenna Station Receiver Source CalAtmosphere CalWVR', bdfflags=True)
  if applyonly != True: es.fixForCSV2555('uid___A002_X87436c_Xb7a.ms')

# Fix of SYSCAL table times
mystep = 1
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  from recipes.almahelpers import fixsyscaltimes
  fixsyscaltimes(vis = 'uid___A002_X87436c_Xb7a.ms')

print "# A priori calibration"

# Running fixplanets on fields with 0,0 coordinates
mystep = 2
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  fixplanets(vis = 'uid___A002_X87436c_Xb7a.ms',
    field = '2', # Uranus
    fixuvw = T)
  

# listobs
mystep = 3
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.listobs')
  listobs(vis = 'uid___A002_X87436c_Xb7a.ms',
    listfile = 'uid___A002_X87436c_Xb7a.ms.listobs')
  
  

# A priori flagging
mystep = 4
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  flagdata(vis = 'uid___A002_X87436c_Xb7a.ms',
    mode = 'manual',
    spw = '0~23',
    autocorr = T,
    flagbackup = F)
  
  flagdata(vis = 'uid___A002_X87436c_Xb7a.ms',
    mode = 'manual',
    intent = '*POINTING*,*SIDEBAND_RATIO*,*ATMOSPHERE*',
    flagbackup = F)
  
  flagcmd(vis = 'uid___A002_X87436c_Xb7a.ms',
    inpmode = 'table',
    useapplied = True,
    action = 'plot',
    plotfile = 'uid___A002_X87436c_Xb7a.ms.flagcmd.png')
  
  flagcmd(vis = 'uid___A002_X87436c_Xb7a.ms',
    inpmode = 'table',
    useapplied = True,
    action = 'apply')
  

# Generation and time averaging of the WVR cal table
mystep = 5
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  

# Generation of the Tsys cal table
mystep = 6
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.tsys') 
  gencal(vis = 'uid___A002_X87436c_Xb7a.ms',
    caltable = 'uid___A002_X87436c_Xb7a.ms.tsys',
    caltype = 'tsys')
  
  # Flagging edge channels
  
  flagdata(vis = 'uid___A002_X87436c_Xb7a.ms.tsys',
    mode = 'manual',
    spw = '8:0~3;124~127,10:0~3;124~127,12:0~3;124~127,14:0~3;124~127',
    flagbackup = F)
  
  if applyonly != True: aU.plotbandpass(caltable='uid___A002_X87436c_Xb7a.ms.tsys', overlay='time', 
    xaxis='freq', yaxis='amp', subplot=22, buildpdf=False, interactive=False,
    showatm=True,pwv='auto',chanrange='5~123',showfdm=True, showBasebandNumber=True, 
    field='', figfile='uid___A002_X87436c_Xb7a.ms.tsys.plots.overlayTime/uid___A002_X87436c_Xb7a.ms.tsys') 
  
  
  if applyonly != True: es.checkCalTable('uid___A002_X87436c_Xb7a.ms.tsys', msName='uid___A002_X87436c_Xb7a.ms', interactive=False) 
  

# Generation of the antenna position cal table
mystep = 7
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  # Position for antenna CM01 is derived from baseline run made on 2014-06-02 04:15:36.
  
  # Position for antenna CM05 is derived from baseline run made on 2014-06-02 04:15:36.
  
  # Position for antenna CM12 is derived from baseline run made on 2014-06-02 04:15:36.
  
  # Position for antenna CM11 is derived from baseline run made on 2014-06-02 04:15:36.
  
  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.antpos') 
  gencal(vis = 'uid___A002_X87436c_Xb7a.ms',
    caltable = 'uid___A002_X87436c_Xb7a.ms.antpos',
    caltype = 'antpos',
    antenna = 'CM01,CM11,CM05,CM12',
    parameter = [0,0,0,0,0,0,0,0,0,0,0,0])
  #  parameter = [0.000254319605787,-0.000394619449271,-6.89422103618e-05,0.000187085476452,-0.00047325931429,-0.00032447903775,0.000164579600096,-0.000295721925795,-0.000169022008777,0.000360958191864,-0.000491564156966,-1.53252508184e-05])
  

# Application of the WVR, Tsys and antpos cal tables
mystep = 8
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  
  
  from recipes.almahelpers import tsysspwmap
  tsysmap = tsysspwmap(vis = 'uid___A002_X87436c_Xb7a.ms', tsystable = 'uid___A002_X87436c_Xb7a.ms.tsys', tsysChanTol = 1)
  
  
  
  applycal(vis = 'uid___A002_X87436c_Xb7a.ms',
    field = '0',
    spw = '16,18,20,22',
    gaintable = ['uid___A002_X87436c_Xb7a.ms.tsys', 'uid___A002_X87436c_Xb7a.ms.antpos'],
    gainfield = ['0', ''],
    interp = 'linear,linear',
    spwmap = [tsysmap,[]],
    calwt = T,
    flagbackup = F)
  
  
  
  # Note: J0108+0135 didn't have any Tsys measurement, and I couldn't find any close measurement. But this is not a science target, so this is probably Ok.
  
  applycal(vis = 'uid___A002_X87436c_Xb7a.ms',
    field = '2',
    spw = '16,18,20,22',
    gaintable = ['uid___A002_X87436c_Xb7a.ms.tsys', 'uid___A002_X87436c_Xb7a.ms.antpos'],
    gainfield = ['2', ''],
    interp = 'linear,linear',
    spwmap = [tsysmap,[]],
    calwt = T,
    flagbackup = F)
  
  
  
  # Note: J0541-0541 didn't have any Tsys measurement, so I used the one made on OMC1_NW. This is probably Ok.
  
  applycal(vis = 'uid___A002_X87436c_Xb7a.ms',
    field = '3',
    spw = '16,18,20,22',
    gaintable = ['uid___A002_X87436c_Xb7a.ms.tsys', 'uid___A002_X87436c_Xb7a.ms.antpos'],
    gainfield = ['4', ''],
    interp = 'linear,linear',
    spwmap = [tsysmap,[]],
    calwt = T,
    flagbackup = F)
  
  
  
  applycal(vis = 'uid___A002_X87436c_Xb7a.ms',
    field = '4~47',
    spw = '16,18,20,22',
    gaintable = ['uid___A002_X87436c_Xb7a.ms.tsys', 'uid___A002_X87436c_Xb7a.ms.antpos'],
    gainfield = ['4', ''],
    interp = 'linear,linear',
    spwmap = [tsysmap,[]],
    calwt = T,
    flagbackup = F)
  
  if applyonly != True: es.getCalWeightStats('uid___A002_X87436c_Xb7a.ms') 
  

# Split out science SPWs and time average
mystep = 9
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.split') 
  split(vis = 'uid___A002_X87436c_Xb7a.ms',
    outputvis = 'uid___A002_X87436c_Xb7a.ms.split',
    datacolumn = 'corrected',
    spw = '16,18,20,22',
    keepflags = T)
  
  

print "# Calibration"

# Listobs, clear pointing table, and save original flags
mystep = 10
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.split.listobs')
  listobs(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    listfile = 'uid___A002_X87436c_Xb7a.ms.split.listobs')
  
  tb.open('uid___A002_X87436c_Xb7a.ms.split/POINTING', nomodify = False)
  a = tb.rownumbers()
  tb.removerows(a)
  tb.close()
  
  if not os.path.exists('uid___A002_X87436c_Xb7a.ms.split.flagversions/Original.flags'):
    flagmanager(vis = 'uid___A002_X87436c_Xb7a.ms.split',
      mode = 'save',
      versionname = 'Original')
  
  

# Initial flagging
mystep = 11
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  # Flagging shadowed data
  
  flagdata(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    mode = 'shadow',
    flagbackup = F)
  
  

# Putting a model for the flux calibrator(s)
mystep = 12
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  setjy(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    field = '2', # Uranus
    spw = '0,1,2,3',
    standard = 'Butler-JPL-Horizons 2012')
  
  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.split.setjy.field*.png') 
  for i in ['2']:
    plotms(vis = 'uid___A002_X87436c_Xb7a.ms.split',
      xaxis = 'uvdist',
      yaxis = 'amp',
      ydatacolumn = 'model',
      field = str(i),
      spw = '0,1,2,3',
      avgchannel = '9999',
      coloraxis = 'spw',
      plotfile = 'uid___A002_X87436c_Xb7a.ms.split.setjy.field'+i+'.png')

# because of some issues with noisy or missing flux calibration, we used the mean of all 4 exectuions of the SB
# to fix scale with J0607-0834 (the BP cal)

  setjy(vis = 'uid___A002_X87436c_Xb7a.ms.split',field='0',spw='0,1,2,3',standard='manual',fluxdensity=[1.47,0,0,0],spix=-0.8,reffreq='225.115GHz')
  

# Save flags before bandpass cal
mystep = 13
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  
  flagmanager(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    mode = 'save',
    versionname = 'BeforeBandpassCalibration')
  
  

# Bandpass calibration
mystep = 14
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.split.ap_pre_bandpass') 
  
  gaincal(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    caltable = 'uid___A002_X87436c_Xb7a.ms.split.ap_pre_bandpass',
    field = '0', # J0607-0834
    spw = '0:816~1224,1:816~1224,2:816~1224,3:816~1224',
    scan = '1,2,4',
    solint = 'int',
    refant = 'CM02',
    calmode = 'p')
  
  if applyonly != True: es.checkCalTable('uid___A002_X87436c_Xb7a.ms.split.ap_pre_bandpass', msName='uid___A002_X87436c_Xb7a.ms.split', interactive=False) 
  
  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.split.bandpass') 
  bandpass(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    caltable = 'uid___A002_X87436c_Xb7a.ms.split.bandpass',
    field = '0', # J0607-0834
    scan = '1,2,4',
    solint = 'inf',
    combine = 'scan',
    refant = 'CM02',
    solnorm = True,
    bandtype = 'B',
    gaintable = 'uid___A002_X87436c_Xb7a.ms.split.ap_pre_bandpass')
  
  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.split.bandpass_smooth20ch') 
  
  bandpass(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    caltable = 'uid___A002_X87436c_Xb7a.ms.split.bandpass_smooth20ch',
    field = '0', # J0607-0834
    scan = '1,2,4',
    solint = 'inf,20ch',
    combine = 'scan',
    refant = 'CM02',
    solnorm = True,
    bandtype = 'B',
    gaintable = 'uid___A002_X87436c_Xb7a.ms.split.ap_pre_bandpass')
  
  if applyonly != True: es.checkCalTable('uid___A002_X87436c_Xb7a.ms.split.bandpass_smooth20ch', msName='uid___A002_X87436c_Xb7a.ms.split', interactive=False) 
  
  if applyonly != True: es.checkCalTable('uid___A002_X87436c_Xb7a.ms.split.bandpass', msName='uid___A002_X87436c_Xb7a.ms.split', interactive=False) 
  

# Save flags before gain cal
mystep = 15
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  
  flagmanager(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    mode = 'save',
    versionname = 'BeforeGainCalibration')
  
  

# Gain calibration
mystep = 16
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.split.phase_int') 
  
  gaincal(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    caltable = 'uid___A002_X87436c_Xb7a.ms.split.phase_int',
    field = '0~0,2~3', # J0607-0834,Uranus,J0541-0541
    solint = 'int',
    refant = 'CM02',
    gaintype = 'G',
    calmode = 'p',
    gaintable = 'uid___A002_X87436c_Xb7a.ms.split.bandpass_smooth20ch')
  
  if applyonly != True: es.checkCalTable('uid___A002_X87436c_Xb7a.ms.split.phase_int', msName='uid___A002_X87436c_Xb7a.ms.split', interactive=False) 
  
  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.split.ampli_inf') 
  gaincal(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    caltable = 'uid___A002_X87436c_Xb7a.ms.split.ampli_inf',
    field = '0~0,2~3', # J0607-0834,Uranus,J0541-0541
    solint = 'inf',
    refant = 'CM02',
    gaintype = 'T',
    calmode = 'a',
    gaintable = ['uid___A002_X87436c_Xb7a.ms.split.bandpass_smooth20ch', 'uid___A002_X87436c_Xb7a.ms.split.phase_int'])
  
  if applyonly != True: es.checkCalTable('uid___A002_X87436c_Xb7a.ms.split.ampli_inf', msName='uid___A002_X87436c_Xb7a.ms.split', interactive=False) 
  
  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.split.flux_inf') 
  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.split.fluxscale') 
  mylogfile = casalog.logfile()
  casalog.setlogfile('uid___A002_X87436c_Xb7a.ms.split.fluxscale')
  
  fluxscaleDict = fluxscale(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    caltable = 'uid___A002_X87436c_Xb7a.ms.split.ampli_inf',
    fluxtable = 'uid___A002_X87436c_Xb7a.ms.split.flux_inf',
    reference = '0') 
  
  casalog.setlogfile(mylogfile)
  
  if applyonly != True: es.fluxscale2(caltable = 'uid___A002_X87436c_Xb7a.ms.split.ampli_inf', removeOutliers=True, msName='uid___A002_X87436c_Xb7a.ms', writeToFile=True, preavg=10000)
  
  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.split.phase_inf') 
  gaincal(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    caltable = 'uid___A002_X87436c_Xb7a.ms.split.phase_inf',
    field = '0~0,2~3', # J0607-0834,Uranus,J0541-0541
    solint = 'inf',
    refant = 'CM02',
    gaintype = 'G',
    calmode = 'p',
    gaintable = 'uid___A002_X87436c_Xb7a.ms.split.bandpass_smooth20ch')
  
  if applyonly != True: es.checkCalTable('uid___A002_X87436c_Xb7a.ms.split.phase_inf', msName='uid___A002_X87436c_Xb7a.ms.split', interactive=False) 
  

# Save flags before applycal
mystep = 17
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  
  flagmanager(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    mode = 'save',
    versionname = 'BeforeApplycal')
  
  

# Application of the bandpass and gain cal tables
mystep = 18
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  for i in ['0', '2']: # J0607-0834,Uranus
    applycal(vis = 'uid___A002_X87436c_Xb7a.ms.split',
      field = str(i),
      gaintable = ['uid___A002_X87436c_Xb7a.ms.split.bandpass_smooth20ch', 'uid___A002_X87436c_Xb7a.ms.split.phase_int', 'uid___A002_X87436c_Xb7a.ms.split.flux_inf'],
      gainfield = ['', i, i],
      interp = 'linear,linear',
      calwt = T,
      flagbackup = F)
  
  applycal(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    field = '3,5~47', # OMC1_NW
    gaintable = ['uid___A002_X87436c_Xb7a.ms.split.bandpass_smooth20ch', 'uid___A002_X87436c_Xb7a.ms.split.phase_inf', 'uid___A002_X87436c_Xb7a.ms.split.flux_inf'],
    gainfield = ['', '3', '3'], # J0541-0541
    interp = 'linear,linear',
    calwt = T,
    flagbackup = F)
  

# Split out corrected column
mystep = 19
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_X87436c_Xb7a.ms.split.cal') 
  split(vis = 'uid___A002_X87436c_Xb7a.ms.split',
    outputvis = 'uid___A002_X87436c_Xb7a.ms.split.cal',
    datacolumn = 'corrected',
    keepflags = T)
  
  

# Save flags after applycal
mystep = 20
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  
  flagmanager(vis = 'uid___A002_X87436c_Xb7a.ms.split.cal',
    mode = 'save',
    versionname = 'AfterApplycal')
  
  

