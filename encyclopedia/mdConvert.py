import re

def convert(mdfile):
    p = re.compile('^[#]+', re.MULTILINE)
    p2 = re.compile('(\n)\s*\n*',re.MULTILINE)
    p3 = re.compile('^[#]+\s*((.*)*)', re.MULTILINE) #group 1 returns heading Text
    p4 = re.compile('\*\*\s*((.*)*)\s*\*\*', re.MULTILINE) #group 1 returns bolded Text
    p5 = re.compile('\[((.*)*)\]\(((.*)*)\)') #group 1 returns text, group 3 returns link
    t1 = "Test String 1"
    t2 = "# Test String 2"
    t3 = "### Test String 3"
    t4 = "### Test String 4 ###"
    t5 = "Testing Paragraph '\n''\n'"
    t6 = "Testing Broken Paragraph \n \n Splitted string"
    t7 = "Testing ** Bolded** things"
    t9 = "testing link [GitHub stuff](https:/github.com)"
    print(p.search(t1))
    print(p.search(t2))
    print(p.search(t3))
    print(p.search(t4))
    print(p.search(t5))
    print(p.search(t6))
    print(p2.search(t1))
    print(p2.search(t2))
    print(p2.search(t3))
    print(p2.search(t4))
    print(p2.search(t5))
    print(p2.search(t6))
    print('------------')
    print(p3.search(t3))
    m = p3.search(t3)
    if m:
        print(m.group(1))

    print(p4.search(t7))
    tes = p4.search(t7)
    if tes:
        print(tes.group(1))

    print(p5.search(t9))
    tes2 = p5.search(t9)
    if tes2:
        print(tes2.group(1))
        print(tes2.group(3))

    t8 = t6.splitlines(True)
    print(t8)

    matchObj = p.match(t3)
    if matchObj:
        headingSize = matchObj.end()
        if headingSize > 6:
            headingSize = 6

    convertedStr = (f"<h{headingSize}>")
