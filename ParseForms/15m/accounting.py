#!/opt/anaconda/bin/python
import pickle
from astropy.io import ascii

def projectjar():

	uniqproj=['CHILE-06B-0288','CHILE-13B-0039','CHILE-14A-0077','CHILE-14A-0106','CHILE-14B-0013']
	uniqproj+=['DUBLIN-11B-000','ESA-14B-0002','GSU-03A-0006','GSU-14A-0001','KOVACS-14A-0001']
	uniqproj+=['LSU-14A-0001','MANLY-14B-0001','MCSS-14A-0001','NOAO-08B-0001','NOAO-11B-0005','NOAO-13B-0270','NOAO-13B-0389']
	uniqproj+=['NOAO-14A-0410','NOAO-14B-0127','NOAO-14B-0243','OSU-03A-0001','OSU-03B-0001','SUNY-03A-0013']
	uniqproj+=['SUNY-03B-0001','SUNY-04A-0011','YALE-03A-0001','YALE-08A-0001']
	uniqproj+=['ALL','Project','STANDARD','STANDARDFIELD']
	projdict=dict(zip([i for i in uniqproj],[{"time":0, "nexp":0} for i in range(0,len(uniqproj))]))
	pickle.dump(projdict,open('projdictPickle','w'))
	return

#depricated, cant handle crappy headers. use tallyascii below instead
def tally(log):
	lines=log.split('\n')
	linesList=[i.split() for i in lines]
	linesList[-1]=linesList[0]
	#linesList.pop(len(linesList)-1)	#last one is empy list
	'''
	uniqproj=['CHILE-06B-0288','CHILE-13B-0039','CHILE-14A-0077','CHILE-14A-0106','CHILE-14B-0013']
	uniqproj+=['DUBLIN-11B-000','ESA-14B-0002','GSU-03A-0006','GSU-14A-0001','KOVACS-14A-0001']
	uniqproj+=['LSU-14A-0001','MANLY-14B-0001','MCSS-14A-0001','NOAO-08B-0001','NOAO-11B-0005','NOAO-13B-0270','NOAO-13B-0389']
	uniqproj+=['NOAO-14A-0410','NOAO-14B-0127','NOAO-14B-0243','OSU-03A-0001','OSU-03B-0001','SUNY-03A-0013']
	uniqproj+=['SUNY-03B-0001','SUNY-04A-0011','YALE-03A-0001','YALE-08A-0001']
	#uniqproj=set([i[0] for i in linesList])
	projdict=dict(zip([i for i in uniqproj],[{"time":0, "nexp":0} for i in range(0,len(uniqproj))]))
	'''
	projdict=pickle.load(open('projdictPickle','r'))


	index=1
	while index < len(linesList)-1:
		projectnow=linesList[index][0]
		timenow=linesList[index][-3]
		targetnow=linesList[index][2]
		while linesList[index][0] == projectnow and index < len(linesList)-1 and linesList[index][2] == targetnow:
			timenext=linesList[index][-3]
			#print eval(linesList[index][-8])
			expnext=eval(linesList[index][-8])
			index=index+1
		elapsed=(float(timenext)-float(timenow))*86400 + expnext
		try:
			projdict[str(projectnow)]["nexp"]+=1
			projdict[str(projectnow)]["time"]+=elapsed
		except KeyError:
			pass
	pickle.dump(projdict,open('projdictPickle','w'))
	return projdict

def tallyascii(log):
	#this is a really hacky way of adding delimiters into the header
	#its necessary to do this to help ascii read the file properly
	log[0]= log[0].replace(' Im', '|Im').replace(' Ob','|Ob').replace(' Exp','|Exp').replace(' Fil','|Fil').replace(' LS','|LS').replace(' UT','|UT').replace(' JD','|JD').replace(' Fil','|Fil').replace(' [L','|[L')
	table=ascii.read(log, format='fixed_width',delimiter="|")
	projdict=pickle.load(open('projdictPickle','r'))
	index=0
	while index < len(table)-1:
		projectnow=table['Project'][index]
		timenow=table['JD'][index]
		targetnow=table['Object'][index]
		while table['Project'][index] == projectnow and index < len(table)-1 and table['Object'][index] == targetnow:
			timenext=table['JD'][index]
			expnext=table['ExpTime'][index]
			index=index+1
		elapsed=(timenext-timenow)*86400 + expnext
		try:
			projdict[str(projectnow)]["nexp"]+=1
			projdict[str(projectnow)]["time"]+=elapsed
		except KeyError:
			pass
	pickle.dump(projdict,open('projdictPickle','w'))
	return projdict
