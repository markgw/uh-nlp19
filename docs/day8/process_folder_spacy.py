import spacy
from spacy.matcher import Matcher   

import re 
import os, sys

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

def remove_overlapping_matches(matches):
    remove = []
    for m1 in range(len(matches)-1):
        if m1 in remove:
            continue
        for m2 in range(m1+1, len(matches)):
            if m2 in remove:
                continue
            _, s1, e1 = matches[m1]
            _, s2, e2 = matches[m2]
            if s1 >= s2 and e1 <= e2:
                remove.append(m1)
                break
            if s2 >= s1 and e2 <= e1:
                remove.append(m2)
                continue

    return [matches[m] for m in range(len(matches)) if m not in remove]

def markup_timex(doc, matches):
    matches = remove_overlapping_matches(matches)
    out = ""
    prev = 0
    for _, start, end in matches:
        out += str(doc[prev:start])+'<TIMEX>'+str(doc[start:end])+'</TIMEX>'
        prev = end
    out += str(doc[prev:])
    return out

input_dir = sys.argv[1]
input_dir = os.path.abspath(input_dir)
output_dir = os.path.join(input_dir, "../sub2")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

month_regex = '(January|February|March|April|May|June|July|August|September|October|November|December)'
month = {"TEXT": {"REGEX": month_regex}}
year = {"SHAPE": "dddd", "<=":"2019"}
day = {"SHAPE": "dd", ">":"0", "<=":"31"}
date =[{**month, 'OP':'?'}, {**day, 'OP':'?'},{'IS_PUNCT': True, 'OP': '?'}, {**year}]
	
matcher.add("TIMEX", None, date)

# YOUR CODE GOES HERE
# don't forget to add you patterns into the matcher
# each pattern should be added by matcher.add() command

    
for d in os.listdir(input_dir):
    with open (os.path.join(input_dir,d), 'r') as inp:
        text = inp.read()

    with open (os.path.join(output_dir,d.replace('raw', 'sub')), 'w') as out:
        doc = nlp(text)
        matches = matcher(doc)
        out.write(markup_timex(doc, matches))
