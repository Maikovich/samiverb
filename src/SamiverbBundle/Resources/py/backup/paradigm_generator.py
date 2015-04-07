#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

class PreAndSuffixesDict(object):
	def __init__(self, verb):
		self.verb = self.original = verb.lower()
		self.verbfname = "verb/" + self.original + ".xml";
		self.stages = {"kŋ": "ŋ", "đđ": "đ", "ff": "f", "ll": "l", "hll": "hl", "ljj": "lj", "mm": "m", "nn": "n", "nnj": "nj", "rr": "r", "hrr": "hr", "ss": "s", "šš": "š", "ŧŧ": "ŧ", "vv": "v", "bb": "pp", "dd": "tt", "ddj": "dj", "dj": "j", "gg": "kk", "zz": "cc", "žž": "čč", "hcc": "hc", "hc": "z", "hčč": "hč", "hč": "ž", "hkk": "hk", "hk": "g", "hpp": "hp", "hp": "b", "htt": "ht", "ht": "đ", "bp": "pm", "pm": "m", "dn": "tn", "tn": "n", "dnj": "tnj", "tnj": "nj", "gn": "kn", "kn": "n", "rbm": "rpm", "rdn": "rtn", "rdjn": "rtjn", "rgn": "rkn", "đb": "đbb", "đg": "đgg", "đj": "đjj", "đv": "đvv", "ib": "ibb", "ic": "icc", "id": "idd", "if": "iff", "ig": "igg", "ik": "ikk", "il": "ill", "ihl": "ihll", "ihm": "ihmm", "ihn": "ihnn", "ip": "ipp", "ir": "irr", "is": "iss", "it": "itt", "iv": "ivv", "iz": "izz", "lb": "lbb", "lc": "lcc", "ld": "ldd", "lf": "lff", "lg": "lgg", "lk": "lkk", "lj": "ljj", "lp": "lpp", "ls": "lss", "lš": "lšš", "lt": "ltt", "lv": "lvv", "lž": "lžž", "mb": "mbb", "mp": "mpp", "ms": "mss", "mš": "mšš", "nc": "ncc", "nč": "nčč", "nd": "ndd", "ns": "nss", "nt": "ntt", "nz": "nzz", "nž": "nžž", "ŋg": "ŋgg", "ŋk": "ŋkk", "rb": "rbb", "rc": "rcc", "rč": "rčč", "rd": "rdd", "rf": "rff", "rg": "rgg", "rj": "rjj", "rk": "rkk", "rp": "rpp", "rs": "rss", "rš": "ršš", "rt": "rtt", "rv": "rvv", "rz": "rzz", "rž": "ržž", "sk": "skk", "sm": "smm", "sp": "spp", "st": "stt", "šk": "škk", "šm": "šmm", "št": "štt", "šv": "švv", "tk": "tkk", "tm": "tmm", "vd": "vdd", "vg": "vgg", "vgŋ": "vŋŋ", "vj": "vjj", "vk": "vkk", "vl": "vll", "vhl": "vhll", "vp": "vpp", "vr": "vrr", "vt": "vtt", "vž": "vžž", "đbm": "đmm", "đgŋ": "đŋŋ", "ibm": "imm", "idn": "inn", "igŋ": "iŋŋ", "lbm": "lmm", "ldn": "lnn", "lgŋ": "lŋŋ", "vdn": "vnn", "vdnj": "vnnj", "isk": "iskk", "ist": "istt", "mšk": "mškk", "nsk": "nskk", "nst": "nstt", "rsk": "rskk", "rst": "rstt", "vsk": "vskk", "kč": "včč", "ks": "vss", "kst": "vstt", "kš": "kšš", "kt": "vtt"}
		
		self.exclist = ["vuoššat", "cissat"]
		
		self.a_prefix = ["an", "at", "á", "e", "abeahtti", "aba", "at", "abehtet", "et"]
		self.i_prefix = ["án", "át", "á", "e", "ibeahtti", "iba", "it", "ibehtet", "et"]
		self.u_prefix = ["un", "ut", "u", "o", "ubeahtti", "uba", "ut", "ubehtet", "ot"]
		self.leat_prefix = ["an", "at", "a", "tne", "ahppi", "aba", "at", "hpet", "at"]
		self.ii_prefix = ["an", "at", "a", "etne", "eahppi", "eaba", "it", "ehpet", "it"]
		self.k_prefix = ["n", "t", "", "jetne", "beahtti", "ba", "t", "behtet", "jit"]

		self.a_prefixp = ["en", "et", "ai", "aime", "aide", "aiga", "aimet", "aidet", "e"]
		self.i_prefixp = ["en", "et", "ii", "iime", "iide", "iiga", "iimet", "iidet", "e"]
		self.u_prefixp = ["on", "ot", "ui", "uime", "uide", "uiga", "uimet", "uidet", "o"]
		self.leat_prefixp = ["djen", "djet", "i", "imme", "idde", "igga", "immet", "iddet", "dje"]
		self.ii_prefixp = ["in", "it", "ii", "eimme", "eidde", "eigga", "eimmet", "eiddet", "edje"]
		self.k_prefixp = ["jin", "jit", "i", "ime", "ide", "iga", "imet", "idet", "jedje"]

		self.nekt_sfix = ["in", "it", "ii", "ean", "eahppi", "eaba", "eat", "ehpet", "eai"]

		self.diftons = {"ea": "e", "uo": "u", "ie": "i", "oa": "o"}
		self.pronoms = ["Mun", "Don", "Son", "Moai", "Doai", "Soai", "Mii", "Dii", "Sii"]

class Verb(PreAndSuffixesDict):
	def __init__(self, verb):
		PreAndSuffixesDict.__init__(self, verb)

	def popLetter(self):
		tmp = len(list(list(self.verb.decode('utf-8'))[-1].encode('utf-8')))
		self.verb, result = self.verb[:-tmp], self.verb[-tmp:]
		return result

	def _isVowel(self, c):
		vowels = ['a', 'á', 'e', 'i', 'u', 'o', 'e']
		for x in vowels:
			if c == x:
				return True
		return False

	def _isConsonant(self, c):
		consonants = ['b', 'c', 'č', 'd', 'đ', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'ŋ', 'p', 'r', 's', 'š', 't', 'ŧ', 'v', 'z', 'ž']
		for x in consonants:
			if c == x:
				return True
		return False

	def _syllableCount(self):
		tmp = list(self.verb.decode('utf-8'))
		syll = 1
		if self._isConsonant(tmp[0].encode('utf-8')) and self._isConsonant(tmp[1].encode('utf-8')):
			syll = 0
		if len(self.verb) > 2:
			for i in range(1, len(tmp)-1):
				if self._isConsonant(tmp[i].encode('utf-8')) and self._isVowel(tmp[i+1].encode('utf-8')):
					syll += 1
		return syll

	def verifyVerb(self):
		if self.popLetter() == 't':
			syll = self._syllableCount()
			if syll > 0:
				pfix = list(self.verb.decode('utf-8'))[-1].encode('utf-8')
				if syll % 2 == 0:
					if pfix == 'a' or pfix == 'i' or pfix == 'u':
						return 1
					if pfix == 'á' or pfix == 'e' or pfix == 'o':
						return 3
				else:
					if pfix == 'i' or pfix == "a":
						return 2
		return 0

	def _findStrongStage(self):
		strong = ""
		n = 0
		while len(self.verb) > 0:
			strong = self.popLetter() + strong
			if strong in self.stages:
				n = 1
			if n == 1 and strong not in self.stages:
				tmp = len(list(list(strong.decode('utf-8'))[0].encode('utf-8')))
				strong, res = strong[tmp:], strong[:tmp]
				self.verb = self.verb + res
				break
		return strong
		
	def _fromStrongToWeakStage(self, s):
		if self.original in self.exclist:
			return s
		try:
			return self.stages[s]
		except KeyError:
			return None	

	def __prefixPresent(self, t):
		if t == 1:
			if self.verb[-1] == 'a':
				self.popLetter()
				return self.a_prefix
			if self.verb[-1] == 'i':
				self.popLetter()
				return self.i_prefix
			if self.verb[-1] == 'u':
				self.popLetter()
				return self.u_prefix
		if t == 2:
			if self.verb[-1] == 'a':
				self.popLetter()
				return self.leat_prefix
			self.popLetter()
			return self.ii_prefix
		if t == 3:
			return self.k_prefix

	def __prefixPast(self, t):
		if t == 1:
			if self.verb[-1] == 'a':
				self.popLetter()
				return self.a_prefixp
			if self.verb[-1] == 'i':
				self.popLetter()
				return self.i_prefixp
			if self.verb[-1] == 'u':
				self.popLetter()
				return self.u_prefixp
		if t == 2:
			if self.verb[-1] == 'a':
				self.popLetter()
				return self.leat_prefixp
			self.popLetter()
			return self.ii_prefixp
		if t == 3:
			return self.k_prefixp

	def __prefixConditionalis(self, t):
		if t == 1 or t == 3:
			return self.ii_prefixp
		if t == 2:
			if self.verb[-1] == 'a':
				self.popLetter()
			self.popLetter()
			return self.i_prefixp

	def __prefixPotentialis(self, t):
		if t == 1 or t == 3:
			return self.ii_prefix
		if t == 2:
			return self.a_prefix
			
	def _prefix(self, t, form):
		if form == 1:
			return self.__prefixPresent(t)
		if form == 2:
			return self.__prefixPast(t)
		if form == 3:
			return self.__prefixConditionalis(t)
		if form == 4:
			return self.__prefixPotentialis(t)

	def _diftonGet(self):
		s = ""
		while len(self.verb) > 0:
			tmp = list(self.verb.decode('utf-8'))
			if self._isConsonant(tmp[-1].encode('utf-8')):
				break
			s = self.popLetter() + s
		return s

	def _fromStrongToWeakDifton(self, d):
		try:
			s = self.diftons[d]
		except KeyError:
			return d
		return s

	def presens(self):
		t = self.verifyVerb()
		if t != 0:
			paradigm = []
			prefix = self._prefix(t, 1)
			if t == 1:
				strong = self._findStrongStage()
				weak = self._fromStrongToWeakStage(strong)
				difton = self._diftonGet() 
				changedifton = self._fromStrongToWeakDifton(difton)
				if weak == None:
					return -1
				for i in range(0, len(prefix)):
					if i == 0 or i == 1:
						paradigm.append(self.pronoms[i] + " " + self.verb + difton + weak + prefix[i])
					elif i == 3 or i == 8:
						paradigm.append(self.pronoms[i] + " " + self.verb + changedifton + strong + prefix[i])
					else:
						paradigm.append(self.pronoms[i] + " " + self.verb + difton + strong + prefix[i])
			elif t == 2:
				for i in range(0, len(prefix)):
					if i == 6:
						paradigm.append(self.pronoms[i] + " " + self.verb + prefix[6] + ", -" + self._suffixGet() + prefix[1])
					else:
						paradigm.append(self.pronoms[i] + " " + self.verb + prefix[i])
			elif t == 3:
				for i in range(0, len(prefix)):
					paradigm.append(self.pronoms[i] + " " + self.verb + prefix[i])
			with open(self.verbfname, 'a') as f:
				f.write('<tense name="Presens">')
			for x in paradigm:
				with open(self.verbfname, 'a') as f:
					f.write("<" + self.pronoms[paradigm.index(x)].lower() + ">" + x + "</" + self.pronoms[paradigm.index(x)].lower() + ">")
			with open(self.verbfname, 'a') as f:
				f.write('</tense>')
		self.verb = self.original

	def _suffixGet(self):
		return list(self.verb.decode('utf-8'))[-1].encode('utf-8')

	def _fromStrongToWeakSuffixPast(self, x):
		if x == 'e':
			self.popLetter()
			return 'i'
		elif x == 'o':
			self.popLetter()
			return 'u'
		elif x == 'á'.decode('utf-8').encode('utf-8'):
			self.popLetter()
			return 'á'

	def _fromStrongToWeakSuffixPots(self, x):
		if x == 'a':
			self.popLetter()
			return x
		elif x == 'i':
			self.popLetter()
			return 'e'
		elif x == 'u':
			self.popLetter()
			return 'o'
			
	def preterium(self):
		t = self.verifyVerb()
		if t != 0:
			paradigm = []
			prefix = self._prefix(t, 2)
			if t == 1:
				strong = self._findStrongStage()
				weak = self._fromStrongToWeakStage(strong)
				difton = self._diftonGet() 
				changedifton = self._fromStrongToWeakDifton(difton)
				if weak == None:
					return -1
				for i in range(0, len(prefix)):
					if i == 0 or i == 1 or i == 8:
						paradigm.append(self.pronoms[i] + " " + self.verb + changedifton + strong + prefix[i])
					else:
						if prefix[2] == "ii":
							paradigm.append(self.pronoms[i] + " " + self.verb + changedifton + weak + prefix[i])
						else:
							paradigm.append(self.pronoms[i] + " " + self.verb + difton + weak + prefix[i])
			elif t == 2:
				for i in range(0, len(prefix)):
					paradigm.append(self.pronoms[i] + " " + self.verb + prefix[i])
			elif t == 3:
				sfix = self._suffixGet()
				changesfix = self._fromStrongToWeakSuffixPast(sfix)
				for i in range(0, len(prefix)):
					if i == 0 or i == 1 or i == 8:
						paradigm.append(self.pronoms[i] + " " + self.verb + sfix + prefix[i])
					else:
						paradigm.append(self.pronoms[i] + " " + self.verb + changesfix + prefix[i])
			with open(self.verbfname, 'a') as f:
				f.write('<tense name="Preterium">')
			for x in paradigm:
				with open(self.verbfname, 'a') as f:
					f.write("<" + self.pronoms[paradigm.index(x)].lower() + ">" + x + "</" + self.pronoms[paradigm.index(x)].lower() + ">")
			with open(self.verbfname, 'a') as f:
				f.write('</tense>')
		self.verb = self.original

	def _fromStrongToWeakSuffixKond(self, x):
		if x == 'i':
			self.popLetter()
			return 'á'
		elif x == 'u':
			self.popLetter()
			return 'o'
		elif x == 'a':
			self.popLetter()
			return x

	def kondisjonalis(self):
		t = self.verifyVerb()
		if t != 0:
			paradigm = []
			prefix = self._prefix(t, 3)
			if t == 1:
				extra = 'š'
				sfix = self._suffixGet()
				changesfix = self._fromStrongToWeakSuffixKond(sfix)
				weak = self._fromStrongToWeakStage(self._findStrongStage())
				difton = self._diftonGet() 
				changedifton = self._fromStrongToWeakDifton(difton)
				if weak == None:
					return -1
				if sfix == 'u':
					self.form = self.verb + changedifton + weak + changesfix + extra
					for i in range(0, len(prefix)):
						paradigm.append(self.pronoms[i] + " " + self.form + prefix[i])
				else:
					self.form = self.verb + difton + weak + changesfix + extra
					for i in range(0, len(prefix)):
						paradigm.append(self.pronoms[i] + " " + self.form + prefix[i])
			elif t == 2:
				extra = 'ivčč'
				self.form = self.verb + extra
				for i in range(0, len(prefix)):
					paradigm.append(self.pronoms[i] + " " + self.form + prefix[i])
			elif t == 3:
				extra = 'š'
				self.form = self.verb + extra
				for i in range(0, len(prefix)):
					paradigm.append(self.pronoms[i] + " " + self.form + prefix[i])
			with open(self.verbfname, 'a') as f:
				f.write('<tense name="Kondisjonalis">')
			for x in paradigm:
				with open(self.verbfname, 'a') as f:
					f.write("<" + self.pronoms[paradigm.index(x)].lower() + ">" + x + "</" + self.pronoms[paradigm.index(x)].lower() + ">")
			with open(self.verbfname, 'a') as f:
				f.write('</tense>')
				
		self.verb = self.original

	def _fromStrongToWeakSuffixNeg(self, x):
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
			if self._suffixGet() == 'r':
				self.popLetter()
				return 'r'
			elif self._suffixGet() == 'l':
				self.popLetter()
				return 'l'
			elif self._suffixGet() == 'i':
				self.popLetter()
				if self._suffixGet() == 'l':
					return 'it';
			return 't'
		elif x == 't':
			self.popLetter()
			if self._suffixGet() == 'š':
				self.popLetter()
				return 'š'
			elif self._suffixGet() == 's':
				self.popLetter()
				return 's'
			return 't'
		elif x == 'k':
			self.popLetter()
			if self._suffixGet() == 's':
				self.popLetter()
				return 's'
			return 'k'
		elif x == 'm':
			self.popLetter()
			if self._suffixGet() == 's':
				self.popLetter()
				return 's'
			return 'm'
		elif x == 'š' or x == 'n' or x == 'l' or x == 's':
			self.popLetter()
			return x

	def nekt_pres(self):
		t = self.verifyVerb()
		if t != 0:
			if t == 1:
				changesfix = self._fromStrongToWeakSuffixNeg(self._suffixGet())
				weak = self._fromStrongToWeakStage(self._findStrongStage())
				if weak == None:
					return -1
				paradigm = self.verb + weak + changesfix
			elif t == 2:
				if self.popLetter() == 'i':
					changesfix = self._fromStrongToWeakSuffixNeg(self._suffixGet())
					paradigm = self.verb + changesfix
				else:
					if self.verb == 'le':
						paradigm = 'leat'
			elif t == 3:
				paradigm = self.verb
		self.verb = self.original
		if t != 0:
			return paradigm

	def perf_part(self):
		t = self.verifyVerb()
		if t != 0:
			if t == 1:
				extra = 'n'
				changesfix = self._fromStrongToWeakSuffixKond(self._suffixGet())
				if changesfix == 'o':
					strong = self._findStrongStage()
					changedifton = self._fromStrongToWeakDifton(self._diftonGet())
					paradigm = self.verb + changedifton + strong + changesfix + extra
				else:
					paradigm = self.verb + changesfix + extra
			elif t == 2:
				self.popLetter()
				paradigm = self.verb + 'an'
			elif t == 3:
				paradigm = self.verb + 'n'
		self.verb = self.original
		if t != 0:
			return paradigm

	def nektingPres(self):
		nektpres = self.nekt_pres()
		with open(self.verbfname, 'a') as f:
			f.write('<tense name="Nekting (pres.)">')
		for i in range(0, len(self.nekt_sfix)):
			with open(self.verbfname, 'a') as f:
				f.write("<" + self.pronoms[i].lower() + ">" + self.pronoms[i] + " " + self.nekt_sfix[i] + " " + nektpres + "</" + self.pronoms[i].lower() + ">")
		with open(self.verbfname, 'a') as f:
			f.write('</tense>')
	
	def nektingPret(self):
		nektpret = self.perf_part()
		with open(self.verbfname, 'a') as f:
			f.write('<tense name="Nekting (pret.)">')
		for i in range(0, len(self.nekt_sfix)):
			with open(self.verbfname, 'a') as f:
				f.write("<" + self.pronoms[i].lower() + ">" + self.pronoms[i] + " " + self.nekt_sfix[i] + " " + nektpret + "</" + self.pronoms[i].lower() + ">")
		with open(self.verbfname, 'a') as f:
			f.write('</tense>')

	def nektingCond(self):
		with open(self.verbfname, 'a') as f:
			f.write('<tense name="Nekting (kond.)">')
		for i in range(0, len(self.nekt_sfix)):
			with open(self.verbfname, 'a') as f:
				f.write("<" + self.pronoms[i].lower() + ">" + self.pronoms[i] + " " + self.nekt_sfix[i] + " " + self.form + 'e' + "</" + self.pronoms[i].lower() + ">")
		with open(self.verbfname, 'a') as f:
			f.write('</tense>')
	
	def nektingPots(self):
		with open(self.verbfname, 'a') as f:
			f.write('<tense name="Nekting (potens.)">')
		for i in range(0, len(self.nekt_sfix)):
			with open(self.verbfname, 'a') as f:
				f.write("<" + self.pronoms[i].lower() + ">" + self.pronoms[i] + " " + self.nekt_sfix[i] + " " + self.potsform + "</" + self.pronoms[i].lower() + ">")
		with open(self.verbfname, 'a') as f:
			f.write('</tense>')
			
	def perfektumPres(self):
		if self.verb == 'leat':
			perfpart = 'leamaš'
		else:
			perfpart = self.perf_part()
		leat = 'le'
		with open(self.verbfname, 'a') as f:
			f.write('<tense name="Perfektum (pres.)">')
		for i in range(0, len(self.leat_prefix)):
			with open(self.verbfname, 'a') as f:
				f.write("<" + self.pronoms[i].lower() + ">" + self.pronoms[i] + " " + leat + self.leat_prefix[i] + " " + perfpart + "</" + self.pronoms[i].lower() + ">")
		with open(self.verbfname, 'a') as f:
			f.write('</tense>')
			
	def perfektumPret(self):
		if self.verb == 'leat':
			perfpart = 'leamaš'
		else:
			perfpart = self.perf_part()
		leat = 'le'
		with open(self.verbfname, 'a') as f:
			f.write('<tense name="Perfektum (pret.)">')
		for i in range(0, len(self.leat_prefix)):
			with open(self.verbfname, 'a') as f:
				f.write("<" + self.pronoms[i].lower() + ">" + self.pronoms[i] + " " + leat + self.leat_prefixp[i] + " " + perfpart + "</" + self.pronoms[i].lower() + ">")
		with open(self.verbfname, 'a') as f:
			f.write('</tense>')
			
	def aktioessivPres(self):
		t = self.verifyVerb()
		if t != 0:
			leat = 'le'
			if t == 1 or t == 3:
				suffix = 'me'
			if t == 2:
				self.popLetter()
				if self.verb == 'le':
					self.popLetter()
				suffix = 'eame'
			with open(self.verbfname, 'a') as f:
				f.write('<tense name="Aktio essiv (pres.)">')
			for i in range(0, len(self.leat_prefix)):
				with open(self.verbfname, 'a') as f:
					f.write("<" + self.pronoms[i].lower() + ">" + self.pronoms[i] + " " + leat + self.leat_prefix[i] + " " + self.verb + suffix + "</" + self.pronoms[i].lower() + ">")	
			with open(self.verbfname, 'a') as f:
				f.write('</tense>')
		self.verb = self.original
	
	def aktioessivPret(self):
		t = self.verifyVerb()
		if t != 0:
			leat = 'le'
			if t == 1 or t == 3:
				suffix = 'me'
			if t == 2:
				self.popLetter()
				if self.verb == 'le':
					self.popLetter()
				suffix = 'eame'
			with open(self.verbfname, 'a') as f:
				f.write('<tense name="Aktio essiv (pret.)">')
			for i in range(0, len(self.leat_prefix)):
				with open(self.verbfname, 'a') as f:
					f.write("<" + self.pronoms[i].lower() + ">" + self.pronoms[i] + " " + leat + self.leat_prefixp[i] + " " + self.verb + suffix + "</" + self.pronoms[i].lower() + ">")	
			with open(self.verbfname, 'a') as f:
				f.write('</tense>')
		self.verb = self.original

	def potentialis(self):
		t = self.verifyVerb()
		if t != 0:
			paradigm = []
			prefix = self._prefix(t, 4)
			if t == 2:
				extra = 'e'
				self.popLetter()
				if self._suffixGet() == 'e':
					extra = 'et'
					self.popLetter()
				for i in range(0, len(prefix)):
					if i == 0 or i == 1:
						paradigm.append(self.pronoms[i] + " " + self.verb + 'eačč' + prefix[i])
					elif i == 2:
						suffix = self._suffixGet()
						self.potsform = self.verb + 'eaš, -' + suffix + 'eš, -' + suffix + 'eažžá'
						paradigm.append(self.pronoms[i] + " " + self.potsform)
					elif i == 3:
						paradigm.append(self.pronoms[i] + " " + self.verb + 'ežž' + extra)
					elif i == 8:
						paradigm.append(self.pronoms[i] + " " + self.verb + 'ežž' + prefix[8])
					else:
						paradigm.append(self.pronoms[i] + " " + self.verb + 'eažž' + prefix[i])
			if t == 1:
				changesfix = self._fromStrongToWeakSuffixPots(self._suffixGet())
				weak = self._fromStrongToWeakStage(self._findStrongStage())
				if weak == None:
					return -1
				difton = self._diftonGet() 
				changedifton = self._fromStrongToWeakDifton(difton)
				if changesfix == 'a':
					changedifton = difton
				for i in range(0, len(prefix)):
					if i == 2:
						self.potsform = self.verb + changedifton + weak + changesfix + 'š'
						paradigm.append(self.pronoms[i] + " " + self.potsform)
					elif i == 6:
						paradigm.append(self.pronoms[i] + " " + self.verb + changedifton + weak + changesfix + 'ž' + prefix[6] + ", -" + 'ž' + prefix[1])
					else:
						paradigm.append(self.pronoms[i] + " " + self.verb + changedifton + weak + changesfix + 'ž' + prefix[i])				
			if t == 3:
				for i in range(0, len(prefix)):
					if i == 2:
						self.potsform = self.verb + 'š'
						paradigm.append(self.pronoms[i] + " " + self.potsform)
					elif i == 6:
						paradigm.append(self.pronoms[i] + " " + self.verb + 'ž' + prefix[6] + ", -" + 'ž' + prefix[1])
					else:
						paradigm.append(self.pronoms[i] + " " + self.verb + 'ž' + prefix[i])	
			with open(self.verbfname, 'a') as f:
				f.write('<tense name="Potensialis">')
			for x in paradigm:
				with open(self.verbfname, 'a') as f:
					f.write("<" + self.pronoms[i].lower() + ">" + x + "</" + self.pronoms[i].lower() + ">")	
			with open(self.verbfname, 'a') as f:
				f.write('</tense>')
			print paradigm
			print self.potsform
		self.verb = self.original		
				
		
	def all(self):
		self.presens()
		print self.verb
		self.nektingPres()
		self.preterium()
		self.nektingPret()
		self.kondisjonalis()
		self.nektingCond()
		self.potentialis()
		self.nektingPots()
		self.perfektumPres()
		self.perfektumPret()
		self.aktioessivPres()
		self.aktioessivPret()

def main():
	if len(sys.argv) != 2:
		print "Something wrong happened!"
		return
	input = sys.argv[1]
	fname = 'verb/' + input + '.xml'
	
	try:
		with open(fname, 'w') as f:
			f.write("<verb name=\"" + input + "\">")
		Verb(input).all()
		with open(fname, 'a') as f:
			f.write("</verb>")
	except:
		os.remove(fname)
		print 0
		return
	print 1

def test():
	if len(sys.argv) != 2:
		print "Something wrong happened!"
		return
	input = sys.argv[1]
	Verb(input).all()
	
if __name__ == '__main__':
	main()