'''
pr0ntools
Copyright 2011 John McMaster <JohnDMcMaster@gmail.com>
Licensed under a 2 clause BSD license, see COPYING for details

.pto format?
http://photocreations.ca/panotools/stitch.txt
XXX: use a map instead
'''

'''
# Hugin project file
# generated by Autopano

# Panorama settings:
p w8000 h1200 f2 v250 n"PSD_mask"

# input images:
#-imgfile 2816 2112 "Z:\home\mcmaster\buffer\IC\motorola_mcu_vince\top_metal\5X\0.1\x00000_y00000.jpg"
o f0 y+0.000000 r+0.000000 p+0.000000 u20 d0.000000 e0.000000 v70.000000 a0.000000 b0.000000 c0.000000
'''

import shutil
import os
from pr0ntools.temp_file import ManagedTempFile
from pr0ntools.execute import Execute
from pr0ntools.stitch.merger import Merger
from pr0ntools.pimage import PImage
from pr0ntools.stitch.pto.util import *
from control_point_line import ControlPointLine, AbsoluteControlPointLine
from image_line import *
from variable_line import VariableLine
from mode_line import ModeLine
from panorama_line import PanoramaLine
from optimizer_line import OptimizerLine
from util import print_debug
import pr0ntools.stitch.optimizer
		
'''
class ControlPointLineImage:
	image = None
	x = None
	y = None
	# Index		
	n = None
'''

'''
"autopano-sift-c" "--maxmatches" "0" "--maxdim" "10000" test.pto data/c0_r0.jpg data/c0_r1.jpg
	# Hugin project file generated by APSCpp

	p f2 w3000 h1500 v360  n"JPEG q90"
	m g1 i0

	# i: image file
	# w: width
	# h: height
	# f: field of view, default: 0
	# y: yaw: default 0
	# p: pitch: default 0
	# r: roll, default 90
	i w2816 h2112 f0 a0 b-0.01 c0 d0 e0 p0 r0 v180 y0  u10 n"data/c0_r0.jpg"
	i w2816 h2112 f0 a=0 b=0 c=0 d0 e0 p0 r0 v=0 y0  u10 n"data/c0_r1.jpg"

	v p1 r1 y1

	# automatically generated control points
	# c: control point
	# n0: lowercase n signifies lowercase coord letters
	# N0: uppercase N signifies uppercase coord letters
	# what is t?
	c n0 N1 x1444.778035 y233.742619 X1225.863118 Y967.737131 t0
	c n0 N1 x138.962214 y280.766699 X700.950061 Y337.168418 t0
	c n0 N1 x174.636854 y1506.062901 X409.952583 Y1520.077001 t0
	c n0 N1 x128.111790 y85.436614 X178.862171 Y82.166356 t0
	c n0 N1 x185.913687 y132.074929 X1316.285962 Y258.582828 t0
	c n0 N1 x575.842717 y186.222059 X807.577503 Y201.843139 t0
	c n0 N1 x106.501605 y234.781930 X415.561176 Y260.394812 t0
	c n0 N1 x106.501605 y234.781930 X415.561176 Y260.394812 t0
	c n0 N1 x282.454363 y861.246866 X524.759974 Y796.168031 t0
	c n0 N1 x263.741226 y1023.111056 X507.095358 Y958.025083 t0
	c n0 N1 x255.076623 y1046.452454 X521.642791 Y820.371911 t0
	c n0 N1 x21.128685 y1518.951592 X258.640812 Y1531.902643 t0
	c n0 N1 x154.281249 y1794.318825 X2276.028785 Y629.057778 t0
	c n0 N1 x184.953100 y1459.943702 X420.250084 Y1474.768162 t0
	c n0 N1 x184.953100 y1459.943702 X420.250084 Y1474.768162 t0
	c n0 N1 x176.023646 y1508.324113 X411.531954 Y1522.403846 t0
	c n0 N1 x120.663877 y774.190799 X1884.899395 Y804.325721 t0
	c n0 N1 x151.601649 y1534.284888 X386.385138 Y1549.239989 t0
	c n0 N1 x855.583962 y1992.647570 X1418.183265 Y51.846079 t0
	c n0 N1 x584.941773 y467.957317 X2294.246845 Y658.254045 t0
	c n0 N1 x1217.925413 y935.521381 X1477.978209 Y216.417092 t0
	c n0 N1 x389.932676 y626.473870 X628.094681 Y645.153382 t0
	c n0 N1 x1455.674496 y1538.841677 X1622.255876 Y476.350083 t0

	# :-)


Example file

	p f2 w3000 h1500 v360  n"JPEG q90"
	m g1 i0

	i w2816 h600 f0 a0 b-0.01 c0 d0 e0 p0 r0 v180 y0  u10 n"/tmp/0.6621735916207697.png"
	i w2816 h600 f0 a=0 b=0 c=0 d0 e0 p0 r0 v=0 y0  u10 n"/tmp/0.5022987786350409.png"

	v p1 r1 y1

	# numbers index into above images
	c n0 N1 x983.515978 y31.390674 X860.944595 Y132.080243 t0
	c n0 N1 x652.899413 y71.500283 X807.577503 Y201.843139 t0
	c n0 N1 x474.578071 y154.235865 X107.943696 Y223.202780 t0
	c n0 N1 x774.903103 y186.724081 X1830.890967 Y429.024407 t0
	c n0 N1 x1201.353730 y299.329003 X1269.005225 Y511.798210 t0
	c n0 N1 x1708.592510 y359.149116 X1873.061084 Y499.156064 t0
	c n0 N1 x192.653946 y158.115483 X80.809197 Y254.420106 t0


	# specify variables that should be optimized
	# Seems there is a lone v entry at the end
	# Hugin GUI groups the following by image: y, p, r
	# And these by lens: v, a, b, c, d, e
	# However, .pto specifies them for invidual by image
	v e0 
	v d1 e1 
	v d2 e2 
	v d3 e3 
	v 
'''
class PTOProject:
	def __init__(self):
		# File name, if one exists
		self.file_name = None
		# Raw project text, None is not loaded
		self.text = None
		# If this is a temporary project, have it delete upon destruction
		self.temp_file = None
		# Could be a mix of temp and non-temp, so don't make any ordering assumptions
		self.temp_image_files = set()
	
		# 'p' line
		self.panorama_line = None
		# 'm' line
		self.mode_line = None
		# Those started with #hugin_
		# option_lines = None
		# Raw strings
		self.comment_lines = None
		# c N1 X1225.863118 Y967.737131 n0 t0 x1444.778035 y233.74261
		self.control_point_lines = None
		self.absolute_control_point_lines = None
		self.image_lines = None
		self.optimizer_lines = None
		'''
		I bet lone v lines can be omitted
		# Variable lines
		v
		v d1 e1 p1 r1 y1
		v d2 e2 p2 r2 y2
		v d3 e3 p3 r3 y3
		v
		'''
		self.variable_lines = None
		# Raw strings, we don't know what these are
		self.misc_lines = list()
		# Has this been loaded from the file?
		self.parsed = False
	
	def remove_file_name(self):
		'''Unbound this from the filesystem'''
		self.ensure_text_loaded()
		self.file_name = None
	
	def copy(self):
		'''Return an unsaved but identical project'''
		return PTOProject.from_text(self.get_text())
	
	def index_to_image(self, index):
		lines = self.get_image_lines()
		if index >= len(lines):
			raise IndexError('index: %d, items: %d' % (index, len(lines)))
		return lines[index]
	
	def assert_uniform_images(self):
		'''All images have same width and height'''
		w = None
		h = None
		for i in self.get_image_lines():
			if w is None:
				w = i.width()
			if h is None:
				h = i.height()
			if w != i.width():
				raise Exception('Mismatched width')
			if h != i.height():
				raise Exception('Mismatched height')
	
	def get_comment_lines(self):
		self.parse()
		return self.comment_lines
	
	def get_image(self, n):
		'''Return image object n'''
		return self.get_image_lines()[n]
	
	def get_image_by_fn(self, fn):
		for i in self.get_image_lines():
			if fn == i.get_name():
				return i
		return None
	
	def add_image(self, image_fn, calc_dim = True):
		self.parse()
		il = ImageLine('i n"%s"' % image_fn, self)
		if calc_dim:
			calc_il_dim(il)
		self.image_lines.append(il)

	def get_image_lines(self):
		self.parse()
		return self.image_lines
	
	def nimages(self):
		return len(self.get_image_lines())
	
	def get_control_point_lines(self):
		self.parse()
		return self.control_point_lines
		
	def add_control_point_line(self, cl):
		self.parse()
		if self.control_point_lines is None:
			self.control_point_lines = []
		self.control_point_lines.append(cl)
		
	def add_control_point_line_by_text(self, cl):
		self.add_control_point_line(ControlPointLine(cl, self))
		
	def add_image_line(self, il):
		self.parse()
		if self.image_lines is None:
			self.image_lines = []
		self.image_lines.append(il)
		
	def add_image_line_by_text(self, il_text):
		il = ImageLine(il_text, self)
		self.add_image_line(il)
		
	def get_optimizer_lines(self):
		self.parse()
		return self.optimizer_lines
		
	def get_panorama_line(self):
		#print 'getting p line, parsed: %d' % self.parsed
		self.parse()
		return self.panorama_line
	
	def get_variable_lines(self):
		self.parse()
		return self.variable_lines
	
	@staticmethod
	def from_file_name(file_name, is_temporary = False):
		ret = PTOProject()
		ret.file_name = file_name
		if is_temporary:
			ret.temp_file = ManagedTempFile.from_existing(file_name)
		return ret

	@staticmethod
	def parse_from_file_name(file_name, is_temporary = False):
		ret = PTOProject()
		ret.file_name = file_name
		if is_temporary:
			ret.temp_file = ManagedTempFile.from_existing(file_name)
		ret.parse()
		return ret
	
	@staticmethod
	def from_temp_file(temp_file):
		ret = PTOProject()
		ret.file_name = temp_file.file_name
		ret.temp_file = temp_file
		return ret

	@staticmethod
	def from_text(text):
		ret = PTOProject()
		if text is None:
			raise Excetpion('No text is invalid')
		ret.text = text
		#ret.reparse()
		return ret

	@staticmethod
	def from_blank():
		return PTOProject.from_text('')

	@staticmethod
	def from_simple():
		return PTOProject.from_text('''
p
m
''')
		
	@staticmethod
	def from_default():
		return PTOProject.from_text('''
p f0 v179 n"PSD_mask" E0.0 R0
m g1.0 i0 f0 m2
''')

	def parse(self):
		'''Parse if not already parsed'''
		if not self.parsed:
			self.reparse()
		# We should now be using the intermediate form
		# Force a regen if someone wants text
		self.text = None

	def reparse(self):
		'''Force a parse'''
		if False:
			print 'WARNING: pto parsing disabled'
			return

		self.panorama_line = None
		self.mode_line = None
		self.comment_lines = list()
		self.variable_lines = list()
		self.control_point_lines = list()
		self.absolute_control_point_lines = list()
		self.image_lines = list()
		self.misc_lines = list()
		self.optimizer_lines = list()

		#print self.text
		print_debug('Beginning split on text of len %d' % (len(self.get_text())))
		for line in self.get_text().split('\n'):
			print_debug('Processing line: %s' % line)
			# Single * is end of file
			# Any comments / garbage is allowed to follow
			#if line.strip() == '*':
			#	break
			# In practice this is PTOptimizer output I want
			# Add an option later if needed to override
			self.parse_line(line)
			print_debug()

		print 'Finished reparse'
		self.parsed = True

	def parse_line(self, line):
		# Ignore empty lines
		if len(line) == 0:
			return
			 
		k = line[0]
		if k == '#':
			# Ignore comments and option lines for now
			# They have position dependencies and usually can be ignored anyway for my purposes
			# They are mostly used by Hugin
			#print 'WARNING: ignoring comment line: %s' % line
			self.comment_lines.append(line)
		# EOF marker, used for PToptimizer to indicate end of original project
		elif k == '*':
			pass
		# Panorama line
		elif k == "p":
			self.panorama_line = PanoramaLine(line, self)
		# additional options
		elif k == "m":
			self.mode_line = ModeLine(line, self)
		# Image line
		elif k == "i":
			self.image_lines.append(ImageLine(line, self))
		# Optimization (variable) line
		elif k == "v":
			self.variable_lines.append(VariableLine(line, self))
		# Control point line
		elif k == "c":
			self.control_point_lines.append(ControlPointLine(line, self))
		elif k == 'C':
			self.absolute_control_point_lines.append(AbsoluteControlPointLine(line, self))
		# Generated by PToptimizer
		elif k == "o":
			self.optimizer_lines.append(OptimizerLine(line, self))
		else:
			print 'WARNING: unknown line type: %s' % line
			self.misc_lines.append(line)
	
	# These functions are fragile....should probably just stick to the get string versions
	def regen_hugin(self):
		self.set_text(self.to_str_core(False))
	
	def regen_pto(self):
		self.set_text(self.to_str_core(True))
	
	# XXX: a lot of this logic was moved out since it was more complicated than anticipated
	def to_ptoptimizer(self):
		'''Create a new, unusaved version compatible with PToptimizer'''
		'''
		FIXME: this was a hack
		Really utilities should create a new PToptimizer compatible project
		and then return the string repr if users want it
		
		
		Illegal token in 'p'-line [83] [S] [S"103,21061,28,16889"]
		'''
		return PTOProject.from_text(self.to_str_core(True))
	
	def regen(self):
		self.regen_pto()
	
	def to_str_core(self, ptoptimizer_form):
		text = ''
		text += '# Generated by pr0ntools\n'

		#print 'Pano line: %s' % self.panorama_line

		if ptoptimizer_form:
			print 'generating ptopt form'

		key_blacklist = None
		if ptoptimizer_form:
			key_blacklist = 'E R S'.split()
			pass
		text += self.panorama_line.regen(key_blacklist)

		text += self.mode_line.regen()
			
		for line in self.image_lines:
			key_blacklist = None
			if ptoptimizer_form:
				key_blacklist = 'Eb Eev Er Ra Rb Rc Rd Re Va Vb Vc Vd Vx Vy'.split()
			text += line.regen(key_blacklist)

		for line in self.variable_lines:
			text += line.regen()

		for line in self.control_point_lines:
			text += line.regen()

		for line in self.absolute_control_point_lines:
			text += line.regen()
			
		for line in self.comment_lines:
			#text += line.regen()
			text += line + '\n'

		return text

	def __str__(self):
		# Might make this diff from get_text to show parser info at some point
		return self.get_text()

	def get_text(self):
		# If parsed then convert the intermediate repr since we may have modified from the saved value
		if self.parsed:
			#print 'get_text: constructed version'
			return self.to_str_core(False)
		else:
			#print 'get_text: file/text version'
			# Not parsed?  Then just directly load from the file
			self.ensure_text_loaded()
			return self.text
		
	def ensure_text_loaded(self):
		if self.text is None:
			self.load_text()
		
	def load_text(self):
		self.text = open(self.file_name).read()
		self.parsed = False

	def make_absolute(self, to = None):
		'''Make all image paths absolute'''
		print 'Making %d images absolute' % len(self.get_image_lines())
		for i in self.get_image_lines():
			i.make_absolute(to)

	def make_relative(self, to = None):
		'''Make all image paths relative'''
		for i in self.get_image_lines():
			i.make_relative(to)
			
	def do_get_a_file_name(self, prefix = None, postfix = None):
		'''If doesn't have a real file, create a temp file'''
		if self.file_name:
			return self.file_name
		if postfix is None:
			postfix = ".pto"
		self.temp_file = ManagedTempFile.get(prefix, postfix)
		self.file_name = self.temp_file.file_name
		return self.file_name
	
	def get_a_file_name(self, prefix = None, postfix = None):
		self.do_get_a_file_name(prefix, postfix)
		self.save()
		return self.file_name

	def set_file_name(self, file_name):
		self.file_name = file_name

	def set_text(self, text):
		self.text = text
		if self.file_name:
			self.save()
		self.parsed = False

	def merge_into(self, others):
		'''Merge project into this one'''
		print 'merge_into: others: %d' % len(others)
		# Merging modifies the project structure so make sure that a dummy merge occurs if nothing else
		temp = self.merge(others)
		self.text = str(temp)
		print 'merge_into: text len: %d' % len(self.text)
		if self.file_name:
			print 'merge_into: saving'
			self.save()	

	def merge(self, others):
		'''Return a project containing both control points'''
		'''
		Does not allow in place replace, we have to move things around
		
		[mcmaster@gespenst bin]$ pto_merge --help
		pto_merge: merges several project files
		pto_merge version 2010.4.0.854952d82c8f

		Usage:  pto_merge [options] input.pto input2.pto ...

		  Options:
			 -o, --output=file.pto  Output Hugin PTO file.
									Default: <filename>_merge.pto
			 -h, --help			 Shows this help
		'''
		if len(others) == 0:
			print 'WARNING: skipping merge due to no other files'
			raise Exception('Nothing to merge')
			return None
		# Make sure that current project gets included
		# if empty we should still do this so that a merge can happen
		# as "merging" causes panotools project transforms tools may expect
		self.save()
		m = Merger(others)
		m.pto = self
		return m.run()

	def save(self):
		'''
		I considered invalidating text here but for most operations I'm doing (PToptimizer excluded)
		only I modify the project
		
		import traceback
		import sys
		sys.stdout.flush()
		sys.stderr.flush()
		traceback.print_stack()
		sys.stdout.flush()
		sys.stderr.flush()
		'''
		if self.file_name is None:
			raise Exception('Cannot save a project that was never assigned a filename')
		self.save_as(self.file_name)

	def save_as(self, file_name, is_new_filename = False):
		open(file_name, 'w').write(self.get_text())
		if is_new_filename:
			self.file_name = file_name

	# reload is a builtin...not sure if it would conflict
	def reopen(self):
		f = open(self.file_name, 'r')
		self.text = f.read()
		self.parsed = False

	def get_file_names(self):
		'''Get image file names'''
		return [i.get_name() for i in self.get_image_lines()]

	def hugin_form(self):
		'''
		This is used when merging through fortify stitch
		
		Something is causing pto_merge to hang, but NOT ptomerge
		Only occurs if I wrap my commands in a script...
		The script doesn't do any fancy I/O redirection			
			clear
			rm -rf /tmp/pr0ntools_*
			pr0nstitch *.jpg out.pto
		pto_merge produces nicer output than ptomerge
		While ptomerge produces the fields I need, it leaves some other junk
		I think pto_merge also calculates width/heigh attributes


		part of Hugin
		[mcmaster@gespenst first]$ pto_merge
		Warning: pto_merge requires at least 2 project files

		pto_merge: merges several project files
		pto_merge version 2010.4.0.854952d82c8f


		part of perl-Panotools-Script
		[mcmaster@gespenst first]$ ptomerge  --help
		cannot read-open --help at /usr/share/perl5/Panotools/Script.pm line 91.		
		man ptomerge
		...
		ptomerge infile1.pto infile2.pto infile3.pto [...] outfile.pto
		...
		'''
		
		# However, this tool also generates an archaic .pto format that pto can parse, but I don't want to
		# pretend to merge into an empty project to force Hugin to clean it up
		# pto_merge --output=temp.pto /dev/null temp.pto
		if False:
			args = list()
			args.append("%s" % self.get_a_file_name())
			args.append("%s" % self.get_a_file_name())
			args.append("%s" % self.get_a_file_name())
		
			(rc, output) = Execute.with_output("ptomerge", args)
		else:
			args = list()
			args.append("--output=%s" % self.get_a_file_name())
			args.append("%s" % self.get_a_file_name())
		
			if False:
				args.append("/dev/null")
			else:
				empty_file = ManagedTempFile.get(None, ".pto")
				open(empty_file.file_name, 'w').write('')
				args.append(empty_file.file_name)

			(rc, output) = Execute.with_output("pto_merge", args)
			
		if not rc == 0:
			print
			print
			print
			if rc == 35072:
				# ex: empty projects seem to cause this
				print 'Out of memory, expect malformed project file'
			print 'output:%s' % output
			raise Exception('Bad rc: %d' % rc)
		
		self.reopen()		

