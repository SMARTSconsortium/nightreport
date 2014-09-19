#!/Users/ih64/anaconda/bin/python
import pickle

uniqproj=['CHILE-06B-0288','CHILE-13B-0039','CHILE-14A-0077','CHILE-14A-0106','CHILE-14B-0013']
uniqproj+=['DUBLIN-11B-000','ESA-14B-0002','GSU-03A-0006','GSU-14A-0001','KOVACS-14A-0001']
uniqproj+=['LSU-14A-0001','MANLY-14B-0001','MCSS-14A-0001','NOAO-08B-0001','NOAO-11B-0005','NOAO-13B-0270','NOAO-13B-0389']
uniqproj+=['NOAO-14A-0410','NOAO-14B-0127','NOAO-14B-0243','OSU-03A-0001','OSU-03B-0001','SUNY-03A-0013']
uniqproj+=['SUNY-03B-0001','SUNY-04A-0011','YALE-03A-0001','YALE-08A-0001']
uniqproj+=['ALL','Project','STANDARD','STANDARDFIELD']
projdict=dict(zip([i for i in uniqproj],[{"time":0, "nexp":0} for i in range(0,len(uniqproj))]))
pickle.dump(projdict,open('projdictPickle','w'))
