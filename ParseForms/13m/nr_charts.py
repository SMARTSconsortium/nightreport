#!/Users/ih64/anaconda/bin/python
import matplotlib.pyplot as plt
import pylab
import numpy as np

def failurechart(sfsetcountdict):
	sfcount= [sfsetcountdict[key] for key in sfsetcountdict if key!= '']
	sfnum = len(sfcount)
	width = .35
	
	fig, ax = plt.subplots()
	rects = ax.bar(np.arange(sfnum), sfcount, width, color='orange')

	ax.set_ylabel('frequency')
	ax.set_xlabel('failures')
	#ax.set_title('SMARTS 1.3 + ANDICAM System Failures')
	ax.set_xticks(np.arange(sfnum)+(width/2))
	ax.set_xticklabels([i for i in sfsetcountdict])
	ax.set_xticklabels(('Dome','WC', 'IR', 'Prospero','Sync D+T', 'IC','TCS'))
	
	plt.savefig('systemfail.png')
	plt.close()
	return

def weatherchart(wsetcountdict):
	wcount= [wsetcountdict[key] for key in wsetcountdict]
	wnum = len(wcount)
	width = .35
	
	fig, ax = plt.subplots()
	rects = ax.bar(np.arange(wnum), wcount, width, color='purple')

	ax.set_ylabel('frequency')
	ax.set_xlabel('Weather Conditions')
	#ax.set_title('SMARTS 1.3 + Weather Conditions')
	ax.set_xticks(np.arange(wnum)+(width/2))
	ax.set_xticklabels(('o.cast', 'winds', 'clear', 'low temp', 'snow', 'humid', 't. cloud', 'p.o.cast', 'cloudy', 'rain'))

	#make the font for the tick labels smaller
	for tick in ax.xaxis.get_major_ticks():
        	tick.label.set_fontsize(10) 
	
	plt.savefig('weather.png')
	plt.close()
	return

def dispositionchart(dissetcountdict):
	discount=[dissetcountdict['minor technical problems'],dissetcountdict['major technical problems'],dissetcountdict['everything worked well']]
	disnum = 3
	width = .35
	
	fig, ax = plt.subplots()
	rects = ax.bar(np.arange(disnum), discount, width, color='blue')

	ax.set_ylabel('frequency')
	ax.set_xlabel('Disposition')
	ax.set_xticks(np.arange(disnum)+(width/2))
	ax.set_xticklabels(("minor technical prob.","major technical prob.","everything worked well"))
	
	plt.savefig('disposition.png')
	plt.close()
	return

def timepie(hours):
	pylab.figure(1, figsize=(6,6))
	ax = pylab.axes([0.1, 0.1, 0.8, 0.8])
	
	labels=[key for key in hours if hours[key] !=0]
	time=[hours[key] for key in hours if hours[key] !=0]
	explode=[.05 for i in time]

	pylab.pie(time, labels=labels, autopct='%1.1f%%', pctdistance=1.15, labeldistance= 1.3, startangle=90, explode=explode)
	#pylab.title("Time Breakdown", bbox={'pad':10})
	pylab.savefig('hours.png')
	plt.close()
	return

def condpie(condsetcountdict):
	pylab.figure(1, figsize=(6,6))
	ax = pylab.axes([0.1, 0.1, 0.8, 0.8])

	labels = [key for key in condsetcountdict if key!='Program used']
	values = [condsetcountdict[key] for key in condsetcountdict if key!='Program used']
	explode=[.05 for i in values]

	pylab.pie(values,labels=labels, autopct='%1.1f%%', explode=explode, startangle=90)
	#pylab.title("Observing Conditions")
	pylab.savefig('conditions.png')
	plt.close()
	return

def breakdownpie(projdict):
	pylab.figure(1, figsize=(6,6))
	ax = pylab.axes([0.1, 0.1, 0.8, 0.8])
	noaotime, chiletime, yaletime, lsutime = 0,0,0,0
	sunytime, gsutime, osutime, allotherstime = 0,0,0,0
	for key in projdict:
		if key.split('-')[0]=='NOAO':
			noaotime+=projdict[key]['time']
		elif key.split('-')[0]=='CHILE':
			chiletime+=projdict[key]['time']
		elif key.split('-')[0]=='YALE':
			yaletime+=projdict[key]['time']
		elif key.split('-')[0]=='LSU':
			lsutime+=projdict[key]['time']
		elif key.split('-')[0]=='SUNY':
			sunytime+=projdict[key]['time']
		elif key.split('-')[0]=='GSU':
			gsutime+=projdict[key]['time']
		elif key.split('-')[0]=='OSU':
			osutime+=projdict[key]['time']
		elif key.split('-')[0]!='STANDARD' and key.split('-')[0]!='STANDARDFIELD' and key.split('-')[0]!='ALL':
			allotherstime+=projdict[key]['time']

	times={"NOAO":noaotime, "CHILE":chiletime, "YALE":yaletime, "LSU":lsutime, "SUNY":sunytime, "GSU":gsutime, "OSU":osutime, "OTHERS":allotherstime}

	labels=[key for key in times if times[key] > 0]
	values=[times[key] for key in times if times[key] > 0]
	explode=[.05 for i in values]

	pylab.pie(values,labels=labels, autopct='%1.1f%%', explode=explode, startangle=90,  pctdistance=1.15, labeldistance= 1.3)

	pylab.savefig('breakdown.png')
	plt.close()
	return
