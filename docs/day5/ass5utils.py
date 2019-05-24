
tagset = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN',
          'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM',
          'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB']


def split_corpus(corpus, training_split=0.8):

    # There are some additional tags for punctuation marks, footnotes, etc. in the corpus,
    # which we filter out for the purposes of the exercises
    training_size = int(training_split * len(corpus.sents()))
    tagged_sents = [[t for t in s if t[1] in tagset] for s in corpus.tagged_sents()]

    training_sents = tagged_sents[:training_size]
    test_sents = tagged_sents[training_size:]

    return training_sents, test_sents