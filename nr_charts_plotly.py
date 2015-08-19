import plotly.plotly as py
from plotly.graph_objs import *

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

	x=[]
	y=[]

	for key in sfsetcountdict:
		if key in ticklabel:
			x.append(ticklabel[key])
			y.append(sfsetcountdict[key])

	data=Data([
		Bar(
			x=x,
			y=y,
			marker=Marker(color='rgb(158,202,225)',opacity=0.7)
		)
	
	])

	plot_url=py.plot(data, filename=str(tele)+'-m-'+date+'systemfail',auto_open=False)
	snippet='<iframe width=750 height=500 frameborder="0" seamless="seamless" scrolling="no" src="'+plot_url+'.embed"></iframe>'
	return snippet


def weatherchart(wsetcountdict,date,tele):
	ticklabel={"strong winds":"winds", "clear":"clear", "overcast":"overcast", "snow":"snow",
		"rain":"rain", "thin clouds":"thin clouds", "partial overcast":"partial overcast", 
		"high humidity":"high humid", "cloudy":"cloudy", "cirrus":"cirrus"}
	#sfcount= [sfsetcountdict[key] for key in sfsetcountdict if key in ticklabel]

	x=[]
	y=[]
	
	for key in wsetcountdict:
		if key in ticklabel:
			x.append(ticklabel[key])
			y.append(wsetcountdict[key])

	data=Data([
		Bar(
			x=x,
			y=y,
			marker=Marker(color='rgb(222,95,95)',opacity=0.5)
		)
	
	])

	plot_url=py.plot(data, filename=str(tele)+'-m-'+date+'weather',auto_open=False)
	snippet='<iframe width=750 height=500 frameborder="0" seamless="seamless" scrolling="no" src="'+plot_url+'.embed"></iframe>'
	return snippet


def dispositionchart(dissetcountdict,date,tele):
	#discount=[dissetcountdict['minor technical problems'],dissetcountdict['major technical problems'],dissetcountdict['everything worked well']]
	keylist=['minor technical problems','major technical problems','everything worked well']
	discount=[]
	for i in keylist:
		try:
			discount.append(dissetcountdict[i])
		except KeyError:
			discount.append(0)
	data=Data([
		Bar(
			x=keylist,
			y=discount,
			marker=Marker(color='rgb(142,124,195)',opacity=0.5)
		)
	
	])
	plot_url=py.plot(data, filename=str(tele)+'-m-'+date+'disposition',auto_open=False)
	snippet='<iframe width=750 height=500 frameborder="0" seamless="seamless" scrolling="no" src="'+plot_url+'.embed"></iframe>'
	return snippet


def condpie(condsetcountdict,date):

	labels=[]
	values=[]

	for key in condsetcountdict:
		labels.append(key)
		values.append(condsetcountdict[key])

	fig = {
		'data':[{'labels':labels,
			'values':values,
			'type':'pie',
			'name':'Program Used',
			'hoverinfo':'label+value+name'
			}],
		'layout':{'showlegend':True}
	}
	plot_url=py.plot(fig,validate=False,filename=date+'conditions',auto_open=False)
	snippet='<iframe width=750 height=500 frameborder="0" seamless="seamless" scrolling="no" src="'+plot_url+'.embed"></iframe>'
	return snippet

def timepie(hours,date,tele):

	labels=[]
	values=[]

	for key in hours:
		if hours[key] > 0:
			labels.append(key)
			values.append(hours[key])
	fig = {
		'data':[{'labels':labels,
			'values':values,
			'type':'pie',
			'name':'hours spent',
			'hoverinfo':'label+value+name'
			}],
		'layout':{'showlegend':True}
	}

	plot_url=py.plot(fig,validate=False,filename=str(tele)+'-m-'+date+'hours',auto_open=False)
	snippet='<iframe width=750 height=500 frameborder="0" seamless="seamless" scrolling="no" src="'+plot_url+'.embed"></iframe>'
	return snippet


def breakdownpie(projdict,datestart):
	noaotime, chiletime, yaletime = 0,0,0,
	sunytime, gsutime, osutime, allotherstime = 0,0,0,0
	for key in projdict:
		if key.split('-')[0]=='NOAO':
			noaotime+=projdict[key]['time']
		elif key.split('-')[0]=='CHILE':
			chiletime+=projdict[key]['time']
		elif key.split('-')[0]=='YALE':
			yaletime+=projdict[key]['time']
		elif key.split('-')[0]=='SUNY':
			sunytime+=projdict[key]['time']
		elif key.split('-')[0]=='GSU':
			gsutime+=projdict[key]['time']
		elif key.split('-')[0]=='OSU':
			osutime+=projdict[key]['time']
		elif key.split('-')[0]!='STANDARD' and key.split('-')[0]!='STANDARDFIELD' and key.split('-')[0]!='ALL' and key.split('-')[0]!='TEST':
			allotherstime+=projdict[key]['time']

	times={"NOAO":noaotime, "CHILE":chiletime, "YALE":yaletime, "SUNY":sunytime, "GSU":gsutime, "OSU":osutime, "OTHERS":allotherstime}

	labels=[]
	values=[]

	for key in times:
		if times[key] > 0:
			labels.append(key)
			values.append(times[key]/3600.0)
	fig = {
		'data':[{'labels':labels,
			'values':values,
			'type':'pie',
			'name':'institution',
			'hoverinfo':'label+value+name'
			}],
		'layout':{'showlegend':True}
	}

	plot_url=py.plot(fig,validate=False,filename=datestart+'breakdown',auto_open=False)
	snippet='<iframe width=750 height=500 frameborder="0" seamless="seamless" scrolling="no" src="'+plot_url+'.embed"></iframe>'
	return snippet


def seeingtime(times,seeing,mask,date,tele):
	if len(seeing) ==2:
		trace0= Scatter(
			x=times[mask[0]],
			y=seeing[0][mask[0]].__array__().astype('float'),
			name='Max',
			line=Line(
				color='rgb(219,64,82)',
				width=2,
			)
		)

		trace1= Scatter(
			x=times[mask[1]],
			y=seeing[1][mask[1]].__array__().astype('float'),
			name='Min',
			line=Line(
				color='rgb(55,128,191)',
				width=2,
			)
		)
		data=Data([trace0,trace1])
	else:
		trace0= Scatter(
			x=times[mask[0]],
			y=seeing[0][mask[0]].__array__().astype('float'),
			name='BON',
			mode='lines+markers',
			line=Line(
				color='rgb(219,64,82)',
				width=2,
			)
		)

		trace1= Scatter(
			x=times[mask[1]],
			y=seeing[1][mask[1]].__array__().astype('float'),
			name='MON',
			mode='lines+markers',
			line=Line(
				color='rgb(55,128,191)',
				width=2,
			)
		)

		trace2= Scatter(
			x=times[mask[2]],
			y=seeing[2][mask[2]].__array__().astype('float'),
			name='EON',
			mode='lines+markers',
			line=Line(
				color='rgb(128,0,128)',
				width=2,
			)
		)
		data=Data([trace0,trace1,trace2])
	plot_url=py.plot(data,filename=str(tele)+'-m-'+date+'seeing',auto_open=False)
	snippet='<iframe width=750 height=500 frameborder="0" seamless="seamless" scrolling="no" src="'+plot_url+'.embed"></iframe>'
	return snippet
