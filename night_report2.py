#!/Users/ih64/anaconda/bin/python
#this is a more cleanly written version of the night report
#it will use some more librarys to make things easier
#it will also have an easy execution from the command line
import urllib2, sys, datetime, calendar, itertools, glob
from astropy.io import ascii
import pandas as pd
import numpy as np
import nr_charts

#fetch the response sheet formated as tsv from google
#return the sheet as an astropy ascii table
def ReadResponse(tele):
	if tele==1.5:
		#this long url is where the tsv response form lives
		response=urllib2.urlopen('https://docs.google.com/spreadsheet/pub?key=0AqOsF57HNy0kdEVYaFcyaFJxQlhpdTQxQ094WXI3b3c&single=true&gid=0&output=tsv')
	elif tele==1.3:
		response=urllib2.urlopen('https://docs.google.com/spreadsheet/pub?key=0AqOsF57HNy0kdFV6ME5ncnJlQWZKM0dHMW0xTlo1eVE&single=true&gid=0&output=tsv')
	rSheet=response.read()
	rTable=ascii.read(rSheet)
	return rTable

#count the unique occourances of all values in a column
def countUniq(table,columnName):
	#first flatten out the column
	listOfLists=[i.split(', ') for i in table[columnName].__array__()]
	flatList=list(itertools.chain(*listOfLists))
	flatArray=np.array(flatList)
	#find the unique values
	key, keyindex = np.unique(flatArray,return_inverse=True)
	setcountdict={}
	for i in range(len(key)):
		setcountdict[key[i]]=len(np.where(keyindex==i)[0])
	return setcountdict

#calculate mean, max, min of a column
def columnCalc(table,columnName):
	#filter out na fields and convert to float type so we can calculate
	columnArray=table[columnName][np.where(table[columnName]!='n/a')].__array__().astype('float')
	columnStats={"max":columnArray.max(), "min":columnArray.min(),"mean":np.around(columnArray.mean(),decimals=1)}
	return columnStats

#given a dict, print out an html table of the key value pairs
def parseHTMLtable(columnDict,fHandle,thead):
	fHandle.write('<table><tr><th>'+thead[0]+'</th><th>'+thead[1]+'</th></tr>')
	for key in columnDict:
		if key == '0':
			fHandle.write('<tr><td>None</td><td>'+str(columnDict[key])+'</td></tr>')
		else:
			fHandle.write('<tr><td>'+key+'</td><td>'+str(columnDict[key])+'</td></tr>')
	fHandle.write('</table>')
	return

def logapi(datestart):
	year='20'+datestart[0:2]
	month=datestart[2:4]

	calendar={"01":"Jan", "02":"Feb", "03":"Mar", "04":"Apr", "05":"May", "06":"Jun",
		"07":"Jul", "08":"Aug", "09":"Sep", "10":"Oct", "11":"Nov", "12":"Dec"}

	urlroot="http://www.astronomy.ohio-state.edu/ANDICAM/ObsLogs/"
	
	request=urlroot+year+"/"+calendar[month]+"/"+'20'+datestart+".log"

	try:
		log=pd.io.parsers.read_fwf(request)
		log.Project=log.Project.replace(np.nan, 'ALL')
		return log
	except urllib2.HTTPError, e:
		print request+" not found"
		return pd.DataFrame()

def tallyascii(datestart):
	projdict={}
	#tally of nights with no observing
	noObs=0
	#figure out how many days there are in the month being processed
	monthLength=calendar.monthrange(2000+int(datestart[0:2]),int(datestart[2:4]))[1]
	for i in np.arange(int(datestart),int(datestart)+monthLength):
		table=logapi(str(i))
		if table.empty is not True:
			index=0
			j=index+1
			while j < len(table)-1:
				projectnow=table['Project'][index]
				timenow=table['JD'][index]
				targetnow=table['Object'][index]
				while table['Project'][j] == projectnow and j < len(table)-1 and table['Object'][j] == targetnow:
					j=j+1
				elapsed=(table['JD'][j-1]-timenow)*86400 + table['ExpTime'][j-1]
				try:
					projdict[projectnow]["nexp"]+=1
					projdict[projectnow]["time"]+=elapsed
				except KeyError:
					if projectnow != 'ALL' and projectnow != 'STANDARD' and projectnow != 'STANDARDFIELD':
						projdict[projectnow]={"nexp":1, "time":elapsed}
					else:
						pass
				index=j
				j+=1
		else:
			noObs+=1
	return [projdict,noObs]

#datestart is yymmdd, tele is either 1.3 or 1.5 (float)
def createHTML(datestart,tele):
	table=ReadResponse(tele)
	tableMonth=table[ (table['SMARTS Date (BON)'] >= int(datestart)) 
		& (table['SMARTS Date (BON)'] < int(datestart) + 100)]

	weather=countUniq(tableMonth,'Weather Types Experienced')
	sysfail=countUniq(tableMonth, 'System Failures Experienced')
	disposition=countUniq(tableMonth, 'Disposition of the Night')

	hrobs=tableMonth['Hours Observing [Scheduled Science]'].sum()
	hrswthr=tableMonth['Hours Lost to Weather'].sum()
	hreng=tableMonth['Hours Engineering'].sum()
	hrsys=tableMonth['Hours Lost to System Failures'].sum()
	hrsToO=tableMonth['Hours spent doing ToO'].sum()

	hours={"observing":hrobs, "weather":hrswthr, "engineering":hreng, "sys_failure":hrsys, "ToO":hrsToO}

	#make charts
	nr_charts.dispositionchart(disposition,datestart,tele)
	nr_charts.weatherchart(weather,datestart,tele)
	nr_charts.failurechart(sysfail,datestart,tele)
	nr_charts.timepie(hours,datestart,tele)

	#make the html page
	fileHTML=open(str(tele)+'-m-'+datestart+'report.html','w')
	fileHTML.write('<html>')
	fileHTML.write('<head><link rel="stylesheet" href="css/style.css" type="text/css"></head>')
	fileHTML.write('<body><h1>SMARTS '+str(tele)+'-m Night Report Summary '+datestart+'</h1>')
	fileHTML.write('<p><em>created on '+datetime.datetime.today().isoformat(' ')+'</em></p>')
	fileHTML.write('<p><em>Total Nights :'+str(len(tableMonth))+'</em></p>')

	if tele==1.3:
		bonseestat=columnCalc(tableMonth,'Seeing (BON)')
		monseestat=columnCalc(tableMonth,'Seeing (Middle of Night)')
		eonseestat=columnCalc(tableMonth,'Seeing (EON)')
		projdict, noObs = tallyascii(datestart)
		fileHTML.write('<p><em>Nights With No Observing : '+str(noObs)+'</em></p>')
		fileHTML.write('<fieldset><h3>Observing Conditions</h3>')
		cond=countUniq(tableMonth,'Program used')
		nr_charts.condpie(cond,datestart)
		fileHTML.write('<img src="images/'+datestart+'conditions.png" align="left" width="500px">')
		parseHTMLtable(cond,fileHTML,['Program Used','Total'])
		fileHTML.write('</fieldset>')

		fileHTML.write('<fieldset><h3>Science Observation Break Down</h3>')
		projtime={}
		for key in projdict:
			projtime[key]=np.around(projdict[key]['time']/3600, decimals=1)
		nr_charts.breakdownpie(projdict,datestart)
		fileHTML.write('<img src="images/'+datestart+'breakdown.png" align="left" width="500px">')
		parseHTMLtable(projtime,fileHTML,['Project ID','Hours'])
		fileHTML.write('</fieldset>')

		fileHTML.write('<fieldset><h3>Seeing Conditions</h3>')
		bonclean=np.where(tableMonth['Seeing (BON)'].__array__()!='n/a')
		monclean=np.where(tableMonth['Seeing (Middle of Night)'].__array__()!='n/a')
		eonclean=np.where(tableMonth['Seeing (EON)'].__array__()!='n/a')

		times=np.array([datetime.datetime.strptime(i, "%m/%d/%Y %H:%M:%S") 
			for i in tableMonth['Timestamp'].__array__()])

		nr_charts.seeingtime(times,[tableMonth['Seeing (BON)'],tableMonth['Seeing (Middle of Night)'],tableMonth['Seeing (EON)']],
			[bonclean,monclean,eonclean],datestart,tele)

		fileHTML.write('<img src="images/'+str(tele)+'-m-'+datestart+'seeing.png" align="left" width="500px">')
		parseHTMLtable(bonseestat,fileHTML,['BON Statistic','Seeing Value'])
		fileHTML.write('<br><br>')
		parseHTMLtable(monseestat,fileHTML,['MON Statistic','Seeing Value'])
		fileHTML.write('<br><br>')
		parseHTMLtable(eonseestat,fileHTML,['EON Statistic','Seeing Value'])
		fileHTML.write('</fieldset>')

	elif tele==1.5:
		fileHTML.write('<fieldset><h3>Seeing Conditions</h3>')

		maxseestat=columnCalc(tableMonth,'Maximum Seeing')
		minseestat=columnCalc(tableMonth,'Minimum Seeing')
		maxsclean=np.where(tableMonth['Maximum Seeing'].__array__()!='n/a')
		minsclean=np.where(tableMonth['Minimum Seeing'].__array__()!='n/a')

		times=np.array([datetime.datetime.strptime(i, "%m/%d/%Y %H:%M:%S") 
			for i in tableMonth['Timestamp'].__array__()])

		nr_charts.seeingtime(times,[tableMonth['Maximum Seeing'],tableMonth['Minimum Seeing']],
			[maxsclean,minsclean],datestart,tele)

		fileHTML.write('<img src="images/'+str(tele)+'-m-'+datestart+'seeing.png" align="left" width="500px">')

		parseHTMLtable(maxseestat,fileHTML,['BON Statistic','Seeing Value'])
		fileHTML.write('<br><br>')
		parseHTMLtable(minseestat,fileHTML,['EON Statistic','Seeing Value'])
		
		fileHTML.write('</fieldset>')

	fileHTML.write('<fieldset><h3>Time Loss & Observing</h3>')
	fileHTML.write('<img src="images/'+str(tele)+'-m-'+datestart+'hours.png" align="left" width="500px">')
	parseHTMLtable(hours,fileHTML,['task','hours'])
	fileHTML.write('</fieldset>')

	fileHTML.write('<fieldset>')
	fileHTML.write('<h3>Weather Conditions</h3>')
	fileHTML.write('<img src="images/'+str(tele)+'-m-'+datestart+'weather.png" align="left" width="500px">')
	parseHTMLtable(weather,fileHTML,['conditions','freq.'])
	fileHTML.write('</fieldset>')
	
	fileHTML.write('<fieldset><h3>System Failures</h3>')
	fileHTML.write('<img src="images/'+str(tele)+'-m-'+datestart+'systemfail.png" align="left" width="500px">')
	parseHTMLtable(sysfail,fileHTML,['failure','freq.'])
	fileHTML.write('</fieldset>')
	
	fileHTML.write('<fieldset><h3>Night Disposition</h3>')
	fileHTML.write('<img src="images/'+str(tele)+'-m-'+datestart+'disposition.png" align="left" width="500px">')
	parseHTMLtable(disposition,fileHTML,['Disposition','freq.'])
	fileHTML.write('</fieldset>')

	fileHTML.write('</body></html>')
	fileHTML.close()
	return

def makeHome():
	home=open('index.html','w')
	pages=sorted(glob.glob('1.*.html'))

	home.write('<html>\n<head>\n<link rel="stylesheet" href="css/style.css" type="text/css">\n<title>SMARTS Night Report</title>\n</head>\n')
	home.write('<body>\n')
	home.write('<h1>SMARTS Night Report System</h1>\n')
	home.write('<div id="container">\n')
	home.write("<h3>Observer's Night Report Forms</h3>\n<a href='http://bit.ly/SMARTS13mEONform'>SMARTS 1.3m</a>\n<a href='http://bit.ly/SMARTS15mEONform'>SMARTS 1.5m</a>\n")
	home.write('<h3>Night Report Responses</h3>\n<a href="http://bit.ly/SMARTS13mresponse">SMARTS 1.3m</a>\n<a href="http://bit.ly/SMARTS15mresponse">SMARTS 1.5m</a>\n')
	home.write("<h3>Observer's Trouble Report Forms</h3>\n<a href='https://docs.google.com/forms/d/1M59YLZVds8-pKGljzN2nub_WSySj8qGkkACBvHP6sFI/viewform'>SMARTS 1.3m</a>\n<a href='https://docs.google.com/forms/d/1IrpJ6Xedz9x4345J6jdaTJNxbCr-FG30dzUWyFYbfxc/viewform'>SMARTS 1.5m</a>\n")
	home.write('<h3>Trouble Report Responses</h3>\n<a href="https://docs.google.com/spreadsheets/d/1oYMZaFaVjWjGnXSCAMXCJR72qoIw2abCrIJqf19zGdQ/pubhtml">SMARTS 1.3m</a>\n<a href="https://docs.google.com/spreadsheets/d/1c1eF9zeZEW5DRBTYNd6oMDeg_EQgdmwfCByo59yrbUM/pubhtml?gid=791702439&single=true">SMARTS 1.5m</a>\n')
	home.write('<h3>Monthly Summaries</h3>\n<table>\n<tr><th>SMARTS 1.3-m</th><th>SMARTS 1.5-m</th></tr>\n')
	for i in range(0,len(pages)/2):
		home.write('<tr><td><a href="'+pages[i]+'">'+pages[i][6:12]+'</a></td><td><a href="'+pages[len(pages)/2 + i]+'">'+pages[len(pages)/2 + i][6:12]+'</a></td></tr>\n') 

	home.write('</table>\n</div>\n</body>\n</html>')
	return

if __name__ =='__main__':
	print('making 1.5-m page for '+sys.argv[1])
	createHTML(str(sys.argv[1]), 1.5)
	print('making 1.3-m page for '+sys.argv[1])
	createHTML(str(sys.argv[1]), 1.3)
	makeHome()
