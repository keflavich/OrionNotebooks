__rethrow_casa_exceptions = True
h_init()
try:
    hif_restoredata (vis=['uid___A002_X9707f1_Xfee'], session=['session_1'])
finally:
    h_save()
