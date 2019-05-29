import csv
from typing import Any, Dict, List, Callable, Tuple
from collections import defaultdict
from nltk.translate.bleu_score import corpus_bleu, sentence_bleu
from nltk.translate.meteor_score import meteor_score
from nltk.tokenize import TweetTokenizer

tokenizer = TweetTokenizer()

class MeaningRepresentation(object):
    def __init__(self, 
                 eat_type: str, 
                 price_range: str, 
                 near: str, 
                 name: str, 
                 food: str, 
                 customer_rating: str, 
                 family_friendly: str, 
                 area: str
            ) -> None:
        self.eat_type = eat_type
        self.price_range = price_range
        self.near = near
        self.name = name
        self.food = food
        self.customer_rating = customer_rating
        self.family_friendly = family_friendly
        self.area = area

    @staticmethod
    def from_dict(d: Dict[str, str]) -> 'MeaningRepresentation':
        return MeaningRepresentation(
            d.get('eatType'),
            d.get('priceRange'),
            d.get('near'),
            d.get('name'),
            d.get('food'),
            d.get('customer rating'),
            d.get('familyFriendly'),
            d.get('area')
        )
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MeaningRepresentation):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash((
            self.eat_type,
            self.price_range,
            self.near,
            self.name,
            self.food,
            self.customer_rating,
            self.family_friendly,
            self.area
        ))

    def __str__(self) -> str:
        return '<' + ', '.join('{}[{}]'.format(key, val) for key, val in self.__dict__.items()) + '>'

    def __repr__(self) -> str:
        return str(self)


def read_file(filename: str) -> Tuple[List[MeaningRepresentation], List[List[str]]]:
    with open(filename) as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(file_reader)  # Skip header

        contents = defaultdict(list)
        
        for row in file_reader:
            mr_part = row[0].split(', ')
            reference_text = row[1]
            mr_dict = dict()
            for key_value_pair in mr_part:
                key_value_pair = key_value_pair.split('[')
                key = key_value_pair[0]
                value = key_value_pair[1][:-1]
                mr_dict[key] = value
            mr = MeaningRepresentation.from_dict(mr_dict)
            contents[mr].append(reference_text)
    return zip(*contents.items())


def rouge(hypotheses: List[str], references: List[List[str]]) -> float:
    scorer = RougeScore()
    scores = [scorer.rouge_l(hyp, refs, 0.5) for hyp, refs in zip(hypotheses, references)]
    return sum(scores) / len(scores)


def meteor(hypotheses: List[str], references: List[List[str]]) -> float:
    scores = [meteor_score(refs, hyp) for hyp, refs in zip(hypotheses, references)]
    return sum(scores) / len(scores)


def bleu(hypotheses: List[str], references: List[List[str]]) -> float:
    hypotheses = [tokenizer.tokenize(sent) for sent in hypotheses]
    references = [[tokenizer.tokenize(sent) for sent in ref_list] for ref_list in references]
    return corpus_bleu(references, hypotheses)


def bleu_single(hypothesis: str, reference: str) -> float:
    return sentence_bleu([tokenizer.tokenize(reference)], tokenizer.tokenize(hypothesis))


def score(generator: Callable[[MeaningRepresentation], str], 
          meaning_representations: List[MeaningRepresentation], 
          references: List[List[str]]) -> None:

    hypotheses = [generator(mr) for mr in meaning_representations]

    print('BLEU score:', bleu(hypotheses, references))
    print('METEOR score:', meteor(hypotheses, references))
    print('ROUGE-L score:', rouge(hypotheses, references))



class RougeScore(object):
    """
    MIT License

    Copyright (c) 2016 Brian DuSell

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """
    import collections

    def _ngrams(self, words, n):
        queue = collections.deque(maxlen=n)
        for w in words:
            queue.append(w)
            if len(queue) == n:
                yield tuple(queue)

    def _ngram_counts(self, words, n):
        return collections.Counter(self._ngrams(words, n))

    def _ngram_count(self, words, n):
        return max(len(words) - n + 1, 0)

    def _counter_overlap(self, counter1, counter2):
        result = 0
        for k, v in six.iteritems(counter1):
            result += min(v, counter2[k])
        return result

    def _safe_divide(self, numerator, denominator):
        if denominator > 0:
            return numerator / denominator
        else:
            return 0

    def _safe_f1(self, matches, recall_total, precision_total, alpha):
        recall_score = self._safe_divide(matches, recall_total)
        precision_score = self._safe_divide(matches, precision_total)
        denom = (1.0 - alpha) * precision_score + alpha * recall_score
        if denom > 0.0:
            return (precision_score * recall_score) / denom
        else:
            return 0.0

    def rouge_n(self, peer, models, n, alpha):
        """
        Compute the ROUGE-N score of a peer with respect to one or more models, for
        a given value of `n`.
        """
        matches = 0
        recall_total = 0
        peer_counter = self._ngram_counts(peer, n)
        for model in models:
            model_counter = self._ngram_counts(model, n)
            matches += self._counter_overlap(peer_counter, model_counter)
            recall_total += self._ngram_count(model, n)
        precision_total = len(models) * self._ngram_count(peer, n)
        return self._safe_f1(matches, recall_total, precision_total, alpha)

    def rouge_1(self, peer, models, alpha):
        """
        Compute the ROUGE-1 (unigram) score of a peer with respect to one or more
        models.
        """
        return self.rouge_n(peer, models, 1, alpha)

    def rouge_2(self, peer, models, alpha):
        """
        Compute the ROUGE-2 (bigram) score of a peer with respect to one or more
        models.
        """
        return self.rouge_n(peer, models, 2, alpha)

    def rouge_3(self, peer, models, alpha):
        """
        Compute the ROUGE-3 (trigram) score of a peer with respect to one or more
        models.
        """
        return self.rouge_n(peer, models, 3, alpha)

    def lcs(self, a, b):
        """
        Compute the length of the longest common subsequence between two sequences.

        Time complexity: O(len(a) * len(b))
        Space complexity: O(min(len(a), len(b)))
        """
        # This is an adaptation of the standard LCS dynamic programming algorithm
        # tweaked for lower memory consumption.
        # Sequence a is laid out along the rows, b along the columns.
        # Minimize number of columns to minimize required memory
        if len(a) < len(b):
            a, b = b, a
        # Sequence b now has the minimum length
        # Quit early if one sequence is empty
        if len(b) == 0:
            return 0
        # Use a single buffer to store the counts for the current row, and
        # overwrite it on each pass
        row = [0] * len(b)
        for ai in a:
            left = 0
            diag = 0
            for j, bj in enumerate(b):
                up = row[j]
                if ai == bj:
                    value = diag + 1
                else:
                    value = max(left, up)
                row[j] = value
                left = value
                diag = up
        # Return the last cell of the last row
        return left

    def rouge_l(self, peer, models, alpha):
        """
        Compute the ROUGE-L score of a peer with respect to one or more models.
        """
        matches = 0
        recall_total = 0
        for model in models:
            matches += self.lcs(model, peer)
            recall_total += len(model)
        precision_total = len(models) * len(peer)
        return self._safe_f1(matches, recall_total, precision_total, alpha)
