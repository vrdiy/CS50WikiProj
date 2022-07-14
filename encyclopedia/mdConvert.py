import re

def convert(mdfile):
    p = re.compile('^[#]+', re.MULTILINE)
    p2 = re.compile('//n//n',re.MULTILINE)
    t1 = "Test String 1"
    t2 = "# Test String 2"
    t3 = "### Test String 3"
    t4 = "### Test String 4 ###"
    t5 = "Testing Paragraph '/n''/n'"
    t6 = "Testing Broken Paragraph /n /n"
    print(p.search(t1))
    print(p.search(t2))
    print(p.search(t3))
    print(p.search(t4))
    print(p.search(t5))
    print(p.search(t6))
