#!/Users/ih64/anaconda/bin/python
import matplotlib.pyplot as plt
import pylab
import numpy as np

def failurechart(sfsetcountdict,date,tele):
	#each telescope sufferes from different problems
	#the dict ticklabel will hold the different response options and shorter versions
	#that can be easily written on the axis of the bar graph
	if tele==1.3:
		ticklabel={"Dome Failure (shutter/motor/tracking) ":"Dome", "WC computer failed":"WC",
			"IR computer failed":"IR", "Failure with Prospero":"Prospero",
			"Synchronization problems between the dome and the telescope":"Sync D+T",
			"IC computer failed":"IC", "Failures with TCS":"TCS"}
	elif tele==1.5:
		ticklabel={'failures with the communication Between Chiron Website and TCS':'Web+TCS',
				'Communication failure between CHIRON website and CHIRON GUI':"Web+GUI",
				'Failures with the TCS':'TCS',
				'Synchronization problems between the dome and telescope':"Sync D+T",
				'Failures with the CTIO PC GUIDER':'PC GUIDER',
				"Problems with the dome's motor":'Dome','Problems with the Pointing':"Pointing"}

	sfcount= [sfsetcountdict[key] for key in sfsetcountdict if key in ticklabel]
	sfnum = len(sfcount)
	width = .35

	fig, ax = plt.subplots()
	rects = ax.bar(np.arange(sfnum), sfcount, width, color='orange')

	ax.set_ylabel('frequency')
	ax.set_xlabel('failures')
	#ax.set_title('SMARTS 1.3 + ANDICAM System Failures')
	ax.set_xticks(np.arange(sfnum)+(width/2))
	ax.set_xticklabels([ticklabel[i] for i in sfsetcountdict if i in ticklabel])
	#ax.set_xticklabels(('Dome','WC', 'IR', 'Prospero','Sync D+T', 'IC','TCS'))
	
	plt.savefig(str(tele)+'-m-'+date+'systemfail.png')
	plt.close()
	return

def weatherchart(wsetcountdict,date,tele):
	ticklabel={"strong winds":"winds", "clear":"clear", "overcast":"o.cast", "snow":"snow",
		"rain":"rain", "thin clouds":"t.cloud", "partial overcast":"p.o.cast", 
		"high humidity":"humid", "cloudy":"cloudy"}

	wcount= [wsetcountdict[key] for key in wsetcountdict if key in ticklabel]
	wnum = len(wcount)
	width = .35	

	fig, ax = plt.subplots()
	rects = ax.bar(np.arange(wnum), wcount, width, color='purple')

	ax.set_ylabel('frequency')
	ax.set_xlabel('Weather Conditions')
	#ax.set_title('SMARTS 1.3 + Weather Conditions')
	ax.set_xticks(np.arange(wnum)+(width/2))
	ax.set_xticklabels([ticklabel[i] for i in wsetcountdict if i in ticklabel])

	#make the font for the tick labels smaller
	for tick in ax.xaxis.get_major_ticks():
        	tick.label.set_fontsize(10) 
	
	plt.savefig(str(tele)+'-m-'+date+'weather.png')
	plt.close()
	return

def dispositionchart(dissetcountdict,date,tele):
	#discount=[dissetcountdict['minor technical problems'],dissetcountdict['major technical problems'],dissetcountdict['everything worked well']]
	keylist=['minor technical problems','major technical problems','everything worked well']
	discount=[]
	for i in keylist:
		try:
			discount.append(dissetcountdict[i])
		except KeyError:
			discount.append(0)
	disnum = 3
	width = .35
	
	fig, ax = plt.subplots()
	rects = ax.bar(np.arange(disnum), discount, width, color='blue')

	ax.set_ylabel('frequency')
	ax.set_xlabel('Disposition')
	ax.set_xticks(np.arange(disnum)+(width/2))
	ax.set_xticklabels(("minor technical prob.","major technical prob.","everything worked well"))
	
	plt.savefig(str(tele)+'-m-'+date+'disposition.png')
	plt.close()
	return

def seeingtime(times,seeing,mask,date,tele):
	numlines=len(seeing)
	colorlist=['r-o','g-o','b-o']
	if len(seeing)==2:
		labelList=['Max','Min']
	elif len(seeing)==3:
		labelList=['BON','MON','EON']
	fig, ax = plt.subplots()
	for i in range(numlines):
		X=times[mask[i]]
		Y=seeing[i][mask[i]].__array__().astype('float')
		ax.plot(X, Y, colorlist[i], label=labelList[i])
	ax.legend(loc='upper right')
	ax.set_ylabel('seeing')
	ax.set_xlabel('time')

	fig.autofmt_xdate()

	plt.savefig(str(tele)+'-m-'+date+'seeing.png')
	plt.close()
	return


def timepie(hours,date,tele):
	pylab.figure(1, figsize=(6,6))
	ax = pylab.axes([0.1, 0.1, 0.8, 0.8])
	
	labels=[key for key in hours if hours[key] !=0]
	time=[hours[key] for key in hours if hours[key] !=0]
	explode=[.05 for i in time]

	pylab.pie(time, labels=labels, autopct='%1.1f%%', pctdistance=1.15, labeldistance= 1.3, startangle=90, explode=explode)
	#pylab.title("Time Breakdown", bbox={'pad':10})
	pylab.savefig(str(tele)+'-m-'+date+'hours.png')
	plt.close()
	return

def condpie(condsetcountdict,date):
	pylab.figure(1, figsize=(6,6))
	ax = pylab.axes([0.1, 0.1, 0.8, 0.8])

	labels = [key[0:4]+'.' for key in condsetcountdict if key!='Program used']
	values = [condsetcountdict[key] for key in condsetcountdict if key!='Program used']
	explode=[.05 for i in values]

	pylab.pie(values,labels=labels, autopct='%1.1f%%', explode=explode, startangle=90)
	#pylab.title("Observing Conditions")
	pylab.savefig(date+'conditions.png')
	plt.close()
	return

def breakdownpie(projdict,datestart):
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

	pylab.savefig(datestart+'breakdown.png')
	plt.close()
	return
