from linecache import getline
import re
from . import util

def convert(mdfile):

    file = util.get_entry(mdfile)
    file = file.splitlines(True)
    headingSize = re.compile('^[#]+')
    checkLineContent = re.compile('.')
    findHeadings = re.compile('^[#]+\s*(.*)') #group 1 returns heading Text
    findBoldedText = re.compile('\*\*\s*(.*)\s*\*\*') #group 1 returns bolded Text
    getLinks = re.compile('\[(.*)\]\(([^()]*)\)') #group 1 returns text, group 3 returns link
   
    convertedFile = ''
    startedParagraph = False
    print(file)
    for i in file:
        convertedLine = i.strip()
        if i == '\r\n':
            if startedParagraph:
                convertedFile += '</p>'
                startedParagraph = False
        else:
            #check for headings
            match = findHeadings.match(i)
            if match:
                headerText = match.group(1).strip()
                size = headingSize.match(i).end()
                if size > 6:
                    size = 6
                #Custom Styling for my own conversions
                convertedLine = (f'<h{size} style="color: #320A28;">' + headerText + f'</h{size}>')
              
            elif not startedParagraph and checkLineContent.match(i.strip()):
                #if not a heading start paragraph
                startedParagraph = True
                convertedLine = '<p style="color: #36413E;">' + convertedLine

            findbold = findBoldedText.search(convertedLine)
            if findbold:
                boldedText = findbold.group(1).strip()
                convertedLine = findBoldedText.sub(f'<strong style="color: #8E443D;">{boldedText}</strong>',convertedLine)

            findlink = getLinks.search(convertedLine)
            if findlink:
                textclick = findlink.group(1).strip()
                linkref = findlink.group(2).strip()
                convertedLine = getLinks.sub(f'<a style="color: #87D68D;" href="{linkref}">{textclick}</a>',convertedLine)
            convertedFile += convertedLine            
    convertedFile += '</p>'
    print(convertedFile)
    return(convertedFile)

def cleanLines(file):
    #When the markdown files save, it adds carraige returns after every line
    #Every time you reload to edit, the gaps get bigger and bigger. So this function undoes that
    newLines = file.splitlines(True)
    print(newLines)
    newFile =''
    for i in newLines:
        if (i == '\n') or (i == "\r\n") or (i == '\r'):
            pass
        else:
            i+= '\n' + '\n'
            newFile += i
    return newFile
