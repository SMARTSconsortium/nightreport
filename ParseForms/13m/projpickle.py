#!/Users/ih64/anaconda/bin/python
import pickle

uniqproj=['CHILE-06B-0288','CHILE-12B-0001','CHILE-13B-0039','CHILE-14A-0077','CHILE-14A-0106']
uniqproj+=['DUBLIN-11B-000','GSU-03A-0006','GSU-14A-0001','KOVACS-14A-0001','LSU-11B-0003']
uniqproj+=['LSU-14A-0001','MCSS-14A-0001','NOAO-13B-0270','NOAO-14A-0016','NOAO-14A-0257']
uniqproj+=['NOAO-14A-0410','NOAO-14A-0468','OSU-03A-0001','OSU-03B-0001','SUNY-03A-0013']
uniqproj+=['SUNY-03B-0001','SUNY-04A-0011','YALE-03A-0001','YALE-08A-0001']
uniqproj+=['ALL','Project','STANDARD','STANDARDFIELD']
projdict=dict(zip([i for i in uniqproj],[{"time":0, "nexp":0} for i in range(0,len(uniqproj))]))
pickle.dump(projdict,open('projdictPickle','w'))