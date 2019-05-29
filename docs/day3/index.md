# Day 3: Finite-State Methods and Statistical NLP

Carry out all the exercises below and submit your answers
[on Moodle](https://moodle.helsinki.fi/course/view.php?id=33565#section-4).
Also submit a single Python file containing your full
implementation.


## Exercise 1: HMM estimation

In this exercise, we will load a corpus annotated manually with
POS tags. NLTK provides easy access to the [MASC corpus](http://www.anc.org/data/masc/),
a part of the Open American National Corpus (OANC) that has
been annotated with various linguistic analyses.

A POS-tagged corpus like this can be used to estimate the
parameters of an HMM, as seen in today's lectures. The
trained model can then be used to POS tag new sentences.

We will begin by computing some of the parameters of an HMM
using **Maximum Likelihood Estimation** (MLE) based on
counts from the corpus. (See lecture slides for more
explanation of this.)

Start by downloading the MASC corpus:
````python
nltk.download("masc_tagged")
````

You can load data from the corpus like this:
````python
from nltk.corpus import masc_tagged
print(masc_tagged.tagged_sents()[0])
print(masc_tagged.tagged_sents()[1])
````

Each sentence consists of (word, tag) pairs:
````python
[('Good', 'JJ'), ('evening', 'NN'), ... ]
````

Recall that the HMM contains two distributions: the **transition**
distribution between tags and the **emission** distribution
from tags to words.
By iterating over the data in MASC, collect the counts needed
to estimate the transition distribution *from* the
verb tag (`VB`) to all other tags (i.e. *p(t[i+1] | t[i] = VB)*).

Also collect counts needed to estimate the emission distribution
for the `VB` tag (i.e. *p(w[i] | t[i] = VB)*).

Compute both of these distributions.

 * Collect these counts and estimate the distributions for `VB`
    using MLE.
 * **Submit the computed *p(t[i+1] = DT | t[i] = VB)* - the probability
    of a verb being followed by a determiner.**
 * **Submit the computed *p(w[i] = 'feel' &#124; t[i] = VB)*.**




## Exercise 2: A full HMM

NLTK contains a function to collect all the necessary counts to
train an HMM using MLE, exactly as you have done above.
The class `nltk.tag.hmm.HiddenMarkovModelTagger` implements
HMM training and tagging.

Use the function
[`HiddenMarkovModelTagger.train()`](https://www.nltk.org/api/nltk.tag.html#nltk.tag.hmm.HiddenMarkovModelTagger.train)
to estimate
all probabilities for an HMM POS tagger from the MASC corpus.

Your HMM can now be used to tag new sentences:
````python
tagged_sent = hmm.tag(
    ["The", "answer", "is", "blowing", "in", "the", "wind", "."]
)
````

> The POS tag set used by this corpus is the same as the Penn Treebank
> and the same one used by the tagger in yesterday's assignment.
> You can find a [description of each tag here](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html).

Try tagging the following sentences:
````
Once we have finished , we will go out .
There is always room for more understanding between warring peoples .
Evidently , this was one of Jud 's choicest tapestries , for the noble emitted a howl of grief and rage and leaped from his divan .
````

The second example contains the ambiguous word *understanding*,
which could take several different tags. Look at how your tagger
handled it.

Take a look at how the tagger behaves when it sees previously
unseen words. *Jud* (in the third example) is not in the training
corpus, but the tagger makes a guess anyway. Although it has
no tags with a non-zero *p(w='Jud'|t)*, it is able to choose
a tag that fits well in the context, thanks to the transition
distribution.

Try some more examples with unseen words and observe how the
tagger manages. Here are a couple to get you started:
````
Misjoggle in a gripty hifnipork .
One fretigy kriptog is always better than several intersplicks .
````

 * What tag did the tagger assign to *understanding*? Is this correct?
 * Give one example of a sentence with unseen words where the
   tagger, in your opinion, picks the correct tags for the unseen words.
 * Give one example where the tagger is thrown off by an
   unseen word. What information might help it make a better guess?
   (Other than seeing the word in its training set!)
 * **Submit your answers as text**



## Exercise 3: Semi-supervised learning

There are many well studied algorithms for working with HMMs: performing
efficient inference (tagging), training in ways that deal better with
sparse or unseen data and unsupervised training.

Here we will use an **unsupervised** training method let our HMM
benefit from having seen
more data. NLTK provides an implementation of the *Baum-Welch* algorithm,
an instance of the *Expectation-Maximization* (EM) algorithm.

Baum-Welch is able to infer a tagging model with no labelled data at all.
A downside of this is that the tags do not necessarily have any
correspondence to real POS tags. Here we will train on the labelled data
we used above, which will be used to initialize a model, *and* a further
unlabelled set. The algorithm iteratively makes guesses as to the POS
tags for words and updates the model's probability distributions from
these guesses.

 * Download the text file [radio_planet_tokens.txt](radio_planet_tokens.txt)

This contains tokenized text from the book
[Radio Planet, by Ralph Milne Farley](http://www.gutenberg.org/ebooks/52326).
This is quite a different domain to the original (labelled) training data.
Load text from the file: one sentence per line, with tokens separated by
spaces.

 * Download the Python file [ass3utils.py](ass3utils.py) and put it
   in the same directory as your Python source.

The function `train_unsupervised()` provides a small wrapper around
NLTK's training to ensure that the unsupervised model is expanded to
cover words unseen in the labelled data. (This is a form of
**semi-supervised** learning.)

Train an HMM using the previous labelled data as well as the new raw data.
This could take a bit of time to run (for me it took 1-2m per iteration).
The default number of iterations is 3, but, if you have time, you might
like to try increasing this
(using the `max_iterations` kwarg to `train_unsupervised()`).

> Training this model could take up to 15m, depending on the parameters
> you set and the computer you're running on. You will reuse it
> in the following exercises.
>
> It's a good idea to store your trained model (returned by
> `train_unsupervised()`) to a file using Python's
> [`pickle` library](https://docs.python.org/3/library/pickle.html)
> and then load it again on subsequent runs, so you don't have to
> re-train it every time you run the later exercises.

Try tagging the earlier example sentences with the new model.

Also try tagging some new sentences from later in *Radio Planet*:
````
Yesterday these fiends operated upon Doggo .
For a time, his own soul and this brain - maggot struggled for supremacy .
````

 * Has the unlabelled data improved the tagger?
 * What could you do to (further) improve the tagger's performance on
   different domains?
 * **Submit your answers**


## Exercise 4: Cross-domain tagging

Try feeding some other sentences into the POS taggers, comparing the
output from the supervised and semi-supervised models.
Try out sentences from a number of different domains:
e.g. fiction, news, legal documents, ...

 * **Submit a few sentences reporting your observations**


## Exercise 5: HMM as a language model

The HMM class has a method
[`log_probability()`](https://www.nltk.org/api/nltk.tag.html#nltk.tag.hmm.HiddenMarkovModelTagger.log_probability)
that uses the full
generative model to assign a probability to a given input sentence.
This allows you to use your trained model as a **language model**.
The model is similar to the Markov language model seen in the
lecture, except that word probabilities are conditioned on (unknown,
inferred) POS tags.

> The `log_probability()` method expects a list of `(word, pos_tag)`
> pairs as input. You don't have to specify the POS tag (it will
> sum over all possible tags if not given), but you still have to
> give it `(word, None)` pairs.

Try using your models as LMs. Measure the log probability of some
short sentences (perhaps including some of the examples above)
using both of your HMMs.
Also estimate the probability of some nonsense sentences you make
up: use real words that are likely to be covered by the model.

 * Do the nonsense sentences tend to receive lower probabilities
   than the real ones?
 * Is the semi-supervised model better at distinguishing between
   real and nonsense sentences?
 * **Submit your answers**

> We will carry out a similar comparison, applying better evaluation
> techniques, on day 5.


## Exercise 6: Generating from HMMs

The HMM provides a simple method to sample random sentences from the
model,
[`random_sample(rng, length)`](https://www.nltk.org/api/nltk.tag.html#nltk.tag.hmm.HiddenMarkovModelTagger.random_sample).
It requires a random number
generator (you can use Python's `random` module) and a length for
the sentence.

Try generating some sentences from your HMMs.

 * Do they look like real sentences?
 * Why are they (usually) incoherent?
 * Why don't they look like the sentences in the training corpus?
 * Is the unsupervised model better?
 * **Submit short answers to these questions**


## Exercise 7: Improving generation

How might you improve on the sentence generator to give
the generated sentences more coherence?

Don't implement anything: just discuss (briefly).

 * **Submit your discussion**
