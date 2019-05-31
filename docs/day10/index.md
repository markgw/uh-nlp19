# Day 10: Putting it all together

Today it's time to put together various components of an NLP pipeline that
we've seen in the course and build a bigger system that does something
cool. There are no specific exercises: instead you will submit a short
report.

**You can choose what you build.** Below are a number of possible options,
with instructions or ideas on how you might put together a suitable
pipeline. You don't need to follow the instructions exactly. We just
expect you to make use of a good number of different NLP components.

**If you have a great idea** for some other system that you could build,
on a suitable scale (i.e. doable in the afternoon session), you're
welcome to do that. Make sure to explain in your report what
your system does and why you chose to perform the analyses you did!


## Submission

You should submit a **short report** containing the following:
 * The task your system addresses
 * The pipeline you used, especially any standard components
 * Some analysis of the system's performance: e.g.
   - Any evaluation results available
   - Conclusions from manual inspection of output
   - Problems that meant you didn't any satisfactory output
 * How you might extend or improve the system if you had more
   time (or computing resources, or data, ...)

Also submit **your code** as a single Python file.
(Don't worry too much about cleaning it up or submitting
production-quality code!)

We will not be grading your submission in any detail on the basis
of the success of your system. The main purpose of this assignment
is for you to have putting into practice a bit of what you've learned
for your own benefit.


## System suggestions

Here are some suggestions for systems you might build. Further
down are instructions, tips, ideas, etc. for each.

The first two suggestions come from the course organisers. The others
are your own
[ideas that you wrote in groups during day 2's lecture](https://moodle.helsinki.fi/mod/forum/view.php?id=1598902).
They will mostly need some refinement (in particular, making them
much less ambitious!) for this purpose.

 * [Temporal information extraction system](#temporal-information-extraction)
 * [Metaphor generation system](#metaphor-generation-system)
 * [Pun generation system](#pun-generation-system)
 * [Identify similar words](#identify-similar-words)
 * [Text summarization](#text-summarization)
 * [Language generation](#language-generation)
 * [News tagging](#news-tagging)
 * [Recognizing politicians' stand-point through their Twitter](#recognizing-politicians-stand-point-through-their-twitter)
 * [Automatic medical diagnosis system](#automatic-medical-diagnosis-system)


## Instructions and ideas

### Temporal information extraction

Here we can continue working on the Temporal Information Exctraction problem,
which we started on day 8. It is assumed that you finished Day 8 assignments
and have implemented two time-expression annotators: regex-based and
spaCy-based.

You have the training and development datasets and the scorer, and
know how the annotators perform in terms of recall, precision and
F1-score. You have made a comparison of the annotators' outputs and know
their main strengths and weaknesses.

Now try to find a method that would combine advantages of both annotators.

The following instructions will take you through
some further ways to develop your system. You are welcome to choose a
different approach.

**The best ever temporal expression annotator**

* Implement a third annotator, which would combine advantages of
  both annotators, using either regular expressions, or spaCy patterns, or both.

You may use any other technology but try to reuse
your code made for Exercises 1 and 2.

* Process training data using this new annotator and run scorer.
  The aim is to yield a higher performance than any of the two previous annotators.

Repeat this process until you are satisfied with your scores.

* Process the development set with the new annotator.

Does it perform better than the other two? If not, try to identify the
problem and modify your annotator.

**Scorer**

By this point you have seen a number of the scorer outputs.

* Do you think the evaluation scheme is fair and meaningful?
  Did you spot any evaluation problems? What, in your opinion,
  might be a better evaluation scheme?
* Try to modify the scorer to obtain a more meaningful comparison.

Most probably you would need to modify a function called `update_scores`.

* Run a new scorer on the results obtained from all three annotators.
  Do the results make more sense to you? Why?


**Results and evaluation**

Now you have three annotators and two scorers. Let's test them on unseen data.

* Download and unpack test set [test.zip](test.zip), process it with all
  your annotators and both scorers.
* Make a table, that would contain all your results on the test set.
  Give it a thought and try to make the table comprehensible for a reader.
* What is the best performing annotator on the test set? Is it the
  same annotator that was the best on the training and development set?
  Is it the best annotator according to both scorers, or only one scoring scheme?
* Which annotator has the highest precision? The highest recall?
  Is it more difficult to obtain a high recall or a high precision on this task? Why?
* Compare scorer outputs for all three annotators.
  Try to find examples when the best-performing annotator does not produce
  correct output. What is the biggest problem of the annotator?
  Propose some ways to overcome these difficulties in the future.
* Do you see any ways to use a temporal expression annotator in any
  real application? Which one? Which steps should be done to deploy an annotator into production?

> The data used in this assignment are taken from
> [TempEval-3 Temporal Annotation Shared Task](https://www.cs.york.ac.uk/semeval-2013/task1/index.html).
> The shared task used a much elaborate annotation schema and consisted
> of several sub-tasks. More details on the tasks and the results can be
> found in the [organizers' paper](https://www.aclweb.org/anthology/S13-2001).



### Metaphor Generation System
The goal of this task is to use knowledge bases of nouns along with their stereotypical adjectival properties (i.e. adjectives that are strongly associated with the nouns) to generate metaphorical expressions.

You can use the knowledge bases provided in [Prosecco Network's Github](https://github.com/prosecconetwork/ThesaurusRex) *Read the README file for descriptions of each file*. Alternatively, you can use other resources (e.g. word embeddings models) to obtain similar relations.

In the resources, the file `expanded_weights.txt` contains inferred stereotypical relations, which makes it more extensive (see [this site](https://expanding-properties.mokha.pw/) for an interactive interface for expanding a seed list of properties). To download the knowledge base, execute the following command:

````sh
wget https://raw.githubusercontent.com/prosecconetwork/ThesaurusRex/master/expanded_weights.txt
````

You can read and parse the knowledge base using the below code:

````python
import io, re
from collections import defaultdict
def parse_members_rex_weights(file):
  '''
  Parses the `expanded_weights.txt` file and returns:
  {
      NOUN: {
          PROPERTY: WEIGHT,
          ...
      }
      ...
  }
  '''
  weights = defaultdict(lambda: defaultdict(float))
  rg_ptrn = re.compile(r"^(\d+)\. ([\d\w_\.\-\"\']+) \[(.*)\]$", re.UNICODE | re.IGNORECASE)  # magical regex pattern
  with io.open(file, 'r', encoding='utf-8') as inp_file:
    for l in inp_file:
      matched = rg_ptrn.match(l).groups()
      member = matched[1].replace('_', ' ')
      properties = map(lambda p: p.replace(')', '').split('('), matched[2].replace(' ', '').split(','))
      properties = map(lambda x: tuple([' '.join(x[0].split('_')[:-1]), float(x[1])]), properties)
      properties = list(properties)
      weights[member] = dict(properties)
  return weights

stereotypes = parse_members_rex_weights('expanded_weights.txt')
````

Now, you can use such knowledge base to create metaphors, similes and analogies. For instance, to produce a metaphor that highlights that someone is very brave, you need to find out a noun that is well-known to be brave. A simple code to do that is:

````python
brave_nouns = [(noun, properties['brave']) for noun, properties in stereotypes.items() if 'brave' in properties] # get brave nouns
brave_nouns = sorted(brave_nouns, key=lambda k: k[1], reverse=True) # sort them based on the strength
print(brave_nouns) # [(u'Hero', 1778.0), (u'Warrior', 1491.0), ...]
````

With this knowledge, you can construct some metaphorical templates (e.g. "X is Y") and fill them dynamically (refer to `Day 6 - Exercise 2: Very simple NLG`) with the knowledge you have depending on the context. Following the earlier example, you can produce metaphorical expressions like "X is a hero", "X is as brave as a hero", "Like a hero, X rescued the dog." and so on.

Write a function that accepts a text and performs some analyses (e.g. POS tagging, dependency parsing, entity recognition). If the sentence contains a noun and an adjective that has an adverb with the relation `advmod`, the function would remove the adverb and, then, inject a metaphorical expression that fits the context. The insertion could be for example after the noun or at the beginning/end of the sentence. Don't complicate the system, just build a very simple proof-of-concept.

Examples:
* The lawyer was extremely aggressive.
  * The lawyer was aggressive, like a monster.
  * Like a boxer, the lawyer was aggressive.
  * ...
* Her lawyer is very annoying.
  * Her lawyer is annoying, like a child.
  * Like a bully, her lawyer is annoying.
  * ...


### Pun Generation System
The goal of this exercise is to extend the pun generator you have implemented during day 2 (feel free to use the model solution). Below are some ideas for improving it (you are free to improve it differently as long as you motivate your choices):

* Build a generic pun generator (e.g. using words in `wordnet` or a dictionary of lemmatized words)
* Consider specific prosody features (e.g. rhyme and alliteration)
* Different pronunciation measurement (have a look at [abydos](https://github.com/chrislit/abydos))


### Identify similar words

[Original suggestion](https://moodle.helsinki.fi/mod/forum/discuss.php?d=864581#p2126484)

Pipeline:
 1. Sentence level tokenization
 2. Word level tokenization
 3. Remove stop words and punctuation
 4. Lemmatization
 5. Morphological analysis
 6. Chunking to phrases
 7. Vectorizing words
 8. Comparing cosine similarities

There are lots of sources of ready-made word vectors out there for
English, and many other languages. However, this could be an interesting
thing to try because:
 * it gives you practical experience of constructing embeddings;
 * you can play around with different methods (e.g. dependency-based
   features, phrase vectors) to see how they affect the results;
 * you could experiment with the effects of training on different
   languages, domains, language types, etc.




### Text summarization

[Original suggestion](https://moodle.helsinki.fi/mod/forum/discuss.php?d=864580#p2126483)

Text summarizatoin accepts as input an arbitrary text (e.g. news article, conversation) and produces its short summary.

**It uses**

Standard NLP components:
* tokenization
* lemmatization
* POS tagging
* Parsing
* Named-entity recognition
* Morphology
* Semantic-role labelling
* Sentence-level semantics
* Document meaning / analysis

Additionally, we can add speech recognition as the first step

Additional components:
* Remove redundancy and details from the text
* NLG components to produce the summary

Potential problems:
* Tokenizer might split sentence and word boundaries wrongly;
* Lemmatizer might lemmatize words wrongly;
* NER component might misdetect NEs;
* Semantic-role labelling might label roles wrongly; etc.
* And all above mentioned could lead to change of meaning.

**Challenge:** How to choose what is important in the text?

Of course, this is a big task and will take a long time to do
well. But it could be very interesting to see how far you can
get with just a few analysis tools and simple strategies for
choosing important phrases, constructing the summary, etc.




### Language generation

[Original suggestion](https://moodle.helsinki.fi/mod/forum/discuss.php?d=864579#p2126481)

*A system for generating text.*

 1. A large corpus is split into sentences.
 2. Tokenization
 3. Lemmatization
 4. Build a generative language model (e.g. markov chain)

Generative model probably outputs bad language and nonsense. The quality of the model depends on the corpus. A more complex model and domain specific corpus needed for passable results.

Interesting things you could explore/learn from this:
 * Effect of different corpora on results
 * Different types of LM: e.g. you could try an LSTM
 * Possible ways to control the output: e.g. condition the sentence on some
   feature from training documents' metadata, like keywords from headlines
   or categories, which can then be set by at generation time
 * Strategies for sampling coherent and interesting sentences from the
   model's probability distributions





### News tagging

[Original suggestion](https://moodle.helsinki.fi/mod/forum/discuss.php?d=864577#p2126479)

*The system gives tags to news articles.*

1. Sentence splitting
2. Tokenization
3. Lemmatization
4. POS
5. NER
6. Topic modelling?

From NER we can just get some of the named entities as tags. Also maybe use topic modelling.

If lemmatization or NER goes wrong (for example NER does not recognize named entities), then we have problems.
We might get useless tags. We need to somehow figure out which tags are important.

You could perform some manual error analysis of the output and assess
where the system is going wrong and how the tagging algorithm could
produce more useful output.

If you have a dataset with manually assigned tags, you could do this
by training a classifier, using features from your pipeline. You will
probably find some suitable examples in one of the lists below.

There are many possible datasets you could try this out on.
Here are some ideas:
- [English, BBC articles](http://mlg.ucd.ie/datasets/bbc.html)
- [Swedish news](https://spraakbanken.gu.se/eng/resource/attasidor)
- [Fake news corpus](https://github.com/several27/FakeNewsCorpus)
- [Others in this list](https://www.clarin.eu/resource-families/newspaper-corpora)
- [Others in this list](https://github.com/niderhoff/nlp-datasets)




### Recognizing politicians' stand-point through their Twitter

[Original suggestion](https://moodle.helsinki.fi/mod/forum/discuss.php?d=864582)

Pipeline:
 1. Extract English data from twitter messages of politicians
   running for the EU parliament
 2. Tokenization
 3. Lemmatization
 4. POS tagging
 5. NER (for example EU, politic parties)
 6. Parsing
 7. Sentence-level semantics
 8. Semantic-role labeling
   (Finding the relation, i.e. stand-point.
   For example same-sex marriage for or against?)
 9. Analyzing the agreement-level/Multi-level classification
   (For example very much against, against, neutral, okay with it, for it)

Potential problems:
 - Twitter text can be noisy (for example slang) and short -> true message doesn't come through. Worst case might classify a politicians as against something rather than for
 - Politicians often use moderate words or tricky expressions to not take such a strong stance. Rather be neutral/hope for the reader to impose her/his own opinions
 - Sarcasm/humour is not easy to recognize

Some further problems, for this assignment:
 1. The above pipeline is not easy to implement quickly (or at all...?)
 2. Labelled data may be possible to retrieve (e.g. from Vaalikone),
    but preparing the data may take a lot of time.

**Regarding 1:** Think about simpler, shallower methods you could
try. E.g. some features from lower-level processing could be fed
into a classifier, instead of relying on more abstract analysis.

**Alternatively**, you could try some ready-made systems for English
abstract analysis (e.g. SRL) and try to find some relatively reliable
signals of stance they produce.

**Regarding 2:** Perhaps there's a related task for which data is
more easily available, which could be seen as a test case or proof of
concept for the task above.
[Take a look at this list](https://github.com/shaypal5/awesome-twitter-data),
for example.




### Automatic medical diagnosis system

[Original suggestion](https://moodle.helsinki.fi/mod/forum/discuss.php?d=864583#p2126489)

User calls the medical hotline and describes the symptoms.
The system tries to guess the nature of the illness based on the description.

Pipeline components:
 * Speech-to-text
 * Tokenization
 * Lemmatization
 * POS tagging
 * Parsing
 * NER
 * Information Extraction
 * Medical database
 * Bayesian network or similar
 * Prediction
 * Text-to-speech

For the purposes of this assignment, you probably want to drop the
speech-related components at the start and end.

Think carefully about what components are necessary and how you will
use their output further down the pipeline.

A crucial factor in this system will be the **knowledge resources**
that supply the medical information. Here are a couple you could
consider:
 * [MedlinePlus Medical Encyclopedia](https://medlineplus.gov/encyclopedia.html)
 * [Diseases Database](http://www.diseasesdatabase.com/content.asp)

However, *avoid spending all your time scraping websites!*
An easily available, poor quality knowledgebase will be most useful
as a proof of concept. You can develop your system to use better
medical databases later, before releasing for use by the medical
profession or selling it to make millions.
