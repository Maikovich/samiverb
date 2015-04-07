import sys, os
import json, urllib2

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def checkVerbs(verbList, rootdir):
	fakeverbs = []
	for verb in verbList:
		with open(rootdir + '/' + verb + '.json', 'r') as f:
			checkval = json.load(f)['check']
		if checkval == 1:
			continue
		# Check the verb
		print 'Checking ' + verb
		url = 'http://gtweb.uit.no/cgi-bin/smi/smi.cgi?text='+verb+'&pos=Any&mode=minimal&action=paradigm&charset=utf-8&lang=sme&plang=sme'
		checktext = '<font color="white">' + verb + '</font>'
		res = urllib2.urlopen(url)
		data = res.read()
		if checktext not in data:
			print verb + ' is a fake verb! Deleting...'
			fakeverbs.append(verb)
		else:
			print verb + ' is a real verb! Adding...'
			# Open the json file and read
			with open(rootdir + '/' + verb + '.json', 'r') as f:
				verbObj = json.load(f, object_hook = _decode_dict)
			# Check the verb
			verbObj['check'] = 1
			# Write new json object to file
			with open(rootdir + '/' + verb + '.json', 'w') as f:
				json.dump(verbObj, f, sort_keys = True, indent = 4, ensure_ascii = False)

	return fakeverbs

def removeVerbs(verbList, rootdir):
	for verb in verbList:
		os.remove(rootdir + '/' + verb + '.json')

def getVerbs(rootdir):
	verbs = []
	for subdir, dirs, files in os.walk(rootdir):
		for f in files:
			verbs.append(os.path.splitext(f)[0])	
	return verbs

def addValueVerbs(verbList, rootdir):
  for verb in verbList:
    # Open the json file and read
    with open(rootdir + '/' + verb + '.json', 'r') as f:
      verbObj = json.load(f, object_hook = _decode_dict)
    # Check the verb
    verbObj['value'] = verbObj['name'].decode('utf-8').title().encode('utf-8')
    print verbObj['value']
    # Write new json object to file
    with open(rootdir + '/' + verb + '.json', 'w') as f:
      json.dump(verbObj, f, sort_keys = True, indent = 4, ensure_ascii = False)

# if __name__ == "__main__":
# 	# Iterate through dir and place all verbs in a list
# 	verbs = getVerbs('bundles/samiverb/json')
# 	# Check every verb on integrity
# 	fakeverbs = checkVerbs(verbs, 'bundles/samiverb/json')
# 	print '===== Result ====='
# 	if len(fakeverbs) > 0:
# 		# Remove fake verbs from dir
# 		removeVerbs(fakeverbs, 'bundles/samiverb/json')
# 		# Print receipt
# 		print ", ".join(str(x) for x in fakeverbs)
# 	else:
# 		print ""

# if __name__ == '__main__':
#   # Iterate through dir and place all verbs in a list
#   verbs = getVerbs('bundles/samiverb/json')
#   addValueVerbs(verbs, 'bundles/samiverb/json')