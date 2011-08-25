import os

# Reads all lines out of 'My Clippings.txt' taken off of Kindle
def Read():
	f = open('My Clippings.txt')
	lines = f.readlines()
	f.close()
	return lines


# Process lines, generate dict keys, associate lists of lines
def Sift(lines):
	notes = {}			#Keys are titles, Values are lists of associated notes
	flag = 0			#Cleared in loop, when note delimiter '=======' is reached
	
	# Process lines from the file
	for line in lines:
		if line.find('===') == 0:	#Clear flag if note delimiter is detected
			flag = 0
		else:
			if flag == 0:							#Clear flag > Expect title (key) line
				flag = 1							#Set flag for next iteration
				key = ''.join(line.split()[:5])		#Keep titles reasonable length, eliminate spaces
				if not notes.has_key(key):			#Check for existence of key
					notes[key] = []					#Create new list as value for key
			else:
				if not line.find('-') == 0:			#Eliminate unnecessary data (dates, etc.)
					notes[key].append(line)			#Append line to list for that title
	return notes


# Create new directory, write file for each key, dump lines from lists
def WriteFiles(notes):
	if not os.path.isdir('Notes'):
		os.mkdir('Notes')
		
	for title in notes:
		filename = 'Notes/' + title + '.txt'		#Separate directory to keep things clean
		try:
			f = open(filename,'w')
			f.writelines(notes[title])				#Write all lines in list for each Title (key)
			f.close()
		except IOError:								#Gracefully (more or less) escape invalid filenames
			print '\nError writing file for:\n' + title + '\n\n'
		

if __name__ == '__main__':
	WriteFiles(Sift(Read()))