import re 
import os, sys

input_dir = sys.argv[1]
input_dir = os.path.abspath(input_dir)
output_dir = os.path.join(input_dir, "../sub")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

months = '(January|February|March|April|May|June|July|August|September|October|November|December)'
date = '((%s\s+)?(\d{1,2},?\s+)?\d{4})' %months
timex = '(%s|%s)' %(date, months)

for d in os.listdir(input_dir):
    with open (os.path.join(input_dir,d), 'r') as inp:
        text = inp.read()

    with open (os.path.join(output_dir,d.replace('raw', 'sub')), 'w') as out:
        out.write(re.sub(timex, r'<TIMEX>\1</TIMEX>', text))
