# Utilities for NLP 2019 course, assignment 3
from nltk.util import unique_list
from nltk.tag import HiddenMarkovModelTrainer
from nltk.probability import LidstoneProbDist


def train_unsupervised(labeled_sents, unlabeled_sents, max_iterations=3):
    symbols = unique_list(word for sent in labeled_sents for word, tag in sent)
    # Extend symbols with those in the unlabelled set
    symbols = unique_list(symbols + unique_list(word for sent in unlabeled_sents for word in sent))
    tag_set = unique_list(tag for sent in labeled_sents for word, tag in sent)

    trainer = HiddenMarkovModelTrainer(tag_set, symbols)
    print("Supervised training for initialization ({} sentences)".format(len(labeled_sents)))
    hmm = trainer.train_supervised(labeled_sents, estimator=lambda fd,bins: LidstoneProbDist(fd, 0.1, bins))

    # The unlabeled sentences are expected to have tags, which are ignored
    unlabeled_sents = [
        [(word, None) for word in sent] for sent in unlabeled_sents
    ]
    print("Unsupervised training ({} sentences) for up to {} iterations".format(
        len(unlabeled_sents), max_iterations
    ))
    hmm = trainer.train_unsupervised(
        unlabeled_sents, model=hmm, max_iterations=max_iterations, verbose=True
    )
    return hmm
