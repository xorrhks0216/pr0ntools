'''
pr0ntools
Copyright 2011 John McMaster <JohnDMcMaster@gmail.com>
Licensed under a 2 clause BSD license, see COPYING for details
'''
from pr0ntools.temp_file import ManagedTempFile
from pr0ntools.temp_file import ManagedTempDir
from pr0ntools.execute import Execute
from pr0ntools.stitch.pto.project import PTOProject
from pr0ntools.stitch.pto.util import *
import shutil
import os.path

# clear; rm -f /tmp/*.pto /tmp/*.jpg; pr0nstitch --result=out.jpg *.jpg

"""
class ControlPointGenerator:
	@staticmethod
	def from_string():
		pass

	@staticmethod
	def from_id():
		pass
		
	def generate_core(image_file_names):
		'''
		Input should be a list of either 
		Returns a PTOProject
		'''
		pass

	def generate_by_name(image_file_names):
		'''Takes in a list of image file names'''
		return generate_core(imageFileNames)

	def generate_by_PIL(images):
		'''Takes in a list of TempFilePIL images'''
		return generateControlPointsCore(imageFiles)

class AutopanoAj(ControlPointGenerator):
	os.system("autopanoaj /allinone /project:hugin '/ransac_dist:1.0'")
	os.system("cat %s |sed 's@%s@%s@g' >/tmp/%s" % (project_file, original_dir, image_dir, temp_project_file))
"""

#class ControlPointGenerator:	
class AutopanoSiftC:
	'''
	Example stitch command
	"autopano-sift-c" "--maxmatches" "0" "--maxdim" "10000" "out.pto" "first.png" "second.png"
	'''
	def generate_core(self, image_file_names):
		project_file = ManagedTempFile.get(None, ".pto")

		command = "autopano-sift-c"
		args = list()
		
		# Try to post process them to make them more accurate
		#args.append("--refine")
		
		# Perform RANSAC to try to get bad control points out
		#args.append("--ransac")
		#args.append("on")

		# Unlimited matches
		args.append("--maxmatches")
		args.append("0")
		
		# ?
		#args.append("--maxdim")
		#args.append("10000")

		# Project file
		args.append(project_file.file_name)
		
		# Images
		for image_file_name in image_file_names:
			 args.append(image_file_name)

		# go go go
		(rc, output) = Execute.with_output(command, args)
		if not rc == 0:
			print
			print
			print
			print 'output:\n%s' % output

			raise Exception('Bad rc: %d' % rc)
		
		# We return PTO object, not string
		return PTOProject.from_temp_file(project_file)


#class AutopanoAJ : ControlPointGenerator:	
class ControlPointGenerator:
	'''
	autopano.exe /f /tmp/file1.jpg /tmp/file2.jpg /project:hugin 
	Example stitch command
	Will result in .pto in being in /tmp though
	
	Eh its pretty unreliable (wine issue?) if we don't put pix in current dir
	Easiest way to accomplish this without copying is to create temp dir and symlink
	we are editing the files anyway, so not a big deal
	'''
	def generate_core(self, image_file_names):
		command = "autopanoaj"
		args = list()
		final_project_file = ManagedTempFile.get(None, ".pto")
		temp_dir = ManagedTempDir.get()
		
		# default is .oto
		args.append("/project:hugin")
		# Use image args instead of dir
		
		# Images
		image_links = dict()
		for image_file_name in image_file_names:
			# args.append(image_file_name.replace("/tmp/", "Z:\\tmp\\"))
			image_file_name = os.path.realpath(image_file_name)

			link_file_name = os.path.join(temp_dir.file_name, os.path.basename(image_file_name))
			print 'Linking %s -> %s' % (link_file_name, image_file_name)
			os.symlink(image_file_name, link_file_name)

		#sys.exit(1)
		# go go go
		(rc, output) = Execute.with_output(command, args, temp_dir.file_name)
		print 'Finished control point pair execution'
		if not rc == 0:
			print
			print
			print
			print 'output:\n%s' % output

			if output.find('This application has requested the Runtime to terminate it in an unusual way'):
				print 'WARNING: skipping crash'
				return None
			
			raise Exception('Bad rc: %d' % rc)
		
		'''
		Doesn't like the match:
		PICTURE PAIRS VALIDATION 
		  Pair (  0,  1)
			Ransac (In : 21, Out : 4, Residu : 4.43799)
			REMOVED
		  Timing : 583.7 us
		'''
		if output.find('REMOVED') >= 0:
			print 'WARNING: RANSAC invalidated control points'
			return None
		
		output_file_name = os.path.join(temp_dir.file_name, "panorama0.pto")
		
		# This happens occassionally, not sure why
		if not os.path.exists(output_file_name):
			print 'WARNING: missing output pto file!'
			return None
		
		# We return PTO object, not string
		# Ditch the gen file because its unreliable
		shutil.move(output_file_name, final_project_file.file_name)
		f = open(final_project_file.file_name, 'r')
		project_text = f.read()
		# Under WINE, do fixup
		# #-imgfile 2816 704 "Z:\tmp\pr0ntools_471477ADA1679A2E\pr0ntools_3CD1C0B1BB218E40.jpg"
		project_text = project_text.replace('Z:\\', '/').replace('\\', '/')
		for image_file_name in image_file_names:
			link_file_name = os.path.join(temp_dir.file_name, os.path.basename(image_file_name))
			print 'Replacing %s -> %s' % (link_file_name, image_file_name)
			project_text = project_text.replace(link_file_name, image_file_name)

		if False:
			print
			print 'Raw control point project (after symbolic link and WINE file name substitution)'
			print
			print
			print project_text
			print
			print
			print
		#sys.exit(1)
		f.close()
		f = open(final_project_file.file_name, 'w')
		f.write(project_text)
		project = PTOProject.from_temp_file(final_project_file)
		return project
		
		

# This might be removed soon as I'm not sure it does much
# or at least the problem it solved could now be solved simpler now that I have a PTO object
def ajpto2pto_text(pto_str, sub_image_0_file, sub_image_1_file, sub_image_0_x_delta, sub_image_0_y_delta, sub_to_real, load_images = True):
	'''Take in an old style autopanoaj project and return a .pto object'''

	# image index to subimage file name link (not symbolic link)
	index_to_sub_file_name = dict()
	imgfile_index = 0
	part_pair_index = 0
	
	ret = PTOProject.from_simple()
	
	#out = ''
	
	'''Convert .oto text (like from autopanoaj) to a .pto'''
	# Actually I think really is a .pto, just in a less common format
	for line in pto_str.split('\n'):
		if len(line) == 0:
			continue
		# This type of line is gen by autopano-sift-c
		elif line[0] == 'c':
			# c n0 N1 x1142.261719 y245.074757 X699.189408 Y426.042661 t0
		
			'''
			Okay def alphabetical issues
			# Not strictly related to this code, but close enough
			if not index_to_sub_file_name[0] == sub_image_0_file:
				print '0 index indicated file: %s, pair gen order expected %s' % (index_to_sub_file_name[0], sub_image_0_file)
				raise Exception('mismatch')
			if not index_to_sub_file_name[1] == sub_image_1_file:
				print '1 index indicated file: %s, pair gen order expected %s' % (index_to_sub_file_name[1], sub_image_1_file)
				raise Exception('mismatch')
			'''
		
			# Parse
			parts = line.split()
			if not parts[1] == 'n0':
				print parts[1]
				raise Exception('mismatch')
			if not parts[2] == 'N1':
				print parts[2]
				raise Exception('mismatch')
			
			x = float(parts[3][1:])								
			y = float(parts[4][1:])
			X = float(parts[5][1:])
			Y = float(parts[6][1:])

			#sub_image_1_x_end = image_1.width()
			#sub_image_1_y_end = image_1.height()

			# Adjust the image towards the upper left hand corner
			if index_to_sub_file_name[0] == sub_image_0_file.file_name:
				# normal adjustment
				x += sub_image_0_x_delta
				y += sub_image_0_y_delta
			elif index_to_sub_file_name[1] == sub_image_0_file.file_name:
				# they got flipped
				X += sub_image_0_x_delta
				Y += sub_image_0_y_delta
			else:
				print index_to_sub_file_name
				print 'index_to_sub_file_name[0]: %s' % repr(index_to_sub_file_name[0])
				print 'index_to_sub_file_name[1]: %s' % repr(index_to_sub_file_name[1])
				print 'sub_image_0_file: %s' % repr(sub_image_0_file)
				print 'sub_image_1_file: %s' % repr(sub_image_1_file)
				raise Exception("confused")

			# Write
			new_line = "c n0 N1 x%f y%f X%f Y%f t0" % (x, y, X, Y)
			#out += new_line + '\n'
			ret.add_control_point_line_by_text(new_line)
		# This type of line is generated by pto_merge
		elif line[0] == 'o':
			'''
			#-imgfile 1632 408 "/tmp/pr0ntools_6691335AD228382E.jpg"
			o f0 y+0.000000 r+0.000000 p+0.000000 u20 d0.000000 e0.000000 v70.000000 a0.000000 b0.000000 c0.000000
			to
			i w2816 h704 f0 a0 b-0.01 c0 d0 e0 p0 r0 v180 y0  u10 n"/tmp/pr0ntools_6691335AD228382E.jpg"
			'''
			new_line = ''
			new_line += 'i'
			# Deferred to end
			if 0:
				# panotools fails in very exciting ways if you don't set this
				new_line += ' w%d' % images[0].width()
				new_line += ' w%d' % images[0].height()
			# default FOV
			new_line += ' v51'
			
			orig_fn = index_to_sub_file_name[part_pair_index]
			new_fn = sub_to_real[orig_fn]
			print 'Replacing %s => %s' % (orig_fn, new_fn)
			new_line += ' n"%s"' % new_fn
			
			part_pair_index += 1
			print 'new line: %s' % new_line
			ret.add_image_line_by_text(new_line)
		# These lines are generated by autopanoaj
		# The comment line is literally part of the file format, some sort of bizarre encoding
		# #-imgfile 2816 704 "/tmp/pr0ntools_2D24DE9F6CC513E0/pr0ntools_6575AA69EA66B3C3.jpg"
		# o f0 y+0.000000 r+0.000000 p+0.000000 u20 d0.000000 e0.000000 v70.000000 a0.000000 b0.000000 c0.000000
		elif line.find('#-imgfile') == 0:
			# Replace pseudo file names with real ones
			new_line = line
			index_to_sub_file_name[imgfile_index] = line.split('"')[1]
			imgfile_index += 1
		elif line.find('#') == 0:
			pass
		else:
			#new_line = line
			print 'WARNING: discarding unknown line %s' % line
		#out += new_line + '\n'
	#else:
		#out += line + '\n'

	#ret = PTOProject.from_text(out)
	
	if load_images:
		print 'Fixing up image lines'
		fixup_image_dim(ret)
	
	return ret





class ControlPointGeneratorXX:
	'''
	autopano.exe /f /tmp/file1.jpg /tmp/file2.jpg /project:hugin 
	Example stitch command
	Will result in .pto in being in /tmp though
	'''
	def generate_core(self, image_file_names):
		command = "autopanoaj"
		args = list()
		project_file = ManagedTempFile.get(None, ".pto")
		
		# default is .oto
		args.append("/project:hugin")
		# Use image args instead of dir
		args.append("/f");
		args.append('/path:Z:\\tmp')
		
		# Images
		for image_file_name in image_file_names:
			 args.append(image_file_name.replace("/tmp/", "Z:\\tmp\\"))

		# go go go
		(rc, output) = Execute.with_output(command, args)
		if not rc == 0:
			raise Exception('Bad rc: %d' % rc)
		
		# We return PTO object, not string
		# Ditch the gen file because its unreliable
		shutil.move("/tmp/panorama0.pto", project_file.file_name)
		f = open(project_file.file_name, 'r')
		project_text = f.read()
		# Under WINE, do fixup
		project_text = project_text.replace('Z:\\tmp\\', '/tmp/')
		print
		print
		print
		print project_text
		print
		print
		print
		#sys.exit(1)
		f.close()
		f = open(project_file.file_name, 'w')
		f.write(project_text)
		return PTOProject.from_temp_file(project_file)

