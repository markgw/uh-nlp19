# Day 6: NLG and Dialogue

Carry out all the exercises below and submit your answers on Moodle. Also submit a single Python file containing your full implementation.

## Exercise 1: The End-to-End NLG Challenge

Read the website of the [End-to-End NLG Challenge](http://www.macs.hw.ac.uk/InteractionLab/E2E/). Observe especially the MR format towards the top of the page, and the example natural language reference associated with it. Download the dataset from the website and open the file `devset.csv`.

> **Submit to Moodle** your answer to the following questions:
> 1. How difficult does the task appear to you?
> 2. Observe the scores reported in the section "Baseline System". Are they meaningful in isolation?
> 3. What are your thoughts on the variety of language in the references of the devset?

## Exercise 2: Very simple NLG

Download [ass6utils.py](/ass6utils.py) and store it in the same directory as `devset.csv`. In the same directory set up a python file with the following contents:

```python
from ass6utils import read_file, score, MeaningRepresentation
import random

meaning_representations, references = read_file('devset.csv')

def generate(mr: MeaningRepresentation) -> str:
    return '{} is a {} {}.'.format(
        mr.name,
        mr.food,
        mr.eat_type,
    )

score(generate, meaning_representations, references)
print('--')
for _ in range(10):
    print('\t', generate(random.choice(meaning_representations)))
print('\n')
```

Familiarize yourself with the `MeaningRepresentation` class in `ass6utils.py`, especially in terms of what fields it contains. The code contains type hints, but you are free to ignore them. You don't have to add them to your code.

Run the code a few times (5 or so) and observe the results. Note that the `score` method applies your NLG-method to the whole `devset` corpus, not just the ten random samples shown to you.

**NB:** The utils code is using the `meteor_score` method which is a fairly new addition to the NLTK. If you are getting an import error, try updating NLTK. If this doesn't work, just remove the import of `nltk.translate.meteor_score` as well as the call to it in the `score` method.

> **Submit to Moodle** your answers to the following questions:
> 1. What kinds of scores is this extremely simple system achieving
> 2. How do they compare to the baseline results on the challenge's website?
> 3. Do you observe any problems with the output (other than it being so short)?

## Exercise 3: Less simple NLG

Improve upon the system so that it can produce output that reflects all the fields available in the MeaningRepresentation. Focus on just getting all the fields realized. You can start by realizing each field as its own sentence, building the output piece-by-piece like so:

```python
output = "<something>."
if mr.family_friendly == "yes":
    output += " X is family friendly."
elif mr.family_friendly == "no":
    output += " X is not family friendly."
else:
    # Say nothing about family friendliness
    pass
```

Evaluate your improved generator using the `score` method as above
> **Submit to Moodle** a few example sentences produced by your generator and the scoring it receives.

## Exercise 4: Improved NLG

Try to improve the system by producing more complex sentence structures. After each modification, check the scores but also look at the example outputs. Don't worry about variety in the output, but ensure that you are not outputting `None` values into the text.

As an example, your output could look like "*The Golden Palace is a Chinese coffee shop in riverside. It is in the £20-25 range and is of high quality.*" or "*The Eagle, a family friendly Chinese coffee shop in city centre near Burger King, has high prices and is rated 1 out of 5 stars.*"

**Don't get too stuck with this assignment, it's fine to do something simple.** Consider doing the following assignments first.

> **Submit to Moodle** examples of output from your (hopefully) improved system together with the scores obtained using the `score` method. It's perfectly OK if you can't get the scores to go up as long as you tried something out. 

## Exercise 5: Reflect on the complexity

>**Submit to Moodle** your answers to the following questions. A few sentences each is sufficient.
> 1. How difficult would it be to modify the system to produce a wider variety of sentences?
> 2. Think of another language you speak. How much work would it be to translate the system to that language compared to this initial implementation?
> 3. Using the Gatt & Krahmer classification (Refer to slides), how would you characterize the system you built?
> 4. Think back on your answers to Exercise #1. Did the task turn out easier or more difficult than you anticipated?
> 5. Think about the pros and cons of the neural systems as discussed in the lecture. Do you think this task is good for them (consider the data, the complexity etc.)? Do you expect them to fare better than "classical" systems?
> 6. How do the Baseline scores (on the E2E website) compare to your scores? How did you compare to the other systems reported in Table 3 of the [Findings of the E2E NLG Challenge -paper](https://arxiv.org/pdf/1810.01170.pdf)?
> 7. Look at the same table. Check from the caption how the colors match the system architectures. How are the rule-based and template-based systems faring against the seq2seq and other data-driven systems? Does this match your expectation from before?


## Exercise 6: Explore BLEU

Import the `bleu_single` method from `ass6utils.py`. Pick some NL realisation, either from those you generated or from the `devset.csv`. Call it the *reference*.

Try out different modifications to the reference and calculate the BLEU scores (using `bleu_single`) between the original and the modified reference. Try to come up with a pair of modifications where candidate #1 has the same logical content (i.e. same information) as the reference and candidate #2 contains some falsehood, but the BLEU scores rank candidate #2 higher than candidate #1.

>**Submit to Moodle** the reference and the candidates you found together with the BLEU scores. What does this tell you about the BLEU scores as a metric? What is the problem with the way we are using the BLEU score? Recall the assumptions behind these kinds of metrics from the slides.

## Exercise 7: Human Evaluation

>**Submit to Moodle** your answers to the following questions. A few sentences each is sufficient.
> 1. What kinds of questions would you ask if you were to conduct an intrinstic human evaluation on this task?
> 2. Can you come up with an extrinsic human evaluation for this task?
> 3. Read Section 4.2 from the [Findings of the E2E NLG Challenge -paper](https://arxiv.org/pdf/1810.01170.pdf). How did seq2seq systems compare to other interms of naturalness and quality?
> 4. Do you think naturalness or quality (~correctness) is more important for a system describing (perhaps recommending) restaurants?
