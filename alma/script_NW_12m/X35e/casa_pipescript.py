from recipes.almahelpers import fixsyscaltimes # SACM/JAO - Fixes
__rethrow_casa_exceptions = True
h_init()
try:
    hifa_importdata(vis=['uid___A002_X960614_X39db', 'uid___A002_X9630c0_Xc26', 'uid___A002_X966cea_X14a4', 'uid___A002_X9d26c8_X39a', 'uid___A002_X9d4710_X1a57', 'uid___A002_X9d6f4c_X154'], session=['session_1', 'session_2', 'session_3', 'session_4', 'session_5', 'session_6'])
    fixsyscaltimes(vis = 'uid___A002_X960614_X39db.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_X9630c0_Xc26.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_X966cea_X14a4.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_X9d26c8_X39a.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_X9d4710_X1a57.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_X9d6f4c_X154.ms')# SACM/JAO - Fixes
    h_save() # SACM/JAO - Finish weblog after fixes
    h_init() # SACM/JAO - Restart weblog after fixes
    hifa_importdata(vis=['uid___A002_X960614_X39db', 'uid___A002_X9630c0_Xc26', 'uid___A002_X966cea_X14a4', 'uid___A002_X9d26c8_X39a', 'uid___A002_X9d4710_X1a57', 'uid___A002_X9d6f4c_X154'], session=['session_1', 'session_2', 'session_3', 'session_4', 'session_5', 'session_6'])
    hifa_flagdata(pipelinemode="automatic")
    hifa_fluxcalflag(pipelinemode="automatic")
    hif_refant(pipelinemode="automatic")
    hifa_tsyscal(pipelinemode="automatic")
    hifa_tsysflag(pipelinemode="automatic")
    hifa_wvrgcalflag(pipelinemode="automatic")
    hif_lowgainflag(pipelinemode="automatic")
    hif_setjy(pipelinemode="automatic")
    hif_bandpass(pipelinemode="automatic")
    hif_bpflagchans(pipelinemode="automatic")
    hifa_gfluxscale(pipelinemode="automatic")
    hifa_timegaincal(pipelinemode="automatic")
    hif_applycal(pipelinemode="automatic")
    hif_makecleanlist(intent='PHASE,BANDPASS,CHECK')
    hif_cleanlist(pipelinemode="automatic")
finally:
    h_save()
