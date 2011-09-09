#!/usr/bin/env python
import os 
import sys
import string
import codecs
sys.path.insert(0, os.path.abspath(os.getcwd() + '/parser'))
from kindleclippingsparser import KindleClippingsParser

class MyClippings():
    """ 
    Container for all data within My Clippings.txt file
    Attributes: filepath, directory, titles(dictionary)
    One-to-Many relationship with Titles class
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.directory = os.path.split(filepath)[0]
        if os.path.split(filepath)[1] == 'My Clippings.txt':
            print 'File selected: \n' + filepath + '\n'
            self.titles = self.Parse(self.ReadFile())
        else:
            print "Your file could not be properly loaded.\n"
            exit
    
    
    def ReadFile(self):
        # Reads all lines out of 'My Clippings.txt'
        # Returns parser object
        # Called from __init__()
        
        parser = KindleClippingsParser(open(self.filepath,'r'))
        return parser

    
    def Parse(self, parser):
        # Parses lines from ReadFile()
        # Returns dictionary (key=title, value=Title object)
        # Called from __init__()
        
        titles = {}
        clippings = parser.parse()
        for clipping in clippings:
            title = clipping['title']
            if not title in titles:
                titles[title] = Title(title, clipping['author']) 
            
            titles[title].addClipping(Clipping(clipping['type'], clipping['location'], 
                                               clipping['date'], clipping['text']))
        return titles
    
    
    def WriteFiles(self):
        # Create new directory, write file for each key, dump lines from lists
        
        path = self.directory + '/Notes/'
        try:
            os.mkdir(path)
        except OSError:
            pass

        for key in self.titles:
            work = self.titles[key]
            title = work.title
            filename = path + ValidateForFilename(title) + '.txt'  #Separate directory to keep things clean
            try:
                f = open(filename,'w')
                titleline = u'Title: ' + work.title + u'\n'
                authorline = u'Author/Source: ' + work.author + u'\n\n'
                f.write(titleline.encode('utf-8'))
                f.write(authorline.encode('utf-8'))
                for clipping in work.clippings:
                    try:
                        clippingtext = clipping.type + ' from ' + str(clipping.date) + '\n' + clipping.text + u'\n\n'
                        f.write(clippingtext.encode('utf8'))
                    except UnicodeEncodeError:
                        pass
                f.close()
            except IOError:
                print '\nError writing file for:\n' + title + '\n\n'


def ValidateForFilename(title):
    # Transform kindle titles to valid filenames

    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    title = ''.join(c for c in title if c in valid_chars)       #eliminate invalid characters
    title = ''.join(title.split()[:5])                          #Keep titles reasonable length
    return title


class Title:
    """ 
    Container for one work including list of clippings
    Attributes: title, author, clippings[list]
    One-to-Many relationship with Clipping class
    Many-to-One relationship with Clippings class
    """
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.clippings = []        #List of Clipping objects
        
    def __str__(self):
        return self.title + ' by ' + self.author
        
    def addClipping(self, clipping):
        self.clippings.append(clipping)
    
        
class Clipping:
    """ 
    Container for one clipping
    Attributes: type, location, date, text
    Many-to-One relationship with Title class 
    """
    def __init__(self, type, location, date, text):
        self.type = type
        self.location = location
        self.date = date
        self.text = text
        
    def __str__(self):
        return self.text


if __name__ == '__main__':
    import Tkinter, tkFileDialog
    root = Tkinter.Tk()
    root.withdraw()
    file = tkFileDialog.askopenfilename(parent=root,title='Select your My Clippings.txt file')
    myclippings = MyClippings(file)
    myclippings.WriteFiles()
