se = '../science_goal.uid___A001_X122_X362/group.uid___A001_X122_X363/merge/Orion_SE_merge_7m_12m.ms'
nw = '../science_goal.uid___A001_X122_X35c/group.uid___A001_X122_X35d/merge/Orion_NW_merge_7m_12m.ms'

cvel(vis=se,
     outputvis='SE_merge_7m12m_CO2-1.ms',
     field='OMC1_SE',
     spw='0,4',
     mode='velocity',
     start='-240km/s',
     width='1.46km/s',
     nchan=300,
     outframe='LSRK',
     veltype='radio',
     restfreq='230.538GHz',
     phasecenter="J2000 05h35m17.448044 -05d22m43.00000",
    )

cvel(vis=nw,
     field='OMC1_NW',
     spw='0,4,8,12,16,20,24,28,32,36',
     mode='velocity',
     start='-240km/s',
     width='1.46km/s',
     nchan=300,
     outframe='LSRK',
     veltype='radio',
     restfreq='230.538GHz',
     phasecenter='J2000 5h35m12.023 -5d21m33.65',
    )
