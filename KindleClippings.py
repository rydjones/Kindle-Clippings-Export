#!/usr/bin/env python
import os, sys
sys.path.insert(0, os.path.abspath(os.getcwd() + '/parser'))

class Clippings():

	def __init__(self, filepath):
		self.filepath = filepath
		self.directory = os.path.split(filepath)[0]
		if os.path.split(filepath)[1] == 'My Clippings.txt':
			print 'File selected: \n' + filepath + '\n'
			self.notes = self.Parse(self.ReadFile())
		else:
			print "Your file could not be properly loaded.\n"
			exit
	
	
	def ReadFile(self):
		# Reads all lines out of 'My Clippings.txt'
		# Returns list of lines read
		# Called from __init__()
		
		f = open(self.filepath)
		lines = f.readlines()
		f.close()
		return lines

	
	def Parse(self, lines):
		# Parses lines from ReadFile()
		# Returns dictionary: key = title, value = list of clippings
		# Called from __init__()
		
		notes = {}			#Keys are titles, Values are lists of associated notes
		flag = 0			#Cleared in loop, when note delimiter '=======' is reached
		
		# Process lines from the file
		for line in lines:
			if line.find('===') == 0:	#Clear flag if note delimiter is detected
				flag = 0
			else:
				if flag == 0:							#Clear flag > Expect title (key) line
					flag = 1							#Set flag for next iteration
					key = line
					if not notes.has_key(key):			#Check for existence of key
						notes[key] = []					#Create new list as value for key
				else:
					if not line.find('-') == 0:			#Eliminate unnecessary data (dates, etc.)
						notes[key].append(line)			#Append line to list for that title
		return notes
	
	
	def WriteFiles(self):
		# Create new directory, write file for each key, dump lines from lists
		
		path = self.directory + '/Notes/'
		try:
			os.mkdir(path)
		except OSError:
			pass

		for title in self.notes:
			filename = path + ValidateForFilename(title) + '.txt'	#Separate directory to keep things clean
			try:
				f = open(filename,'w')
				f.writelines(self.notes[title])				#Write all lines in list for each Title (key)
				f.close()
			except IOError:									#Gracefully (more or less) escape invalid filenames, note errors for adjusting ValidateForFilename()
				print '\nError writing file for:\n' + title + '\n\n'


# Transform kindle titles to valid filenames
def ValidateForFilename(title):
	import string
	valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
	title = ''.join(c for c in title if c in valid_chars)	#eliminate invalid characters
	title = ''.join(title.split()[:5])						#Keep titles reasonable length, eliminate spaces
	return title


class Title:
	""" Holds data for one work including list of clippings """
	def __init__(self, title, author):
		self.title = title
		self.author = author
		self.clippings = []		#List of Clipping objects
		
	def __str__(self):
		return self.title + ' by ' + self.author
		
	def addClipping(self, clipping):
		self.clippings.append(clipping)
	
		
class Clipping:
	def __init__(self, type, location, date, text):
		self.type = type
		self.location = location
		self.date = date
		self.text = text
		
	def __str__():
		return self.text

if __name__ == '__main__':
	import Tkinter, tkFileDialog
	root = Tkinter.Tk()
	root.withdraw()
	file = tkFileDialog.askopenfilename(parent=root,title='Select your My Clippings.txt file')
	MyClippings = Clippings(file)
	MyClippings.WriteFiles()