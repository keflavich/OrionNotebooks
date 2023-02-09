__rethrow_casa_exceptions = True
h_init()
try:
    hif_restoredata (vis=['uid___A002_X86dcae_X416'], session=['session_1'])
finally:
    h_save()
