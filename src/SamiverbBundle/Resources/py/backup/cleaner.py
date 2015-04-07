import os
import urllib, urllib2
import xml.etree.ElementTree as ET

def checkverbs(vlist):
	fakeverbs = []
	var = 0
	for verb in vlist:
		# Perhaps the verb already checked?
		tree = ET.parse('verb/' + verb + '.xml')
		root = tree.getroot()
		# Avoid KeyError
		try:
			checkval = root.attrib['check']
		except KeyError:
			checkval = 'notset'
		if checkval == 'valid':
			continue
		# Check the verb
		url = 'http://gtweb.uit.no/cgi-bin/smi/smi.cgi?text='+verb+'&pos=Any&mode=minimal&action=paradigm&charset=utf-8&lang=sme&plang=sme'
		checktext = '<font color="maroon">' + verb + '</font>'
		res = urllib2.urlopen(url)
		data = res.read()
		if checktext not in data:
			fakeverbs.append(verb)
		else:
			root.set('check', 'valid')
			tree.write('verb/' + verb + '.xml')
		if var == 3:
			break
		var += 1
	return fakeverbs

def rmverbs(vlist):
	for verb in vlist:
		os.remove('verb/' + verb + '.xml')

def getverbs(rootdir):
	verbs = []
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			verbs.append(os.path.splitext(file)[0])	
	return verbs

if __name__ == "__main__":
	# Iterate through dir and place all verbs in a list
	verbs = getverbs('verb')
	# Check every verb on integrity
	fakeverbs = checkverbs(verbs)
	if len(fakeverbs) > 0:
		# Remove fake verbs from dir
		rmverbs(fakeverbs)
		# Print receipt
		print 'Disse verbene er fjernet: '+ ", ".join(str(x) for x in fakeverbs) +'.'
	else:
		print -1