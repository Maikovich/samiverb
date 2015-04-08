#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Mike Voets, 2014, mike@samiverb.com

class SamiSfixAndSyntaxLibrary(object):
	""" A tiny library for Sami suffixes and methods """
	def __init__(self):
		self.stageList = {"kŋ": "ŋ", "đđ": "đ", "ff": "f", "ll": "l", "hll": "hl", 
"ljj": "lj", "mm": "m", "nn": "n", "nnj": "nj", "rr": "r", "hrr": "hr", "ss": 
"s", "šš": "š", "ŧŧ": "ŧ", "vv": "v", "bb": "pp", "dd": "tt", "ddj": "dj", "dj"
: "j", "gg": "kk", "zz": "cc", "žž": "čč", "hcc": "hc", "hc": "z", "hčč": "hč",
 "hč": "ž", "hkk": "hk", "hk": "g", "hpp": "hp", "hp": "b", "htt": "ht", "ht": 
"đ", "bm": "pm", "pm": "m", "dn": "tn", "tn": "n", "dnj": "tnj", "tnj": "nj", 
"gn": "kn", "kn": "n", "rbm": "rpm", "rdn": "rtn", "rdjn": "rtjn", "rgn": "rkn"
, "đb": "đbb", "đg": "đgg", "đj": "đjj", "đv": "đvv", "ib": "ibb", "ic": "icc",
 "id": "idd", "if": "iff", "ig": "igg", "ik": "ikk", "il": "ill", "ihl": "ihll"
, "ihm": "ihmm", "ihn": "ihnn", "ip": "ipp", "ir": "irr", "is": "iss", "it": 
"itt", "iv": "ivv", "iz": "izz", "lb": "lbb", "lc": "lcc", "ld": "ldd", "lf": 
"lff", "lg": "lgg", "lk": "lkk", "lj": "ljj", "lp": "lpp", "ls": "lss", "lš": 
"lšš", "lt": "ltt", "lv": "lvv", "lž": "lžž", "mb": "mbb", "mp": "mpp", "ms": 
"mss", "mš": "mšš", "nc": "ncc", "nč": "nčč", "nd": "ndd", "ns": "nss", "nt": 
"ntt", "nz": "nzz", "nž": "nžž", "ŋg": "ŋgg", "ŋk": "ŋkk", "rb": "rbb", "rc": 
"rcc", "rč": "rčč", "rd": "rdd", "rf": "rff", "rg": "rgg", "rj": "rjj", "rk": 
"rkk", "rp": "rpp", "rs": "rss", "rš": "ršš", "rt": "rtt", "rv": "rvv", "rz": 
"rzz", "rž": "ržž", "sk": "skk", "sm": "smm", "sp": "spp", "st": "stt", "šk": 
"škk", "šm": "šmm", "št": "štt", "šv": "švv", "tk": "tkk", "tm": "tmm", "vd": 
"vdd", "vg": "vgg", "vgŋ": "vŋŋ", "vj": "vjj", "vk": "vkk", "vl": "vll", "vhl":
 "vhll", "vp": "vpp", "vr": "vrr", "vt": "vtt", "vž": "vžž", "đbm": "đmm", 
"đgŋ": "đŋŋ", "ibm": "imm", "idn": "inn", "igŋ": "iŋŋ", "lbm": "lmm", "ldn": 
"lnn", "lgŋ": "lŋŋ", "vdn": "vnn", "vdnj": "vnnj", "isk": "iskk", "ist": "istt"
, "mšk": "mškk", "nsk": "nskk", "nst": "nstt", "rsk": "rskk", "rst": "rstt", 
"vsk": "vskk", "kč": "včč", "ks": "vss", "kst": "vstt", "kš": "kšš", "kt": 
"vtt"}
		
		self.vowels = ['a', 'á', 'e', 'i', 'u', 'o', 'e']
		self.consonants = ['b', 'c', 'č', 'd', 'đ', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'ŋ', 'p', 'r', 's', 'š', 't', 'ŧ', 'v', 'z', 'ž']
		self.diftons = {"ea": "e", "uo": "u", "ie": "i", "oa": "o"}
		self.pronoms = ["Mun", "Don", "Son", "Moai", "Doai", "Soai", "Mii", "Dii", "Sii"]

		self.expectionsList = ["vuoššat", "cissat"]
		
		self.sfixAVerbPres = ["an", "at", "á", "e", "abeahtti", "aba", "at", "abehtet", "et"]
		self.sfixIVerbPres = ["án", "át", "á", "e", "ibeahtti", "iba", "it", "ibehtet", "et"]
		self.sfixUVerbPres = ["un", "ut", "u", "o", "ubeahtti", "uba", "ut", "ubehtet", "ot"]
		self.sfixLeatPres = ["an", "at", "a", "tne", "ahppi", "aba", "at", "hpet", "at"]
		self.sfixNegVerbPres = ["an", "at", "a", "etne", "eahppi", "eaba", "it", "ehpet", "it"]
		self.sfixContrVerbPres = ["n", "t", "", "jetne", "beahtti", "ba", "t", "behtet", "jit"]

		self.sfixAVerbPast = ["en", "et", "ai", "aime", "aide", "aiga", "aimet", "aidet", "e"]
		self.sfixIVerbPast = ["en", "et", "ii", "iime", "iide", "iiga", "iimet", "iidet", "e"]
		self.sfixUVerbPast = ["on", "ot", "ui", "uime", "uide", "uiga", "uimet", "uidet", "o"]
		self.sfixLeatPast = ["djen", "djet", "i", "imme", "idde", "igga", "immet", "iddet", "dje"]
		self.sfixNegVerbPast = ["in", "it", "ii", "eimme", "eidde", "eigga", "eimmet", "eiddet", "edje"]
		self.sfixContrVerbPast = ["jin", "jit", "i", "ime", "ide", "iga", "imet", "idet", "jedje"]
		self.sfixRegVerbImp = ["on", "", "os", "u", ["i", "u"], "oska", "ot", ["et", "it", "ot"], "oset"]
		self.sfixOtherVerbImp = ["ehkon", "eage", ["ehkos", "us"], ["eahkku", "eadnu"], "eahkki", "ehkoska", ["ehkot", "eahkkut", "eatnot", "etnot", "eadnot"], ["ehket", "eahkkit"], "ehkoset"]
		
		self.partImpNeg = ["allon", "ale", "allos", "allu", "alli", "alloska", "allot, allut", "allet, allit", "alloset"]	
		self.partNeg = ["in", "it", "ii", "ean", "eahppi", "eaba", "eat", "ehpet", "eai"]

	def _isVowel(self, character):
		""" Returns True if character is a vowel, otherwise False """
		for x in self.vowels:
			if character == x:
				return True
		return False

	def _isConsonant(self, character):
		""" Returns True if character is a consonant, otherwise False """
		for x in self.consonants:
			if character == x:
				return True
		return False

	def lastCharGet(self, word):
		""" Returns last character from word """
		return list(word.decode('utf-8'))[-1].encode('utf-8')

	def lastLastCharGet(self, word):
		""" Returns last character from word """
		return list(word.decode('utf-8'))[-2].encode('utf-8')
	
	def syllableCount(self, word):
		""" Counts the amount of syllables in a word """
		# Little hack to list all characters including the special utf-8 chars
		tmp = list(word.decode('utf-8'))
		# Start analyzing the verb
		if len(word) > 2:
			syllables = 1
			# Take in account the first two letters and find out if both are consonants (if true => no syllables confirmed yet)
			if self._isConsonant(tmp[0].encode('utf-8')) and self._isConsonant(tmp[1].encode('utf-8')):
				syllables = 0
			for i in range(1, len(tmp)-1):
				# For each vowel after a consontant, there's a syllable
				if self._isConsonant(tmp[i].encode('utf-8')) and self._isVowel(tmp[i+1].encode('utf-8')):
					syllables += 1
			return syllables
		return 0

	def _fromStrongToWeakSuffixPast(self, x):
		""" Returns weak form of suffix (past tense) """
		if x == 'e':
			self.popLetter()
			return 'i'
		elif x == 'o':
			self.popLetter()
			return 'u'
		elif x == 'á'.decode('utf-8').encode('utf-8'):
			self.popLetter()
			return 'á'

	def _fromStrongToWeakSuffixKond(self, x):
		""" Returns weak form of suffix (conditionalis) """
		if x == 'i':
			self.popLetter()
			return 'á'
		elif x == 'u':
			self.popLetter()
			return 'o'
		elif x == 'a':
			self.popLetter()
			return x

	def _fromStrongToWeakSuffixPots(self, x):
		""" Returns weak form of suffix (potentialis) """
		if x == 'a':
			self.popLetter()
			return x
		elif x == 'i':
			self.popLetter()
			return 'e'
		elif x == 'u':
			self.popLetter()
			return 'o'

	def _fromStrongToWeakSuffixNeg(self, x):
		""" Returns weak form of suffix (negative) """
		if x == 'i':
			self.popLetter()
			return 'e'
		elif x == 'u':
			self.popLetter()
			return 'o'
		elif x == 'a':
			self.popLetter()
			return x
		elif x == 'h' or x == 'g':
			self.popLetter()
			return 't'
		elif x == 'd':
			self.popLetter()
			if self.lastCharGet(self.verb) == 'r':
				self.popLetter()
				return 'r'
			elif self.lastCharGet(self.verb) == 'l':
				self.popLetter()
				return 'l'
			return 't'
		elif x == 't':
			self.popLetter()
			if self.lastCharGet(self.verb) == 'š':
				self.popLetter()
				return 'š'
			elif self.lastCharGet(self.verb) == 's':
				self.popLetter()
				return 's'
			return 't'
		elif x == 'k':
			self.popLetter()
			if self.lastCharGet(self.verb) == 's':
				self.popLetter()
				return 's'
			return 'k'
		elif x == 'm':
			self.popLetter()
			if self.lastCharGet(self.verb) == 's':
				self.popLetter()
				return 's'
			return 'm'
		elif x == 'š' or x == 'n' or x == 'l' or x == 's':
			self.popLetter()
			return x