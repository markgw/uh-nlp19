import spacy
from spacy.matcher import Matcher   

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


if __name__ == "__main__":

	sentences = [
	"Waxman Industries Inc. said holders of $6,542,000 face amount of its 6 1/4% convertible subordinated debentures, due March 15, 2007, have elected to convert the debt into about 683,000 common shares.",
	"Seventy-five million copies of the rifle have been built since it entered production in February 1947, making it history's most widely distributed weapon.",
	"Many of the local religious leaders who led the 1992 protests have moved."
	]
	
	month_regex = r'(January|February|March|April|May|June|July|August|September|October|November|December)'
	month = {"TEXT": {"REGEX": month_regex}}
	year = {"SHAPE": "dddd", "<=":"2019"}
	day = {"SHAPE": "dd", ">":"0", "<=":"31"}
	date =[{**month, 'OP':'?'}, {**day, 'OP':'?'},{'IS_PUNCT': True, 'OP': '?'}, {**year}]
	
	matcher.add("TIMEX", None, date)
	
	for s in sentences:
	    doc = nlp(s)
	    matches = matcher(doc)
	    print(markup_timex(doc, matches))
	    
	        

