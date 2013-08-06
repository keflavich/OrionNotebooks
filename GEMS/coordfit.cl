int n
for(n=47;n<=52;n+=1)
{
    if (n != 51) {
        delete("found"//str(n))
        ccfind("coords","found"//str(n), "mrgS20130131S00"//str(n)//".fits[SCI]", usewcs=yes, datamin=1000, center=yes, sbox=200)
        ccmap("found"//str(n), "ccmap"//str(n)//".db", images="mrgS20130131S00"//str(n)//".fits[SCI]", xcol=3, ycol=4, lngcol=1, latcol=2, update=yes)
        #cctran("ccmap"//str(n)//".db", "ccmap_trans"//str(n)//".db", 
    }
}

