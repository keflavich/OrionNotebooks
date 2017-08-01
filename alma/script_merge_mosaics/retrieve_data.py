from astroquery.alma import Alma

Alma.cache_location = '.'

rslt = Alma.query(payload={'pi_name':'Bally'}, public=False)

filtered_rslt = rslt[(rslt['Project code'].astype('str') == '2013.1.00546.S') & (rslt['Source name'] != 'Uranus')]

Alma.retrieve_data_from_uid(filtered_rslt['Member ous id'])
