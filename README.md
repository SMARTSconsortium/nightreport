nightreport
===========

programs for generating the monthly night report digest from the SMARTS 1.3 and 1.5 meter observer end of night forms

night_report2.py and nr_charts.py are the top level are the codes which are recent! Use them!

Everything else is depricated, but is there just in case it becomes usefull to look at.

There is another version of nr_charts.py in the ParseFomrs directory. dont use that. its depricated.
Its from before I started using version control on this project

Instructions
==========

to use these programs on the yale astronomy department webserver, pegasus, do the following

1) ssh as yourself to pegasus
```shell
$ ssh user@pegasus.astro.yale.edu
```

2) swap user to yalo. You will be prompted for a password
```shell
su yalo
```

3) change directory to the nightreport directory
```shell
cd /var/www/html/smarts/nightreport
```

4) use anaconda distribution of python to run night report script, and provide the start date. eg
```shell
/opt/anaconda/bin/python night_report2.py 150101
```
will run the night report program from jan 01 - jan 31 2015. the end date for the month is computed in the program. for example, it knows january has 31 days and feb has 28.

this will create a few files, an html page of the form 1.3-m-yymmddreport.html *and* 1.5-m-yymmddreport.html, along with png files that contain visualizations in the images/ directory

finally, the program recreates the homepage, re-writing the table at the bottom providing links to all the night report pages it can find.

Making Specific Pages Individualy
================================
If you want to recreate a particular page for one telescope with out re-writing the home page or anything like that, follow the instructions below

1) navigate to /var/www/htm/smarts/nightreport as yalo on pegasus. (see above for greater detail)

2) start up an anaconda python instance by typing the following at your prompt
```shell
/opt/anaconda/bin/python
```

3) at your python prompt, import the night_report2.py module
```python
import night_report2
```

4) use the createHTML function in night_report2, providing the start date and telescope you are interested in. for example
```python
night_report2.createHTML(150301, 1.5)
```
will create 1.5-m-150301report.html

Suggested Improvements/Know Problems
====================
andicam has problems where it doesnt write out header info for targets sometimes, or writes incorrect information. This is particularly a problem for the JD column in the andicam logs. occasionally the JD of an observation will be written as 000.00, or will be an order of magnitude too small. The tallyascii function looks at the JD's of observations to determine for how long the telescope pointed at a target. Bad JD values can lead to nonsensicle negative observation times for projects. See YALE-08A-0001 for 1.3-m-150601report.html under the Science Observation Break Down section for an example, it has -53075000 hours of observing. 

if you are super cool, it would be neat if the program could give warnings about immenent failurs given past night report data. ie if the dewar is being refilled constantly, it may mean it needs its vacuum restored

Supporting programs
================
www.astro.yale.edu/smarts/nightreport/ has a nice outline of all the forms and response sheets for the report forms.
These are owned by the user smartscas@gmail.com. The response forms have googlescripts which regulate when smartscas emails the submitted night report. 

To look at the google scripts, first open up the response sheet, go to tools > script editor. They should have a trigger set such that the codes are executed when the form is submitted

