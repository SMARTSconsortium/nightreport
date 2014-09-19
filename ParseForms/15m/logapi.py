#!/opt/anaconda/bin/python
from urllib2 import Request, urlopen, URLError
def logapi(year,month,day):
	calendar={"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04", "May":"05", "Jun":"06",
		"Jul":"07", "Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"}

	urlroot="http://www.astronomy.ohio-state.edu/ANDICAM/ObsLogs/"
	
	request=urlroot+year+"/"+month+"/"+str(year)+calendar[month]+day+".log"

	try:
		response=urlopen(request)
		log=response.readlines()
		return log
	except URLError, e:
		print request+" not found"
		return 0
