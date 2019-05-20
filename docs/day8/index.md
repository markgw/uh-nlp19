# Day 8: Temporal Information Extraction

Carry out all the exercises below and submit your answers
[on Moodle](https://moodle.helsinki.fi/course/view.php?id=33565#section-8).
Also submit an archive containing all your code and scorer outputs. Give the files meaningful names.

----

Temporal Information Extraction is finding temporal expressions in a natural language text. "Monday", "last summer", "next year", "May 29, 2019", "today" are all examples of temporal expressions.

## Exercise 1: Temporal IE with regural expressions

This is an example code that uses a regular expression to find temporal expressions in the given sentences.

````python
import re

sentences = [
"Waxman Industries Inc. said holders of $6,542,000 face amount of its 6 1/4% convertible subordinated debentures, due March 15, 2007, have elected to convert the debt into about 683,000 common shares.",
"Seventy-five million copies of the rifle have been built since it entered production in February 1947, making it history's most widely distributed weapon.",
"Many of the local religious leaders who led the 1992 protests have moved."
]

months = '(January|February|March|April|May|June|July|August|September|October|November|December)'
timex = r'((%s\s+)?(\d{1,2},?\s+)?\d{4})' % months

for s in sentences:
    print (re.sub(timex, r'<TIMEX>\1</TIMEX>', s))
````

The output is the same sentences with temporal expressions marked up with `<TIMEX>` tag:
````
Waxman Industries Inc. said holders of $6,542,000 face amount of its 6 1/4% convertible subordinated debentures, due <TIMEX>March 15, 2007</TIMEX>, have elected to convert the debt into about 683,000 common shares.
Seventy-five million copies of the rifle have been built since it entered production in <TIMEX>February 1947</TIMEX>, making it history's most widely distributed weapon.
Many of the local religious leaders who led the <TIMEX>1992</TIMEX> protests have moved.
````


### Exercise 1.1

* Write regular expressions that would capture temporal expressions in
the following sentences.

````
The company said it expects to release third-quarter results in mid-November.

The thrift announced the plan Aug. 21.

The split and quarterly dividend will be payable Jan. 3 to stock of record Nov. 16, the company said.

Ogden Projects, whose shares began trading on the New York Stock Exchange in August, closed yesterday at $26.875, down 75 cents.

A spokeswoman for Crum amp Forster said employees were told early this week that numerous staff functions for the personal insurance lines were going to be centralized as a cost-cutting move.

For the quarter ended Sept. 30, Delta posted net income of $133.1 million, or $2.53 a share, up from $100 million, or $2.03 a share, a year earlier.
````

This is an output that should be produced:

````
The company said it expects to release third-quarter results in <TIMEX>mid-November</TIMEX>.

The thrift announced the plan <TIMEX>Aug. 21</TIMEX>.

The split and quarterly dividend will be payable <TIMEX>Jan. 3</TIMEX> to stock of record <TIMEX>Nov. 16</TIMEX>, the company said.

Ogden Projects, whose shares began trading on the New York Stock Exchange in <TIMEX>August</TIMEX>, closed <TIMEX>yesterday</TIMEX> at $26.875, down 75 cents.

A spokeswoman for Crum amp Forster said employees were told <TIMEX>early this week</TIMEX> that numerous staff functions for the personal insurance lines were going to be centralized as a cost-cutting move.

For <TIMEX>the quarter</TIMEX> ended <TIMEX>Sept. 30</TIMEX>, Delta posted net income of $133.1 million, or $2.53 a share, up from $100 million, or $2.03 a share, <TIMEX>a year earlier</TIMEX>.
````

Try to make your regular expressions as general as possible, so that
they would capture not only given examples but also some other possible
temporal expressions.

### Exercise 1.2

* Download and unpack training data [train.zip](train.zip)

The folder consists of two sub-folders: `raw` that contains plain-text
documents, and `ann` that contains the same documents manually
annotated with temporal expression.

* Write a program, that processes `raw` documents one by one,
  annotates temporal expressions in each of them (using regular
  expressions made on the previous step) and output the result into a new
  folder.

Use regular expressions made in Exercise 1.1. The documents in
the new folder should be named `<no>_sub.txt`, where `<no>` is the
same document number as in `raw` folder.

* Download the scorer [scorer.py](scorer.py) and run it on the output of the previous step.

The scorer takes three parameters: path to the gold annotations folder, path to the system output folder and (optional) name of the output. E.g.:

````bash
python train/ann/ train/sub/ train.txt
````

The scorer outputs the evaluation measures---recall, precision and
F1-score---which you should include into your report, and a detailed
evaluations in a separate file.

* Scan the scorer output trying to find the biggest problems of the annotator. Edit your code trying to improve F1-score. Process documents again and get new scores.

Repeat that process until you are satisfied with the scores.

* Download and unpack development set [dev.zip](dev.zip), run your code and the scorer.

* **Submit evaluation measures for the training and development sets**
* **Attach your code and the scorer outputs**


## Exercise 2: Temporal IE with spaCy

In this exercise we will solve the same problem using a pipeline of nlp-tools. First, the document is proccessed by spaCy to tokenize text and to assign each token with additional information, such as part of speech tags. Then, a matcher is used to find patterns in text. Patterns are similar to regular expressions but operate on tokens instead of characters.

* Install spaCy if you have not done that before:

````bash
python -m venv .env
source .env/bin/activate
pip install -U spacy
python -m spacy download en
````

> See [spaCy documentation](https://spacy.io/usage) for more details.


### Exercise 2.1

Download example code [spacy_timex.py](spacy_timex.py).  This programme processes three sentences that there used in Exercise 1 and outputs the same result using spaCy pattern matcher.

You do not need to understand everything that is going on in the code. Focus on the main function and try to understand how spaCy patterns work.

> For more details on the pattern syntax consult [spaCy documentation](https://spacy.io/usage/rule-based-matching).

* Using spaCy pattern matching make patterns that would capture temporal expressions in
the same sentences that used in Exercise 1.1


### Exercise 2.2

* Write a program, that process raw documents one by one, annotates them with temporal expressions using spaCy pattern matcher and prints output to another folder.

Use patterns made in Exercise 2.1. The documents in
the new folder should be named `<no>_sub.txt`, where `<no>` is the
same document number as in `raw` folder.

* Run scorer on the output of the previous step.

* Scan the scorer output trying to find the biggest problems of the annotator. Edit your code trying to improve F1-score. Process documents again and get new scores.

Repeat that process until you are satisfied with the scores.

* Run your code and the scorer on the development set.

* **Submit evaluations measures for the training and development sets**
* **Attach your code and the scorer outputs**


## Exercise 3: Model comparison

Now you have two time-expression annotators: regex-based and spaCy-based, and two scorer outputs for each annotator.

* Which annotator, in your opinion, is working better? Why?
* Which annotator was easier to implement, debug and modify?

Compare scorer outputs obtained on development set. Try to find cases correctly processed by one annotator but missed by another.

* What is the main strength of the regex annotator? What is its main weakness?
* What is the main strength of the spaCy annotator? What is its main weakness?
Add some examples to justify your response.

* **Submit your answers**


