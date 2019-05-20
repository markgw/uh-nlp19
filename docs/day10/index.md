Day 10: Temporal Information Continuation
==============

Carry out all the exercises below and submit your answers
[on Moodle](https://moodle.helsinki.fi/course/view.php?id=33565#section-10).
Also submit an archive containing all your code and scorer outputs. Give the files meaningful names.


Today we continue working on the Temporal Information Exctraction problem, which we started on day 8. It is assumed that you finished Day 8 assignments and have implemented two time-expression annotators: regex-based and spaCy-based. You have the training and development datasets and the scorer, and know how the annotators perfom in terms of recall, precision and F1-score. You have made a comparison of the annotators' outputs and know their main strengths and weaknesses.

Now try to find a method that would combine advantages of both annotators.


## Exercise 4: The best ever temporal expression annotator

* Implement the third annotator, which would combine advantages of both annotators, using either regular expressions, or spaCy patterns, or both.

You may use any other technology but try to reuse your code made for Exercises 1 and 2.

* Process training data using this new annotator and run scorer. The aim is to yield a higher performance than any of the two previous annotators.

Repeat this process until you are satisfied with your scores.

* Process the development set with the new annotator.

Does it perform better than the other two? If not, try to identify the problem and modify your annotator.

* **Submit a short explanation on how the annotator works**
* **Submit evaluations measures of the third annotator on the training and development sets**
* **Attach your code and the scorer outputs**


## Exercises 5: Scorer

By that point you have seen a number of the scorer outputs.

* Do you think the evaluation scheme is fair and meaningful? Did you spot any evaluation problems? What, in your opinion, might be a better evaluation scheme?

* Try to modify the scorer to obtain a more meaningful comparison.

Most probably you would need to modify a function called `update_scores`.

* Run a new scorer on the results obtained from all three annotators. Do results have more sense for you? Why?

* **Submit your answers and new evaluation scores**
* **Submit a short explanation on how the new scorer works**
* **Attach your code and the scorer outputs**


## Exercises 6: Results and discussion

Now you have three annotators and two scorers. Lets test them on unseen data.

* Download and unpack test set [test.zip](test.zip), process it with all your annotators and both scorers.

* Make a table, that would contain all your results on the test set. Give it a thought and try to make the table comprehensible for a reader.

* What is the best performing annotator on the test set? Is it the same annotator that was the best on the training and development set? Is it the best annotator according to both scorers, or only one scoring scheme?

* Which annotator has the highest precision? The highest recall? Is it more difficult to obtain a high recall or a high precision on this task? Why?

* Compare scorer outputs for all three annotators. Try to find examples when the best-performing annotator does not produce correct output. What is the biggest problem of the annotator? Propose some ways to overcome these difficulties in the future.

* Do you see any ways to use a temporal expression annotator in any real application? Which one? Which steps should be done to deploy an annotator into production?

* **Submit the result table and your answers**
* **Attach scorer outputs**


## Acknowledgements

The data used in this assignment are taken from [TempEval-3 Temporal Annotation Shared Task](https://www.cs.york.ac.uk/semeval-2013/task1/index.html). The shared task used much mpre elaborated annotation schema and consisted of several sub-tasks. More details on the tasks and the results can be found in the [organizers' paper](https://www.aclweb.org/anthology/S13-2001).
