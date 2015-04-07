from os import walk
from jsonwritesamiverb import *
import urllib, urllib2
import xml.etree.ElementTree as ET

verbs = []
for (dirpath, dirnames, filenames) in walk("bundles/samiverb/xml"):
    for f in filenames:
      if f[-4:] == '.xml':
        verbs.append(f[:-4])
    break

l = len(verbs)
for i in range(0, l):
  v = verbs[i]
  print str(i + 1) + '/' + str(l) + ' : Transferring ' + v + '.xml to ' + v + '.json'
  # Perhaps the verb already checked?
  tree = ET.parse('bundles/samiverb/xml/' + v + '.xml')
  root = tree.getroot()
  # Avoid KeyError
  try:
    checkval = root.attrib['check']
  except KeyError:
    checkval = None
  if checkval == 'valid':
    JSON_WriteSamiVerb(v).MakeVerb(valid = True)
  else:
    JSON_WriteSamiVerb(v).MakeVerb()