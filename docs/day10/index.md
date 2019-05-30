# Day 10: Putting it all together

Today it's time to put together various components of an NLP pipeline that
we've seen in the course and build a bigger system that does something
cool. There are no specific exercises: instead you will submit a short
description of your system, as well as your code.

**You can choose what you build.** Below are a number of possible options,
with instructions on how you might go through putting together a suitable
pipeline. You don't need to follow the instructions exactly, but we
expect you to make use of a good number of different NLP components
in your pipeline.

**If you have a great idea** for some other system that you could build,
on a similar scale to these (i.e. doable in the afternoon session), you're
welcome to do that instead. Make sure to explain in your report what
your system does and why you chose to perform the analyses you did!

## System possibilities

Here are the suggestions we have for systems you might build. Further
down the page, you'll find instructions, tips, ideas, etc. for each.

 * Temporal information extraction system
 * Punny metaphor generation system
 * *More to come!*


## Instructions

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

#### Part 1: The best ever temporal expression annotator

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

#### Part 2: Scorer

By this point you have seen a number of the scorer outputs.

* Do you think the evaluation scheme is fair and meaningful?
  Did you spot any evaluation problems? What, in your opinion,
  might be a better evaluation scheme?

* Try to modify the scorer to obtain a more meaningful comparison.

Most probably you would need to modify a function called `update_scores`.

* Run a new scorer on the results obtained from all three annotators.
  Do the results make more sense to you? Why?


#### Part 3: Results and discussion

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


#### Acknowledgements

The data used in this assignment are taken from
[TempEval-3 Temporal Annotation Shared Task](https://www.cs.york.ac.uk/semeval-2013/task1/index.html).
The shared task used much mpre elaborated annotation schema and consisted
of several sub-tasks. More details on the tasks and the results can be
found in the [organizers' paper](https://www.aclweb.org/anthology/S13-2001).


### Punny metaphor generation system

This system builds on the simple **pun generation system** that
you created on day 2.

*Further description to be added here*
