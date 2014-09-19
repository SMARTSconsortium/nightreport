#!/Users/ih64/anaconda/bin/python

#this module holds a bunch of functions to help make web-broswser friendly interactive plots

#import some thing's we will need
import numpy as np
import matplotlib.pyplot as plt
import mpld3
from bokeh.plotting import *
'''
These functions will handle data
getting data from file, cleaning it up, computing color excesses
'''
#load up the photometry from all wavelengths into numpy arrays
#input: the blazar's name-AS A STRING
#output: A list of 5 arrays. Each holds photometry of a band
#use the blazar.tab file, this is the public one
#and doesnt have INV data
def getdata(tabfile):
	Bdat=np.loadtxt(tabfile, usecols=(1,2,3), unpack=True)
	Vdat=np.loadtxt(tabfile, usecols=(4,5,6), unpack=True)
	Rdat=np.loadtxt(tabfile, usecols=(7,8,9), unpack=True)
	Jdat=np.loadtxt(tabfile, usecols=(10,11,12), unpack=True)
	Kdat=np.loadtxt(tabfile, usecols=(13,14,15), unpack=True)
	return [Bdat, Vdat, Rdat, Jdat, Kdat]

#remove the 999's from the data photometry table
#input: filterdat, a numpy array of shape (3,) (obs date, mag, iraf error)
#output: cleandat, a numpy array of shape (3,) (obs date, mag, iraf error)
#with all 999 entries removed
def cleandata(filterdat):
	truedatai=np.where(filterdat[0] != 999.0)
	cleandat=[filterdat[0][truedatai], filterdat[1][truedatai], filterdat[2][truedatai]]
	return cleandat

#nearest neighbor search algorithm
#vectorized implementation
#use to compare data for two filters to find closest observation dates
#input: two numpy arrays (fltblue, fltred) which each have shape (3,)
#(obs time, mag, iraf error)
#output: list of numpy arrays (difference in obs time, obstime fltb, fltbmag, fltrmag )
def colexces(fltblue,fltred):
	#its easier to use modified jd for the search
	fbdmin=fltblue[0]-2450000
	frdmin=fltred[0]-2450000
	#make the 2 above arrays into column vectors
	#we need to do this to perform matrix multiplication
	fbdmin=np.reshape(fbdmin,(len(fbdmin),1))
	frdmin=np.reshape(frdmin,(len(frdmin),1))
	#make some square arrays for each filter
	bb=np.dot(fbdmin, fbdmin.T)
	rr=np.dot(frdmin, frdmin.T)
	#to make a color magnitude diagram, we need one color value
	#for every value in the redder filter
	#make the cross term matrix
	rb=np.dot(frdmin,fbdmin.T)
	#D is a matrix that holds (bobsdate - robsdate)**2 for every pair of dates
	#with b columns and r rows
	D=bb.diagonal()[np.newaxis] - 2*rb + rr.diagonal()[:,np.newaxis]
	#sort along the second axis to find smallest values
	#match these to the red ones, and compute their difference
	datedif=fltblue[0][np.argsort(D,axis=1)[:,0]]-fltred[0]
	A=np.vstack((datedif,fltred[0],fltblue[1][np.argsort(D,axis=1)[:,0]],fltred[1]))
	#finally, filter it so that only observations taken with in .003 jd time are listed
	closeenough=np.where(np.fabs(A[0]) < .003)
	B=np.vstack((A[0][closeenough],A[1][closeenough],A[2][closeenough],A[3][closeenough]))
	return B

'''
These functions will make bokeh plots
'''

#make a light curves of an object with filters
#input: tabfile-the string of the table of the target, eg "3C27.tab"
#input : filters-a python list with filters to get light curves of, eg ['B'.'V','R']
#output : currently a lightcurve.html file. later, an html snippet to find the .embed.js
def lightcurveBokeh(tabfile, filters):
	numplots=len(filters)
	coldict=dict(B=0, V=1, R=2, J=3, K=4)
	photdata=getdata(tabfile)
	photdatatrim=[photdata[coldict[j]] for j in filters]
	cp=[cleandata(k) for k in photdatatrim]
	output_file("lightcurve.html", title="Light curve example")
	pltlist=[scatter(cp[coldict[i]][0],cp[coldict[i]][1]*(-1),tools="pan,wheel_zoom,box_zoom,reset,resize,previewsave", legend=i) for i in filters]
	gridplot([[i] for i in pltlist])
	show()
	return	

#make a color magnitude diagram using all the data taken
#in the lifetime of smarts
#input: tabfile-the string of the table of the target, eg "3C27.tab"
#input: bfilter-string for the bluer filter, eg "B"
#input: rfilter-string for the redder filter, eg "J"
#output : currently cmd.html file with a bokeh plot. later, an html snippet to find the .embed.js
def colormagBokeh(tabfile, bfilter, rfilter):
	from bokeh.objects import HoverTool
	from collections import OrderedDict
	#this dictionary will help us translate the filter input
	#to the return of getdata()
	coldict=dict(B=0, V=1, R=2, J=3, K=4)
	photdata=getdata(tabfile)
	cp=[cleandata(i) for i in photdata]
	colorarray=colexces(cp[coldict[bfilter]], cp[coldict[rfilter]])
	labels=[str(i) for i in colorarray[1]]
	x=colorarray[3]
	y=colorarray[2]-colorarray[3]
	source=ColumnDataSource(
		data=dict(
			x=x,
			y=y,
			labels=labels))
	output_file("cmd.html", title="Color Magnitude")
	hold()
	plot=scatter(x,y, size=7, source=source,tools="pan,wheel_zoom,box_zoom,reset,resize,hover,previewsave")
	hover = [t for t in curplot().tools if isinstance(t, HoverTool)][0]
	hover.tooltips = OrderedDict([("date", "@labels")])
	xaxis().axis_label=rfilter
	yaxis().axis_label=bfilter+' - '+rfilter
	snip=plot.create_html_snippet(static_path='/Users/ih64/anaconda/lib/python2.7/site-packages/bokeh/server/static/')
	return snip

'''
These functions make mpld3 plots
'''
def lightcurveMPLD3(tabfile, filters):
	import matplotlib.pyplot as plt
	import mpld3
	fig = plt.figure()
	numplots=len(filters)
	coldict=dict(B=0, V=1, R=2, J=3, K=4)
	photdata=getdata(tabfile)
	photdatatrim=[photdata[coldict[j]] for j in filters]
	cp=[cleandata(k) for k in photdatatrim]
	for i in range(0,len(filters)):
		a=fig.add_subplot(numplots,1,i+1)
		a.scatter(cp[i][0],cp[i][1])
		a.axes.invert_yaxis()
		a.axes.set_xlabel('Julian Date')
		a.axes.set_ylabel(filters[i]+" magnitude")
	mpld3.plugins.connect(fig, mpld3.plugins.Zoom(button=False, enabled=True))
	mpld3.save_html(fig, "mpld3lc.html")
	return

def colormagMPLD3(tabfile, bfilter, rfilter):
	import matplotlib.pyplot as plt
	import mpld3
	coldict=dict(B=0, V=1, R=2, J=3, K=4)
	photdata=getdata(tabfile)
	cp=[cleandata(i) for i in photdata]
	colorarray=colexces(cp[coldict[bfilter]], cp[coldict[rfilter]])
	fig, ax = plt.subplots()
	scatter=ax.scatter(colorarray[3],colorarray[2]-colorarray[3],c=colorarray[1], s=40)
	ax.axes.invert_xaxis()
	ax.axes.set_xlabel(rfilter)
	ax.axes.set_ylabel(bfilter+" - "+rfilter)
	labels=[str(colorarray[1][i]) for i in range(0,len(colorarray[1]))]
	tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
	mpld3.plugins.connect(fig, tooltip)
	mpld3.save_html(fig, "mpld3color.html")
	return
