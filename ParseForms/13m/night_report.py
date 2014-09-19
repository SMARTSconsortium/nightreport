#!/Users/ih64/anaconda/bin/python
import nr_charts
import accounting
import os
import fnmatch
#set up the class so that we can read the response form and assign atributes to each night
class nightReport:
	def __init__(self,submit,bon,obs,obsast,wthr,bsee,msee,esee,hrobs,hrtoo,hreng,hrsys,hrwthr,dis,comments,sysfail,cond,ln2):
		self.submit=submit
		self.bon=bon
		self.obs=obs
		self.obsast=obsast
		self.wthr=wthr
		self.bsee=bsee
		self.msee=msee
		self.esee=esee
		self.hrobs=hrobs
		self.hrtoo=hrtoo
		self.hreng=hreng
		self.hrsys=hrsys
		self.hrwthr=hrwthr
		self.dis=dis
		self.comments=comments
		self.sysfail=sysfail
		self.cond=cond
		self.ln2=ln2

#this will handle multiple responses given for weather and store them in a list
	def wthrExp(self):
		return self.wthr.split(', ')

#this will handle multiple responses given for disposition and store them in a list 
	def disExp(self):
		return self.dis.split(', ')

#this will handle multiple responses given for system failures and store them in a list
	def sysfailExp(self):
		return self.sysfail.split(', ')

#this list, nights, will hold each class. each class will be its own element
nights=[]

inputfile=open('13mResponses.tsv')

for line in inputfile:
	s=line.split('\t') #we are expecting the response form to be tab delimited
	nights.append(nightReport(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8],s[9],s[10],s[11],s[12],s[13],s[14],s[15],s[16],s[17]))

inputfile.close()

#find how many nights there were. subtract one because the column headings are also included
totnights=len(nights)-1

#find sums of hours observing etc. dont bother with the 0th index, it is the column headings
obstothr=sum([float(nights[i].hrobs) for i in range(1,totnights + 1)])
tootothr=sum([float(nights[i].hrtoo) for i in range(1,totnights + 1)])
engtothr=sum([float(nights[i].hreng) for i in range(1,totnights + 1)])
systothr=sum([float(nights[i].hrsys) for i in range(1,totnights + 1)])
wthrtothr=sum([float(nights[i].hrwthr) for i in range(1,totnights + 1)])


#find the different weather types experienced, and count the instances of each
#use wthrExp() defined above to split up instances of multiple weather types experienced
#wthrexp will be a list which contains a list for each night whcih contains the weather types experienced
wthrexp=[nights[i].wthrExp() for i in range(1,len(nights))]

#we just want one list with the weather responses given, so flatten out wthrexp
w=[]
for i in range(0,len(wthrexp)):
	for j in range(0,len(wthrexp[i])):
		w.append(wthrexp[i][j])

#wset contains the unique values of w
wset=set(w)
wsetcount=[(x, w.count(x)) for x in wset]
wsetcountdict=dict(wsetcount)	#wsetcountdict is a dictionary whose keys are weather and values are # reported

#find the different system failures experienced, and count the instances of each
#use sysfailExp() defined above to split up instances of failure types experienced
#sysfailexp will be a list which contains a list for each night whcih contains the weather types experienced
sfexp=[nights[i].sysfailExp() for i in range(1,len(nights))]

#we just want one list with the weather responses given, so flatten out wthrexp
sf=[]
for i in range(0,len(sfexp)):
	for j in range(0,len(sfexp[i])):
		sf.append(sfexp[i][j])

#sfset contains the unique values of sf
sfset=set(sf)
sfsetcount=[(x, sf.count(x)) for x in sfset]
sfsetcountdict=dict(sfsetcount)	#sfsetcountdict is a dictionary whose keys are weather and values are # reported

#############
disexp=[nights[i].disExp() for i in range(1,len(nights))]

#we just want one list with the weather responses given, so flatten out wthrexp
dis=[]
for i in range(0,len(disexp)):
	for j in range(0,len(disexp[i])):
		dis.append(disexp[i][j])

#sfset contains the unique values of sf
disset=set(dis)
dissetcount=[(x, dis.count(x)) for x in disset]
dissetcountdict=dict(dissetcount)	#sfsetcountdict is a dictionary whose keys are weather and values are # reported

#############

#count the conditions reported
cond=[i.cond for i in nights]
condset=set(cond)
condsetcount=[(x, cond.count(x)) for x in condset]
condsetcountdict=dict(condsetcount)

hours = dict(observing=obstothr, ToO=tootothr, engineering=engtothr, sys_failure=systothr, weather=wthrtothr)

#gather up the seeing values in a list
bseelist=[eval(i.bsee) for i in nights if (i.bsee !='Beginning of night seeing' and i.bsee !='n/a')]
mseelist=[eval(i.msee) for i in nights if (i.msee !='Middle of night seeing' and i.msee !='n/a')]
eseelist=[eval(i.esee) for i in nights if (i.esee !='End of night seeing' and i.esee !='n/a')]

#work on the observer logs to tally up observation time on each project
os.system('rm *Pickle')
accounting.projectjar()
logs=fnmatch.filter(os.listdir('.'),'*.log')
for i in logs:
	projdict=accounting.tally(i)


#make charts
nr_charts.dispositionchart(dissetcountdict)
nr_charts.condpie(condsetcountdict)
nr_charts.timepie(hours)
nr_charts.failurechart(sfsetcountdict)
nr_charts.weatherchart(wsetcountdict)
nr_charts.breakdownpie(projdict)
#print our results
print '-------------------------'
print 'weather types experienced'
print '-------------------------'
for key in wsetcountdict:
	print key, wsetcountdict[key]
print '---------------------------'
print 'system failures experienced'
print '---------------------------'
for key in sfsetcountdict:
	if key!='':
		print key, sfsetcountdict[key]

print '-------------------------'
print 'avg seeing beginning of night : '+ str(sum(bseelist)/len(bseelist))
print 'avg seeing middle of night : '+ str(sum(mseelist)/len(mseelist))
print 'avg seeing end of night : '+ str(sum(eseelist)/len(eseelist))
print 'total nights : ' + str(totnights)
print 'total hours spent observing : ' + str(obstothr)
print 'total hours spent on ToO    : ' + str(tootothr)
print 'total hours lost to engineering : ' + str(engtothr)
print 'total hours lost to system failure : '+ str(systothr)
print 'total hours lost to weather : ' + str(wthrtothr)

f=open("nightreport.html",'w')
f.write("<html>")
f.write("<body>")
f.write("<h1>SMARTS 1.3-m Night Report Summary</h1>")
f.write("<hr><h3>Total Nights</h3>")
f.write("<p>"+str(len(nights)-1)+"</p>")
f.write("<hr><h3>Observing Conditions</h3>")
f.write("<img src='conditions.png' width='500px', align='left'>")
f.write('<p>'+'avg seeing beginning of night : '+ str(sum(bseelist)/len(bseelist))+'</p>')
f.write('<p>'+'avg seeing middle of night : '+ str(sum(mseelist)/len(mseelist))+'</p>')
f.write('<p>'+'avg seeing end of night : '+ str(sum(eseelist)/len(eseelist))+'</p>')
f.write('<p>Photometric nights : '+str(condsetcountdict['Photometric'])+'</p>')
f.write('<p>Nonhotometric nights : '+str(condsetcountdict['Nonphotometric'])+'</p>')
f.write("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>")
f.write("<hr><h3>Weather Conditions</h3>")
f.write("<img src='weather.png' width='500px' align='left'>")
f.write("<table>")
for key in wsetcountdict:
	f.write("<tr><td>"+str(key)+"</td><td>"+str(wsetcountdict[key])+"</td></tr>")
f.write("</table>")
f.write("<br><br><br><br><br><br><br><br><br><br>")
f.write("<hr><h3>Night Disposition</h3>")
f.write("<img src='disposition.png' width='500px' align='left'>")
f.write("<table>")
f.write("<tr><td>minor technical problems</td><td>"+str(dissetcountdict['minor technical problems'])+"</td></tr>")
f.write("<tr><td>major technical problems</td><td>"+str(dissetcountdict['major technical problems'])+"</td></tr>")
f.write("<tr><td>everything worked well</td><td>"+str(dissetcountdict['everything worked well'])+"</td></tr>")
f.write("</table>")
f.write("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>")
f.write("<hr><h3>System Failures</h3>")
f.write("<img src='systemfail.png' width='500px' align='left'>")
f.write("<table>")
for key in sfsetcountdict:
	f.write("<tr><td>"+str(key)+"</td><td>"+str(sfsetcountdict[key])+"</td></tr>")
f.write("</table>")
f.write("<br><br><br><br><br><br><br><br><br><br><br><br><br><br>")
f.write("<hr><h3>Time Loss & Observing</h3>")
f.write("<img src='hours.png' width='500px' align='left'>")
f.write("<table>")
for key in hours:
	f.write("<tr><td>"+str(key)+"</td><td>"+str(hours[key])+"</td></tr>")
f.write("</table>")
f.write("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>")
f.write("<hr><h3>Science Observation Break Down</h3>")
f.write("<img src='breakdown.png' width='500px' align='left'>")
f.write("<table>")
for key in projdict:
	if key!='ALL' and key !='STANDARD' and key !='STANDARDFIELD' and key !='Project':
		f.write("<tr><td>"+key+"</td><td>"+str(projdict[key]['time']/3600)[0:5]+"</td></tr>")
f.write("</table>")
f.write("</body>")
f.write("</html>")
f.close()
