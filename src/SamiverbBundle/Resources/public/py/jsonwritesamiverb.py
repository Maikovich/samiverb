#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Mike Voets, 2014, mike@samiverb.com

import sys, os
import json

from samisyntaxlib import *
from paradigm_generator import *

idxNum 	 		= 0
idxName 	 	= 1
idxVal 	 		= 2
idxOption 	= 3

class JSON_WriteSamiVerb(SamiVerb):
	def __init__(self, verb):
		SamiVerb.__init__(self, verb)
		self.verbFilename = "bundles/samiverb/json/" + self.original + ".json";

		self.paradigmTypeList = [
			[PRESENT, 'present', 'Present', NULL],
			[NEG_PRES, 'neg-present', 'Neg. Present', NULL],
			[PRETERITE, 'preterite', 'Preterite', NULL],
			[NEG_PRET, 'neg-preterite', 'Neg. Preterite', NULL],
			[PERFECT, 'pres-perfect', 'Present Perfect', PRES],
			[PERFECT, 'past-perfect', 'Past Perfect', PAST],
			[ACTIO_ESSIVE, 'pres-actioessive', 'Present Actio Essive', PRES],
			[ACTIO_ESSIVE, 'past-actioessive', 'Past Actio Essive', PAST],
			[CONDITIONAL, 'conditional', 'Conditional', NULL],
			[CONDITIONAL, 'neg-conditional', 'Neg. Conditional', NEG],
			[POTENTIAL, 'potential', 'Potential', NULL],
			[POTENTIAL, 'neg-potential', 'Neg. Potential', NEG],
			[IMPERATIVE, 'imperative', 'Imperative', NULL],
			[NEG_IMP, 'neg-imperative', 'Neg. Imperative', NULL]
		]
	
	def MakeVerb(self):
		""" Make JSON file for a verb """
		# Prepare object
		verbObj = {}
		verbObj['tenses'] = []
		# Initialize it
		verbObj['name'] = self.verb
		verbObj['value'] = self.verb.decode('utf-8').title().encode('utf-8')
		verbObj['check'] = 0
		verbObj['valid'] = 0
		# Start filling with paradigms

		for pType in self.paradigmTypeList:
			# Create tense object
			tense = {}
			tense['name'] = pType[idxName]
			tense['value'] = pType[idxVal]

			# Get paradigms
			num = pType[idxNum]
			opt = pType[idxOption]

			if num == PRESENT or num == PRETERITE or (num == CONDITIONAL and opt != NEG) or (num == POTENTIAL and opt != NEG) or num == IMPERATIVE:
				# Get paradigm list
				tmpList = self.paradigmGet(num)
				# Put it in the object
				tense['paradigms'] = tmpList

			elif num == NEG_PRES or num == NEG_PRET:
				# Get paradigm
				paradigm = self.paradigmGet(num)
				# Put it in the object together with negative parts
				tmp = []
				for p in self.partNeg:
					tmp.append(p + ' ' + paradigm)
				tense['paradigms'] = tmp
	
			elif num == NEG_IMP:
				# Get paradigm
				paradigm = self.paradigmGet(num)
				# Put it in the obect together with negative parts
				tmp = []
				for p in self.partImpNeg:
					tmp.append(p + ' ' + paradigm)
				tense['paradigms'] = tmp

			elif num == PERFECT or num == ACTIO_ESSIVE:
				# Get paradigm
				paradigm = self.paradigmGet(num)
				if opt == PRES:
					sfixLeat = self.sfixLeatPres
				else:
					sfixLeat = self.sfixLeatPast
				leat = 'le'
				# Put paradigm in object
				tmp = []
				for p in sfixLeat:
					tmp.append(leat + p + ' ' + paradigm) 
				tense['paradigms'] = tmp

			elif num == CONDITIONAL and opt == NEG:
				tmp = []
				for p in self.partNeg:
					tmp.append(p + ' ' + self.stamCond + 'e')
				tense['paradigms'] = tmp

			elif num == POTENTIAL and opt == NEG:
				tmp = []
				for p in self.partNeg:
					tmp.append(p + ' ' + self.stamPots)
				tense['paradigms'] = tmp

			verbObj['tenses'].append(tense)

		try:
			# Write the object in JSON format to file
			with open(self.verbFilename, 'w') as f:
				json.dump(verbObj, f, sort_keys = True, indent = 2, ensure_ascii = False)
			return 1
		except:
			# If exception was caught, remove the file
			os.remove(self.verbFilename)
			return 0



def main():
	if len(sys.argv) != 2:
		print 0
	print JSON_WriteSamiVerb(sys.argv[1]).MakeVerb()

if __name__ == '__main__':
	main()