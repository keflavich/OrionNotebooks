import re

#if re.search('^4.3.0', casadef.casa_version) == None:
# sys.exit('ERROR: PLEASE USE THE SAME VERSION OF CASA THAT YOU USED FOR GENERATING THE SCRIPT: 4.3.0')


print "# Concatenating the data."

concat(vis = ['uid___A002_X872bbc_X412.ms.split.cal', 'uid___A002_X872bbc_X7c.ms.split.cal', 'uid___A002_X87436c_Xb7a.ms.split.cal', 'uid___A002_X87c075_X1066.ms.split.cal'],
  concatvis = 'calibrated.ms')


