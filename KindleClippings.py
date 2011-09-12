#!/usr/bin/env python
import os 
import sys
import string
import optparse
import Tkinter 
import tkFileDialog
from parser.kindleclippingsparser import KindleClippingsParser

def main():
    # Setup options parser
    parser = optparse.OptionParser(description="This will eventually hold argument parsing for Kindle Clippings Exporter")
    parser.add_option("-i", "--infile", action="store", default="", type="string", dest="infile", help="Path to My Clippings.txt. Dialog asks for location if none is provided.")
    parser.add_option("-o", "--outdir", action="store", default=os.getcwd(), type="string", dest="outdir", help="Directory location for output. Assumes current working directory if none is provided.")
    parser.add_option("-v", "--verbose", action="store_true", default=False,dest="verbose", help="Include metadata (type, location, date, and time) for clippingsin output. Only clipping text is included otherwise.")
    parser.add_option("-f", "--format", action="store", default="text", dest="format", help="Valid options: text. More options coming soon.")
    #parser.add_option("-s", "--search", action="store", default="", dest="query", help="Search query to match a title. Will only output clippings for single matching title.")
    options, args = parser.parse_args()

    options.infile = ValidateOption_infile(options.infile)
    options.outdir = ValidateOption_outdir(options.outdir)

    #Perform export
    myclippings = MyClippings(options.infile)
    
    if options.format == "text":
        for title in myclippings.titles:
            work = myclippings.titles[title]
            work.toTxt(options.outdir, options.verbose)
    elif options.format == "html":
        print "This hasn't been implemented yet silly!"
        exit
    else:
        raise optParse.OptionError("is not a valid output format", options.format)


def ValidateOption_infile(infile):
    if not infile:
        root = Tkinter.Tk()
        root.withdraw()
        infile = tkFileDialog.askopenfilename(parent=root,title='Select your My Clippings.txt file')
    else:
        infile = os.path.expanduser(infile)
        if not os.path.exists(infile):
            raise optparse.OptionError("File does not exist", infile)
    
    if not os.path.split(infile)[1]=="My Clippings.txt":
            raise optparse.OptionError("does not point to a My Clippings.txt file", infile)
    #print 'INFILE: ' + options.infile + '\n'
    return infile


def ValidateOption_outdir(outdir):
    outdir = os.path.expanduser(outdir)
    outdir += '/Clippings/'
    try:
        os.mkdir(outdir)
    except OSError:
        pass
    #print 'OUTDIR: ' + options.outdir + '\n'
    return outdir


class MyClippings():
    """ 
    Container for all data within My Clippings.txt file
    Attributes: filepath, directory, titles(dictionary)
    One-to-Many relationship with Titles class
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.directory = os.path.split(filepath)[0]
        try:
            self.titles = self.Parse(self.ReadFile())
        except IOError:
            print "Your file could not be properly loaded.\n"
            exit
    
    
    def ReadFile(self):
        """
        Reads all lines out of 'My Clippings.txt'
        Returns parser object
        Called from __init__()
        """

        parser = KindleClippingsParser(open(self.filepath,'r'))
        return parser

    
    def Parse(self, parser):
        """
        Parses lines from ReadFile()
        Returns dictionary (key=title, value=Title object)
        Called from __init__()
        """

        titles = {}
        clippings = parser.parse()
        for clipping in clippings:
            title = clipping['title']
            if not title in titles:
                titles[title] = Title(title, clipping['author']) 
            
            titles[title].addClipping(Clipping(clipping['type'], clipping['location'], 
                                               clipping['date'], clipping['text']))
        return titles
    

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
        self.clippings = []
        
    def __str__(self):
        return self.title + ' by ' + self.author
        
    def addClipping(self, clipping):
        self.clippings.append(clipping)

    def toTxt(self, outdir, verbose):
        """
        outdir: location (directory) of text file output, default is current working directory.
        verbose: boolean value. If true, prints clipping type, location, date/time. Default is false.
        """

        filename = outdir + ValidateForFilename(self.title) + '.txt'
        try:
            f = open(filename,'w')
            titleline = u'Title: ' + self.title + u'\n'
            authorline = u'Author/Source: ' + self.author + u'\n\n'
            f.write(titleline.encode('utf-8'))
            f.write(authorline.encode('utf-8'))
            for clipping in self.clippings:
                clippingtext = u''
                if verbose:
                    clippingtext += clipping.type + u' | ' + clipping.location + u' | ' + str(clipping.date) + u'\n'
                clippingtext += clipping.text + u'\n\n'
                try:
                    f.write(clippingtext.encode('utf8'))
                except UnicodeEncodeError:
                    pass
            f.close()
        except IOError:
            print '\nError writing file for:\n' + self.title + '\n\n'
    
        
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


def ValidateForFilename(title):
    """
    Transform kindle titles (or any string) to valid filenames
    title: a string to be used as a filename
    """

    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    title = ''.join(c for c in title if c in valid_chars)       #eliminate invalid characters
    title = ''.join(title.split()[:5])                          #Keep titles reasonable length
    return title
            

if __name__ == '__main__':
    main()