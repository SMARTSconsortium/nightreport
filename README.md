nightreport
===========

programs for generating the monthly night report digest from the SMARTS 1.3 and 1.5 meter observer end of night forms

night_report2.py and nr_charts.py are the top level are the codes which are recent! Use them!

Everything else is depricated, but is there just in case it becomes usefull to look at.

There is another version of nr_charts.py in the ParseFomrs directory. dont use that. its depricated.
Its from before I started using version control on this project

==========

to use these programs on the yale astronomy department webserver, pegasus, do the following

1) ssh as yourself to pegasus
	$ ssh user@pegasus.astro.yale.edu

2) swap user to yalo. You will be prompted for a password
	$ su yalo

3) change directory to the nightreport directory
	> cd /var/www/html/smarts/nightreport

4) use anaconda distribution of python to run night report script, and provide the telescope and start date. eg
	> /opt/anaconda/bin/python night_report2.py 150101 1.3
will run the night report program from jan 01 - jan 31 2015 using data from the 1.3m response sheet. the end date for the month is computed in the program. for example, it knows january has 31 days and feb has 28.

this will create a few files, an html page of the form 1.3-m-yymmddreport.html or 1.5-m-yymmddreport.html-depending on the telescope-and several png files that visualize the data from the form

the user needs to update the html page index.html so the new month's html page is given as a link under the monthly summaires section. 
it would be cool if someone added a feature here so the index.html page updates by itself.

Suggested Improvements
====================

this program looks at all the 1.3m observation logs it can find for whatever month it is reducing so it can tally up the ammount of time used by program. andicam has problems where it doesnt write out header info for targets sometimes. this will cause the entire program to crash

you could probably clean this all up by usings panda data frames instead of astropy tables. but that will take a lot of rewritting

if you are super cool, it would be neat if the program could give warnings about immenent failurs given past night report data. ie if the dewar is being refilled constantly, it may mean it needs its vacuum restored

