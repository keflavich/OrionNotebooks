__rethrow_casa_exceptions = True
h_init()
try:
    hif_restoredata (vis=['uid___A002_X960614_X39db', 'uid___A002_X9630c0_Xc26', 'uid___A002_X966cea_X14a4', 'uid___A002_X9d26c8_X39a', 'uid___A002_X9d4710_X1a57', 'uid___A002_X9d6f4c_X154'], session=['session_1', 'session_1', 'session_1', 'session_1', 'session_1', 'session_1'])
finally:
    h_save()
