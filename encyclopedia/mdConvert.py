from linecache import getline
import re
from . import util

def cleanLines(file):
    #When the markdown files save, it adds carraige returns after every line
    #Every time you reload to edit, the gaps get bigger and bigger. So this function undoes that
    newLines = file.splitlines(True)
    print(newLines)
    newFile =''
    for i in newLines:
        if i != '\r\n':  
            newFile += i
            
        
    return newFile

def convert(mdfile):

    file = cleanLines(util.get_entry(mdfile))
    file = file.splitlines(True)
    headingSize = re.compile('^[#]+')
    findUnorderedList = re.compile('\*([^\*].*)') #unordered list
    findHeadings = re.compile('^[#]+\s*(.*)') #group 1 returns heading Text
    findBoldedText = re.compile('\*\*(.*?)\*\*') #group 1 returns bolded Text
    getLinks = re.compile('\[([^\[\]]*)\]\(([^()]*)\)') #group 1 returns text, group 3 returns link
   
    convertedFile = ''
    startedParagraph = False
    startedUnorderList = False
    for i in file:
        convertedLine = i.strip()
        if i =='\r':
            #if there is an empty line, end existing paragraphs/list
            if startedParagraph:
                convertedFile += '</p>'
                startedParagraph = False
            if startedUnorderList:
                convertedFile += '</ul>'
                startedUnorderList = False

        #check now lines that have content
        else:
            #check for headings
            match = findHeadings.match(i)
            if match:
                headerText = match.group(1).strip()
                size = headingSize.match(i).end()
                if size > 6:
                    size = 6
                #Custom Styling for my own conversions
                convertedLine = (f'<h{size} style="color: #320A28;font-family: Monospace;">' + headerText + f'</h{size}>')
                #if heading has started, then paragraph/list has ended
                if startedParagraph:
                    convertedFile += '</p>'
                    startedParagraph = False
                if startedUnorderList:
                    convertedFile += '</ul>'
                    startedUnorderList = False
            
            elif not startedParagraph and not findUnorderedList.match(i.strip()):
                #if not a heading or ulist start paragraph
                startedParagraph = True
                #end the list if we were on one
                if startedUnorderList:
                    convertedLine += '</ul>'
                    startedUnorderList = False
                convertedLine = '<p style="color: purple; font-family: Monospace;">' + convertedLine

            #lists only are checked at the start of line, so if its a header it won't be called
            #And as seen above paragraphs are only made when there isn't a match for a list
            finduolist = findUnorderedList.match(i.strip())
            if finduolist:
                #start the list if not already in one
                if not startedUnorderList:
                    convertedLine = '<ul style="font-family: Monospace;"><li>' + finduolist.group(1) +'</li>'
                    startedUnorderList = True
                else:
                    convertedLine = '<li>' + finduolist.group(1) + '</li>'
            #bold is checked for on every occasion
            findbold = findBoldedText.search(convertedLine)
            if findbold:
                for i in findBoldedText.finditer(convertedLine):
                    print(i)
                    print(i.group(1))
                    boldedText = i.group(1).strip()
                    convertedLine = findBoldedText.sub(f'<strong style="color: #8E443D;">{boldedText}</strong>',convertedLine,1)

            #links are checked for on every occasion
            findlink = getLinks.search(convertedLine)
            if findlink:
                for i in getLinks.finditer(convertedLine):
                    textclick = i.group(1).strip()
                    linkref = i.group(2).strip()
                    convertedLine = getLinks.sub(f'<a style="color: #87D68D;" href="{linkref}">{textclick}</a>',convertedLine,1)

            #space added to the back of strings in paragraphs    
            if startedParagraph:
                convertedLine += '\r'
            convertedFile += convertedLine
        convertedFile+='\n'
    #if file ends while in paragraph or list close it
    if startedParagraph:         
        convertedFile += '</p>'
    if startedUnorderList:         
        convertedFile += '</ul>'
    #print(convertedFile) enable or view page source
    return(convertedFile)

