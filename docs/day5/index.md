# Day 5: Evaluation

Carry out all the exercises below
and submit your answers on
[Moodle](https://moodle.helsinki.fi/course/view.php?id=33565#section-5).
Also submit a single Python file containing your full implementation.  


## Exercise 1: Basics


Consider an information retrieval system that returns a retrieval set of 15 documents (`retrieved`).
Each document in `retrieved` is labelled as *relevant* (`'R'`) or *non-relevant* (`'N'`):   

````python
total_docs = 100
total_relevant = 10

retrieved = ['R', 'N', 'N', 'R', 'R', 'N', 'N', 'N',
             'R', 'N', 'R', 'N', 'N', 'R', 'R']

````

### Exercise 1.1

Continuing the snippet given above, compute the numbers of true positives, false positives, true negatives, and
false negatives. Then, compute the values of the following metrics (round the values to two decimal places):

* Precision
* Recall
* F-score with &beta; = 1 (also known as *F1-score*)
* Accuracy
* **Submit the values you computed for each metric**

### Exercise 1.2

Consider the following scenario: a database consists of 10,000 documents in total, of which 10 are relevant.    

* Is accuracy an appropriate metric for evaluating the performance of a retrieval system in this scenario?
Why/why not? Discuss shortly.
* **Submit your answer**


## Exercise 2: Evaluation of a POS tagger

In exercises 2.1-3, we evaluate a POS tagger based on a hidden Markov model (HMM), which you
implemented on Day 3.

Today, we will again use the Penn Treebank corpus that you used yesterday.
You will already have downloaded yesterday using:
````python
import nltk
nltk.download('treebank')
````

We use 80% of sentences for training, and the remaining 20% for testing.  
The following code splits the corpus of sentences into training and test sentences,
and assigns test tokens and the correct tags into separate lists.

Train the HMM with `training_sents`, as in exercise 2 of Day 3.
Download [ass5utils.py](ass5utils.py) into the same directory as
your source code.

````python
from nltk.corpus import treebank
from nltk.tag.hmm import HiddenMarkovModelTagger
from ass5utils import split_corpus

training_sents, test_sents = split_corpus(treebank, 0.8)

test_tokens = [t[0] for s in test_sents for t in s]
correct_tags = [t[1] for s in test_sents for t in s]

hmm_tagger = HiddenMarkovModelTagger.train(training_sents)
````

### Exercise 2.1: Confusion matrix

Use the HMM to predict the tags for `test_tokens`.
(If you've forgotten how to do this, refer back to your code from day 3.)

Then, compute the confusion matrix between the predicted tags and `correct_tags`.  
You can use the
[`nltk.metrics.ConfusionMatrix`](https://www.nltk.org/api/nltk.metrics.html#nltk.metrics.confusionmatrix.ConfusionMatrix)
class for this exercise.

(In the confusion matrix, rows are the correct tags and columns are the predicted tags.
That is, an entry `cm[correct_tag, predicted_tag]` is the number of times a token with true tag `correct_tag` was
tagged with `predicted_tag`.)

* Which `(correct_tag, predicted_tag)` pair was the most common error? How many times did it occur?
* What is the overall accuracy of the HMM tagger? (Round the value to two decimal places.)
* Compute the precision, recall, and F1-score (&beta; = 1) for the tag `'NN'`. (Round the value to two decimal places.)
* **Submit the answers**


### Exercise 2.2: Comparison with baselines

We would like to know whether the HMM tagger is any good compared to naive baselines.

Now, implement the following functions:
 * `random_tagger(tagset, tokens)`: given a list of tokens, assigns a POS tag randomly to each token.
 (The tagset is defined in [ass5utils.py](ass5utils.py).)

 * `majority_tagger(training_sents, tokens)`: find the tag that is most common in the training sentences,
 and tag each token with this tag.

Compute the overall accuracy of both baselines, and compare the values with the HMM.

* Which baseline performs better?
* What is the difference in accuracy (expressed in [percentage points](https://en.wikipedia.org/wiki/Percentage_point)) between this baseline and the HMM? (Round the value to one decimal place.)   
* **Submit the name of baseline and accuracy difference**


### Exercise 2.3: Evaluation of HMM language model

Recall exercise 5 on Day 3, where you used the HMM as a language model.

Again, use the `log_probability()` method of the HMM to compute the total log-probability of test tokens.
(The input should be given as `(token, None)` pairs.)

* Compute the perplexity given the log-probability (round the value to two decimal places).
* What does the perplexity of a language model describe? Explain shortly.
* How could we find out whether the HMM language model is 'good'? Explain shortly.
* **Submit the perplexity value and explanations**

## Exercise 3: Text annotation

Consider the following sentences from Penn Treebank corpus:
````python
s1 = ['So', 'far', 'Mr.', 'Hahn', 'is', 'trying', 'to', 'entice', 'Nekoosa', 'into', 'negotiating', 'a', 'friendly',
'surrender', 'while', 'talking', 'tough']
s2 = ['Despite', 'the', 'economic', 'slowdown', 'there', 'are', 'few', 'clear', 'signs', 'that', 'growth', 'is',
'coming', 'to', 'a', 'halt']
s3 =  ['The', 'real', 'battle', 'is', 'over', 'who', 'will', 'control', 'that', 'market', 'and', 'reap',
'its', 'huge', 'rewards']
````


### Exercise 3.1

Annotate the sentences with appropriate POS tags.
The tags are described [here](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html).  

(It is not the aim of the exercise to annotate exactly according to guidelines,
so simply make your best guess of the correct tag.)       

* Give an example of a word/phrase you found difficult to annotate.  
* Why is this example difficult? Explain shortly.
* **Submit your answer as text**


### Exercise 3.2

The corresponding gold-standard tags of the sentences are below:

````python
tags1 = ['IN', 'RB', 'NNP', 'NNP', 'VBZ', 'VBG', 'TO', 'VB', 'NNP', 'IN', 'VBG', 'DT', 'JJ', 'NN', 'IN', 'VBG', 'JJ']
tags2 = ['IN', 'DT', 'JJ', 'NN', 'EX', 'VBP', 'JJ', 'JJ', 'NNS', 'IN', 'NN', 'VBZ', 'VBG', 'TO', 'DT', 'NN']
tags3 = ['DT', 'JJ', 'NN', 'VBZ', 'IN', 'WP', 'MD', 'VB', 'DT', 'NN', 'CC', 'VB', 'PRP$', 'JJ', 'NNS']
````

* Compute the *raw agreement rate* between your own annotations and the tags above.
**Submit the rate**  
