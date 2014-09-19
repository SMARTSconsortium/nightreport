#!/Users/ih64/anaconda/bin/python
import pickle

def projectjar():

	uniqproj=['CHILE-06B-0288','CHILE-12B-0001','CHILE-13B-0039','CHILE-14A-0077','CHILE-14A-0106']
	uniqproj+=['DUBLIN-11B-000','GSU-03A-0006','GSU-14A-0001','KOVACS-14A-0001','LSU-11B-0003']
	uniqproj+=['LSU-14A-0001','MCSS-14A-0001','NOAO-13B-0270','NOAO-14A-0016','NOAO-14A-0257']
	uniqproj+=['NOAO-14A-0410','NOAO-14A-0468','OSU-03A-0001','OSU-03B-0001','SUNY-03A-0013']
	uniqproj+=['SUNY-03B-0001','SUNY-04A-0011','YALE-03A-0001','YALE-08A-0001']
	uniqproj+=['ALL','Project','STANDARD','STANDARDFIELD']
	projdict=dict(zip([i for i in uniqproj],[{"time":0, "nexp":0} for i in range(0,len(uniqproj))]))
	pickle.dump(projdict,open('projdictPickle','w'))
	return

def tally(log):
	with open(log) as f:
		wholetext=f.read()
	lines=wholetext.split('\n')
	linesList=[i.split() for i in lines]
	linesList[-1]=linesList[0]

	projdict=pickle.load(open('projdictPickle','r'))


	index=1
	while index < len(linesList)-1:
		projectnow=linesList[index][0]
		timenow=linesList[index][-3]
		targetnow=linesList[index][2]
		while linesList[index][0] == projectnow and index < len(linesList)-1 and linesList[index][2] == targetnow:
			timenext=linesList[index][-3]
			expnext=eval(linesList[index][-8])
			index=index+1
		elapsed=(float(timenext)-float(timenow))*86400 + expnext
		projdict[str(projectnow)]["nexp"]+=1
		projdict[str(projectnow)]["time"]+=elapsed
	pickle.dump(projdict,open('projdictPickle','w'))
	return projdict
