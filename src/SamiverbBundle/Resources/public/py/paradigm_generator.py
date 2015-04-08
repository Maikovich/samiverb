#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Mike Voets, 2014, mike@samiverb.com

import sys, os
from samisyntaxlib import *

PRESENT 		  = 1
PRETERITE 	  = 2
CONDITIONAL 	=	3
POTENTIAL   	= 4
NEG_PRES      = 5
NEG_PRET	  	= 6
PERFECT    		= 7
ACTIO_ESSIVE  = 8
IMPERATIVE    = 9
NEG_IMP		  	= 10
NULL   			  = 0
PRES 		 	 		= 1
PAST 	 	  		= 2
NEG 					= 3

class SamiVerb(SamiSfixAndSyntaxLibrary):
	def __init__(self, verb):
		SamiSfixAndSyntaxLibrary.__init__(self)
		self.verb = self.original = verb.lower()

	def resetVerb(self):
		""" Resets verb to original state """
		self.verb = self.original

	def popLetter(self):
		""" Pops one letter from the end of the verb, saves the verb and returns the pop result """
		# Little hack to find the length of an utf-8 special char in order to pop it
		tmp = len(list(list(self.verb.decode('utf-8'))[-1].encode('utf-8')))
		self.verb, pop = self.verb[:-tmp], self.verb[-tmp:]
		return pop

	def verifyVerb(self):
		""" Verify the verb's validness """
		# Last char must be a "t"
		if self.popLetter() == 't':
			syllableCnt = self.syllableCount(self.verb)
			if syllableCnt > 0:
				# Second last char must be "a, i, u, á, e, o" and correspons with the right syllableable amount
				lastChar = self.lastCharGet(self.verb)
				if syllableCnt % 2 == 0:
					if lastChar == 'a' or lastChar == 'i' or lastChar == 'u':
						return 1
					if lastChar == 'á' or lastChar == 'e' or lastChar == 'o':
						return 3
				else:
					if lastChar == 'i' or lastChar == "a":
						return 2
		return 0

	def _findStrongStage(self):
		""" Find the strong stage of the verb """
		# Initialize the string
		strong = ""
		n = 0
		# Start analyzing the verb for the stage
		while len(self.verb) > 0:
			# Pop the letters until found stage + 1
			strong = self.popLetter() + strong
			if strong in self.stageList:
				n = 1
			if n == 1 and strong not in self.stageList:
				# Concatenate the last popped letter to the verb
				tmp = len(list(list(strong.decode('utf-8'))[0].encode('utf-8')))
				strong, res = strong[tmp:], strong[:tmp]
				self.verb = self.verb + res
				break
		return strong
		
	def _fromStrongToWeakStage(self, strongStageForm):
		""" Returns weak stage form for inputted strong stage form """
		if self.original in self.expectionsList:
			return strongStageForm
		try:
			return self.stageList[strongStageForm]
		except KeyError:
			return None	
	
	def _fromStrongToExtraStrongStage(self, strongStageForm):
		""" Returns extra strong form for inputted strong stage form """
		for extraStr, strong in self.stageList.iteritems():
			if strongStageForm == strong:
				return extraStr
		return strongStageForm
		
	def __sfixListPresGet(self, syllableCnt):
		""" Returns appropriate present tense suffix list from library """
		if syllableCnt == 1:
			if self.verb[-1] == 'a':
				self.popLetter()
				return self.sfixAVerbPres
			if self.verb[-1] == 'i':
				self.popLetter()
				return self.sfixIVerbPres
			if self.verb[-1] == 'u':
				self.popLetter()
				return self.sfixUVerbPres
		if syllableCnt == 2:
			if self.verb[-1] == 'a':
				self.popLetter()
				return self.sfixLeatPres
			self.popLetter()
			return self.sfixNegVerbPres
		if syllableCnt == 3:
			return self.sfixContrVerbPres

	def __sfixListPastGet(self, syllableCnt):
		""" Returns appropriate past tense suffix list from library """
		if syllableCnt == 1:
			if self.verb[-1] == 'a':
				self.popLetter()
				return self.sfixAVerbPast
			if self.verb[-1] == 'i':
				self.popLetter()
				return self.sfixIVerbPast
			if self.verb[-1] == 'u':
				self.popLetter()
				return self.sfixUVerbPast
		if syllableCnt == 2:
			if self.verb[-1] == 'a':
				self.popLetter()
				return self.sfixLeatPast
			self.popLetter()
			return self.sfixNegVerbPast
		if syllableCnt == 3:
			return self.sfixContrVerbPast

	def __sfixListCondGet(self, syllableCnt):
		""" Returns appropriate CONDITIONAL suffix list from library """
		if syllableCnt == 1 or syllableCnt == 3:
			return self.sfixNegVerbPast
		if syllableCnt == 2:
			if self.verb[-1] == 'a':
				self.popLetter()
			self.popLetter()
			return self.sfixIVerbPast

	def __sfixListPotsGet(self, syllableCnt):
		""" Returns appropriate POTENTIAL suffix list from library """
		if syllableCnt == 1 or syllableCnt == 3:
			return self.sfixNegVerbPres
		if syllableCnt == 2:
			return self.sfixAVerbPres
	
	def __sfixListImpGet(self, syllableCnt):
		""" Returns appropriate imperative suffix list from library """
		if syllableCnt == 1:
			return self.sfixRegVerbImp
		if syllableCnt == 2 or syllableCnt == 3:
			return self.sfixOtherVerbImp
		
	def _sfixListGet(self, syllableCnt, tense):
		""" Returns appropriate suffix list from library """
		if tense == PRESENT:
			return self.__sfixListPresGet(syllableCnt)
		if tense == PRETERITE:
			return self.__sfixListPastGet(syllableCnt)
		if tense == CONDITIONAL:
			return self.__sfixListCondGet(syllableCnt)
		if tense == POTENTIAL:
			return self.__sfixListPotsGet(syllableCnt)
		if tense == IMPERATIVE:
			return self.__sfixListImpGet(syllableCnt)

	def _diftonGet(self):
		""" Return the difton """
		# Initialize string
		difton = ""
		while len(self.verb) > 0:
			# Pop vowels and add to string until consonant appears
			tmp = list(self.verb.decode('utf-8'))
			if self._isConsonant(tmp[-1].encode('utf-8')):
				break
			difton = self.popLetter() + difton
		return difton

	def _fromStrongToWeakDifton(self, diftonStrong):
		""" Returns weak form of difton """
		try:
			diftonWeak = self.diftons[diftonStrong]
		except KeyError:
			return diftonStrong
		return diftonWeak

	def _paradigmListPres(self):
		""" Adds all forms of the present tense to a paradigm list """
		# Count syllables to determine verb type
		typeVerb = self.verifyVerb()
		if typeVerb != 0:
			# Initialize paradigm list
			paradigmList = []
			# Get appropriate suffix list
			sfixList = self._sfixListGet(typeVerb, PRESENT)
			
			# typeVerb 1 => "likestavelses", 2 => "ulikestavelsels", 3 => "kontrakt"
			if typeVerb == 1:
				# Fetch all stages and difton changes
				strStage = self._findStrongStage()
				wkStage = self._fromStrongToWeakStage(strStage)
				strDftn = self._diftonGet() 
				wkDftn = self._fromStrongToWeakDifton(strDftn)
				if wkStage == None:
					return -1
				# Add forms to paradigm list
				for i in range(0, len(sfixList)):
					if i == 0 or i == 1:
						paradigmList.append(self.verb + strDftn + wkStage + sfixList[i])
					elif i == 3 or i == 8:
						paradigmList.append(self.verb + wkDftn + strStage + sfixList[i])
					else:
						paradigmList.append(self.verb + strDftn + strStage + sfixList[i])
			
			elif typeVerb == 2:
				for i in range(0, len(sfixList)):
					if i == 6:
						paradigmList.append(self.verb + sfixList[6] + ", -" + self.lastCharGet(self.verb) + sfixList[1])
					else:
						paradigmList.append(self.verb + sfixList[i])
			
			elif typeVerb == 3:
				for i in range(0, len(sfixList)):
					paradigmList.append(self.verb + sfixList[i])
			
			# Reset verb to original state
			self.resetVerb()
			return paradigmList
		# Any errors, return -1
		return -1
			
	def _paradigmListPast(self):
		""" Adds all forms of the past tense to a paradigm list """
		# Count syllables to determine verb type
		typeVerb = self.verifyVerb()
		if typeVerb != 0:
			# Initialize paradigm list
			paradigmList = []
			# Get appropriate suffix list
			sfixList = self._sfixListGet(typeVerb, PRETERITE)
			
			# typeVerb 1 => "likestavelses", 2 => "ulikestavelsels", 3 => "kontrakt"
			if typeVerb == 1:
				# Fetch all stages and difton changes
				strStage = self._findStrongStage()
				wkStage = self._fromStrongToWeakStage(strStage)
				strDftn = self._diftonGet() 
				wkDftn = self._fromStrongToWeakDifton(strDftn)
				if wkStage == None:
					return -1
				# Add forms to paradigm list
				for i in range(0, len(sfixList)):
					if i == 0 or i == 1 or i == 8:
						paradigmList.append(self.verb + wkDftn + strStage + sfixList[i])
					else:
						if sfixList[2] == "ii":
							paradigmList.append(self.verb + wkDftn + wkStage + sfixList[i])
						else:
							paradigmList.append(self.verb + strDftn + wkStage + sfixList[i])
			
			elif typeVerb == 2:
				for i in range(0, len(sfixList)):
					paradigmList.append(self.verb + sfixList[i])
			
			elif typeVerb == 3:
				strLstChar = self.lastCharGet(self.verb)
				wkLstChar = self._fromStrongToWeakSuffixPast(strLstChar)
				for i in range(0, len(sfixList)):
					if i == 0 or i == 1 or i == 8:
						paradigmList.append(self.verb + strLstChar + sfixList[i])
					else:
						paradigmList.append(self.verb + wkLstChar + sfixList[i])
			
			# Reset verb to original state
			self.resetVerb()
			return paradigmList
		# Any errors, return -1
		return -1

	def _paradigmListCond(self):
		""" Adds all forms of the CONDITIONAL to a paradigm list """
		# Count syllables to determine verb type
		typeVerb = self.verifyVerb()
		if typeVerb != 0:
			# Initialize paradigm list
			paradigmList = []
			# Get appropriate suffix list
			sfixList = self._sfixListGet(typeVerb, CONDITIONAL)

			# typeVerb 1 => "likestavelses", 2 => "ulikestavelsels", 3 => "kontrakt"
			if typeVerb == 1:
				# Fetch all stages and difton changes
				xtr = 'š'
				strLstChar = self.lastCharGet(self.verb)
				wkLstChar = self._fromStrongToWeakSuffixKond(strLstChar)
				wkStage = self._fromStrongToWeakStage(self._findStrongStage())
				strDftn = self._diftonGet() 
				wkDftn = self._fromStrongToWeakDifton(strDftn)
				if wkStage == None:
					return -1
				# Add forms to paradigm list
				if strLstChar == 'u':
					self.stamCond = self.verb + wkDftn + wkStage + wkLstChar + xtr
					for i in range(0, len(sfixList)):
						paradigmList.append(self.stamCond + sfixList[i])
				else:
					self.stamCond = self.verb + strDftn + wkStage + wkLstChar + xtr
					for i in range(0, len(sfixList)):
						paradigmList.append(self.stamCond + sfixList[i])

			elif typeVerb == 2:
				xtr = 'ivčč'
				self.stamCond = self.verb + xtr
				for i in range(0, len(sfixList)):
					paradigmList.append(self.stamCond + sfixList[i])
			
			elif typeVerb == 3:
				xtr = 'š'
				self.stamCond = self.verb + xtr
				for i in range(0, len(sfixList)):
					paradigmList.append(self.stamCond + sfixList[i])

			# Reset verb to original state
			self.resetVerb()
			return paradigmList
		# Any errors, return -1
		return -1

	def _paradigmListPots(self):
		""" Adds all forms of the POTENTIAL to a paradigm list """
		# Count syllables to determine verb type
		typeVerb = self.verifyVerb()
		if typeVerb != 0:
			# Initialize paradigm list
			paradigmList = []
			# Get appropriate suffix list
			sfixList = self._sfixListGet(typeVerb, POTENTIAL)
			
			# typeVerb 1 => "likestavelses", 2 => "ulikestavelsels", 3 => "kontrakt"
			if typeVerb == 2:
				xtr = 'e'
				self.popLetter()
				if self.lastCharGet(self.verb) == 'e':
					xtr = 'et'
					self.popLetter()
				# Add every form in paradigm list
				for i in range(0, len(sfixList)):
					if i == 0 or i == 1:
						paradigmList.append(self.verb + 'eačč' + sfixList[i])
					elif i == 2:
						lstChar = self.lastCharGet(self.verb)
						self.stamPots = self.verb + 'eaš, -' + lstChar + 'eš, -' + lstChar + 'eažžá'
						paradigmList.append(self.stamPots)
					elif i == 3:
						paradigmList.append(self.verb + 'ežž' + xtr)
					elif i == 8:
						paradigmList.append(self.verb + 'ežž' + sfixList[8])
					else:
						paradigmList.append(self.verb + 'eažž' + sfixList[i])
			
			if typeVerb == 1:
				wkLstChar = self._fromStrongToWeakSuffixPots(self.lastCharGet(self.verb))
				wkStage = self._fromStrongToWeakStage(self._findStrongStage())
				if wkStage == None:
					return -1
				strDftn = self._diftonGet() 
				wkDftn = self._fromStrongToWeakDifton(strDftn)
				if wkLstChar == 'a':
					wkDftn = strDftn
				for i in range(0, len(sfixList)):
					if i == 2:
						self.stamPots = self.verb + wkDftn + wkStage + wkLstChar + 'š'
						paradigmList.append(self.stamPots)
					elif i == 6:
						paradigmList.append(self.verb + wkDftn + wkStage + wkLstChar + 'ž' + sfixList[6] + ", -" + 'ž' + sfixList[1])
					else:
						paradigmList.append(self.verb + wkDftn + wkStage + wkLstChar + 'ž' + sfixList[i])				
			
			if typeVerb == 3:
				for i in range(0, len(sfixList)):
					if i == 2:
						self.stamPots = self.verb + 'š'
						paradigmList.append(self.stamPots)
					elif i == 6:
						paradigmList.append(self.verb + 'ž' + sfixList[6] + ", -" + 'ž' + sfixList[1])
					else:
						paradigmList.append(self.verb + 'ž' + sfixList[i])	

			# Reset verb to original state
			self.resetVerb()
			return paradigmList
		# Any errors, return -1
		return -1	

	def _paradigmListImp(self):
		""" Returns paradigm list of imperative """
		# Count syllables to determine verb type
		typeVerb = self.verifyVerb()
		if typeVerb != 0:
			# Initialize paradigm list
			paradigmList = []
			# Get appropriate suffix list
			sfixList = self._sfixListGet(typeVerb, IMPERATIVE)
		
			# typeVerb 1 => "likestavelses", 2 => "ulikestavelsels", 3 => "kontrakt"
			if typeVerb == 1:
				strLstChar = self.lastCharGet(self.verb)
				wkLstChar = self._fromStrongToWeakSuffixNeg(strLstChar)
				strStage = self._findStrongStage()
				xtrStrStage = self._fromStrongToExtraStrongStage(strStage)
				wkStage = self._fromStrongToWeakStage(strStage)
				if wkStage == None:
					return -1
				strDftn = self._diftonGet() 
				wkDftn = self._fromStrongToWeakDifton(strDftn)
				# Define paradigm list
				for i in range(0, len(sfixList)):
					if i == 1:
						paradigmList.append(self.verb + strDftn + wkStage + wkLstChar)
					elif i == 4:
						if strLstChar == 'u':
							paradigmList.append(self.verb + strDftn + xtrStrStage + sfixList[i][1])
						else:
							paradigmList.append(self.verb + strDftn + xtrStrStage + sfixList[i][0])
					elif i == 6:
						if strStage == xtrStrStage and wkDftn == strDftn:
							paradigmList.append(self.verb + wkDftn + strStage + sfixList[i])
						else:
							paradigmList.append(self.verb + wkDftn + strStage + sfixList[i] + ", " + self.verb + strDftn + xtrStrStage + sfixList[i])
					elif i == 7:
						if strLstChar == 'a':
							paradigmList.append(self.verb + wkDftn + strStage + sfixList[i][0] + ", " + self.verb + strDftn + xtrStrStage + sfixList[i][1])
						elif strLstChar == 'i':
							if strStage == xtrStrStage and wkDftn == strDftn:
								paradigmList.append(self.verb + wkDftn + strStage + sfixList[i][0])
							else:
								paradigmList.append(self.verb + wkDftn + strStage + sfixList[i][0] + ", " + self.verb + strDftn + xtrStrStage + sfixList[i][0])
						elif strLstChar == 'u':
							if strStage == xtrStrStage and wkDftn == strDftn:
								paradigmList.append(self.verb + wkDftn + strStage + sfixList[i][2])
							else:
								paradigmList.append(self.verb + wkDftn + strStage + sfixList[i][2] + ", " + self.verb + strDftn + xtrStrStage + sfixList[i][2])
					elif i == 3:
						paradigmList.append(self.verb + strDftn + xtrStrStage + sfixList[i])
					else:
						paradigmList.append(self.verb + wkDftn + strStage + sfixList[i])
			
			elif typeVerb == 2:
				# Remove i
				self.popLetter()
				if self.lastCharGet(self.verb) == 'e':
					# Leat
					self.popLetter()
					# Define paradigm list (leat)
					for i in range(0, len(sfixList)):
						if i == 2:
							paradigmList.append(self.verb + sfixList[i][0])
						elif i == 3 or i == 7:
							paradigmList.append(self.verb + sfixList[i][0] + ", " + self.verb + sfixList[i][1])
						elif i == 6:
							paradigmList.append(self.verb + sfixList[i][0] + ", " + self.verb + sfixList[i][1] + ", " + self.verb + sfixList[i][2])
						else:
							paradigmList.append(self.verb + sfixList[i])
				else:	
					strChar = self.lastCharGet(self.verb)
					lstStrChar = self.lastLastCharGet(self.verb)
					wkChar = self._fromStrongToWeakSuffixNeg(strChar)
					if self._isConsonant(lstStrChar):
						strChar = lstStrChar + strChar
					# Define paradigm list
					for i in range(0, len(sfixList)):
						if i == 1:
							paradigmList.append(self.verb + wkChar)
						elif i == 2:
							paradigmList.append(self.verb + strChar + sfixList[i][0] + ", " + self.verb + strChar + sfixList[i][1])
						elif i == 3:
							paradigmList.append(self.verb + strChar + sfixList[i][1])
						elif i == 6:
							paradigmList.append(self.verb + strChar + sfixList[i][0] + ", " + self.verb + strChar + sfixList[i][1] + ", " + self.verb + strChar + sfixList[i][3] + ", " + self.verb + strChar + sfixList[i][4])
						elif i == 7:
							paradigmList.append(self.verb + strChar + sfixList[i][0])
						else:
							paradigmList.append(self.verb + strChar + sfixList[i])
						
			elif typeVerb == 3:
				xtr = 'j'
				# Define paradigm list
				for i in range(0, len(sfixList)):
					if i == 1:
						paradigmList.append(self.verb)
					elif i == 2:
						paradigmList.append(self.verb + xtr + sfixList[i][0])
					elif i == 3 or i == 7:
						paradigmList.append(self.verb + xtr + sfixList[i][1])
					elif i == 6:
						paradigmList.append(self.verb + xtr + sfixList[i][1] + ", " + self.verb + xtr + sfixList[i][4] + ", " + self.verb + xtr + sfixList[i][0] + ", " + self.verb + xtr + sfixList[i][3])
					else:
						paradigmList.append(self.verb + xtr + sfixList[i])
			
			# Reset verb to original state
			self.resetVerb()
			return paradigmList
		# Any errors, return -1
		return -1
		
	def _paradigmNegPres(self):
		""" Returns negative present paradigm form """
		# Count syllables to determine verb type
		typeVerb = self.verifyVerb()
		if typeVerb != 0:
			
			# typeVerb 1 => "likestavelses", 2 => "ulikestavelsels", 3 => "kontrakt"
			if typeVerb == 1:
				wkLstChar = self._fromStrongToWeakSuffixNeg(self.lastCharGet(self.verb))
				wkStage = self._fromStrongToWeakStage(self._findStrongStage())
				if wkStage == None:
					return -1
				# Define paradigm form
				paradigm = self.verb + wkStage + wkLstChar
			
			elif typeVerb == 2:
				if self.popLetter() == 'i':
					wkLstChar = self._fromStrongToWeakSuffixNeg(self.lastCharGet(self.verb))
					paradigm = self.verb + wkLstChar
				else:
					if self.verb == 'le':
						paradigm = 'leat'
			
			elif typeVerb == 3:
				paradigm = self.verb
		
		# Reset verb and return paradigm
		self.resetVerb()
		if typeVerb != 0:
			return paradigm

	def _paradigmPerf(self):
		""" Returns PERFECT paradigm form """
		# Count syllables to determine verb type
		if self.verb == 'leat':
			return 'leamaš'
		typeVerb = self.verifyVerb()
		if typeVerb != 0:
			
			# typeVerb 1 => "likestavelses", 2 => "ulikestavelsels", 3 => "kontrakt"
			if typeVerb == 1:
				xtr = 'n'
				wkLstChar = self._fromStrongToWeakSuffixKond(self.lastCharGet(self.verb))
				if wkLstChar == 'o':
					# Fetch changes
					strStage = self._findStrongStage()
					wkDftn = self._fromStrongToWeakDifton(self._diftonGet())
					paradigm = self.verb + wkDftn + strStage + wkLstChar + xtr
				else:
					paradigm = self.verb + wkLstChar + xtr
			
			elif typeVerb == 2:
				self.popLetter()
				paradigm = self.verb + 'an'
			
			elif typeVerb == 3:
				paradigm = self.verb + 'n'
		
		# Reset verb and return paradigm
		self.resetVerb()
		if typeVerb != 0:
			return paradigm
	
	def _paradigmActioEssive(self):
		""" Returns PERFECT paradigm form """
		# Count syllables to determine verb type
		typeVerb = self.verifyVerb()
		if typeVerb != 0:
			leat = 'le'
			# typeVerb 1 => "likestavelses", 2 => "ulikestavelsels", 3 => "kontrakt"
			if typeVerb == 1 or typeVerb == 3:
				paradigm = self.verb + 'me, -min'
			
			if typeVerb == 2:
				self.popLetter()
				if self.verb == 'le':
					self.popLetter()
				paradigm = self.verb + 'eame, -men'

		# Reset verb and return paradigm
		self.resetVerb()
		if typeVerb != 0:
			return paradigm

	def paradigmGet(self, num):
		""" Return appropriate paradigm (list) """
		if num == PRESENT:
			return self._paradigmListPres()
		elif num == PRETERITE:
			return self._paradigmListPast()
		elif num == CONDITIONAL:
			return self._paradigmListCond()
		elif num == POTENTIAL:
			return self._paradigmListPots()
		elif num == NEG_PRES:
			return self._paradigmNegPres()
		elif num == NEG_IMP:
			if self.verb == "leat":
				return "leage"
			else:
				return self._paradigmNegPres()
		elif num == PERFECT:
			return self._paradigmPerf()
		elif num == NEG_PRET:
			if self.verb == "leat":
				return "lean"
			else: 
				return self._paradigmPerf()
		elif num == ACTIO_ESSIVE:
			return self._paradigmActioEssive()
		elif num == IMPERATIVE:
			return self._paradigmListImp()
		else:
			return -1
