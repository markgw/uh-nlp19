# Day 7: Vectors and Lexical Semantics

Carry out all the exercises below
and submit your answers on
[Moodle](https://moodle.helsinki.fi/course/view.php?id=33565#section-5).
Also submit a single Python file containing your full implementation.  

## Exercise 0: Load the documents

For this exercise session, we will mostly be using these five 'documents'.
````python
documents = ['Wage conflict in retail business grows',
			 'Higher wages for cafeteria employees',
			 'Retailing Wage Dispute Expands',
			 'Train Crash Near Petershausen',
			 'Five Deaths in Crash of Police Helicopter']
````

## Exercise 1: Document-term matrix

In this exercise, we will build a simple document-term matrix for the documents in Exercise 0.

### Exercise 1.1: Step-by-step construction of the doc-term matrix
For each document, convert to lowercase, tokenize, remove stopwrods and then lemmatize.
For lemmatization, you can make use of the lemmatizer included in the NLTK library.
````python
from nltk.stem.wordnet import WordNetLemmatizer
lemma = WordNetLemmatizer()
lemma.lemmatize(word)
````
Construct a vocabulary for your corpus which is all the words that appear in the documents minus stopwords.
The shape of the matrix will be the no. of documents by the vocabulary size (n_docs x vocab_size).
What is the shape of your matrix?

Construct the document-term matrix by going through each document and checking if the vocabulary word is present or not.

### Exercise 1.2: Using scikit-learn to build the doc-term matrix

Scikit-learn actually has a method called the [CountVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html) to build document-term matrices easily and includes a number of options
such as removing stopwords, tokenizing, indicationg encoding (important for documents in other languages), and others.
At the bottom of the CountVectorizer page is a code snippet to build count vectors for each document. You can easily convert these to a binary doc-term matrix.

How does your doc-term matrix from 1.1 compare to your doc-term matrix from 1.2? Are they exactly the same or are their differences?
If they are different, what could account for these differences?

For the next exercises, we will make use the doc-term matrix with count vectors produced by the CountVectorizer.

## Exercise 2: Ranking documents by query

### Exercise 2.1: Using the dot product to rank documents

Suppose you have the query 'retail wages'. Rank the documents by relevance to this query by getting the dot product of the query by the doc-term matrix.
Which document is the most relevant to the query? Does it align with your intuition?

Normalize the count vectors by the document length and perform the same relevance ranking. Does it produce the same results?

### Exercise 2.2: Using TF-IDF to weight words

In the previous exercise, our doc-term matrix is composed of count vectors where each element in the vector is the number of times a word appeared in the document.
In this exercise, we will convert that doc-term matrix to a doc-term matrix composed of TF-IDF vectors.
Construct a TF-IDF doc-term matrix using the [TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html#sklearn.feature_extraction.text.TfidfVectorizer) from Scikit-learn.
Perform the same relevance ranking that we did in Exercise 2.1 by getting the dot product of the same query with your new TF-IDF doc-term matrix.
Does the ranking change? If there is a change in ranking, what do you think could account for this?


## Exercise 3: Finding similar documents

Using the doc-term matrix from Exercise 2.2, use cosine similarity for each document pair to find which two documents are most similar to each other.

Tip: The ````itertools```` package can produce the document pairs so you don't have to construct them yourselves.
Which document-pair are most similar to each other? How about the least similar? Does it follow your intuition.

Suppose you are given three new documents that you have not seen so far:

````python
new_docs = ['Plane crash in Baden-Wuerttemberg',
	'Bavaria comes up with model for tax-reform',
	'The weather']
`````
Construct the TF-IDF matrix for these unseen documents and find the documents from our original corpus that are most similar to each of these new documents
using cosine similarity. Which document is most similar to the first new document? How about the second one? And the third one?


## Exercise 4: Topic modelling

We will use the [Gensim package](https://radimrehurek.com/gensim/models/ldamodel.html) to perform topic modelling on a corpus of news articles. Topic modelling works better if we have more data.
We have provided the 'denews.txt' which consists of short news stories separated with tags.
Use the following method to separate the articles (you can also preprocess the articles to remove stopwords, punctuations, etc. if you want):
````python
def prepare_dataset(filename):
    articles = []
    text = open(filename,'r').read().split()
    index_start = list(np.where(np.array(text)=="<DOC")[0])
    for i in range(len(index_start)-1):
        start_art = index_start[i]+2
        end_art = index_start[i+1]
        article = text[start_art:end_art]
        articles.append(article)
    return articles
````

The most popular topic modelling method is LDA. The following lines will train a topic model for two topics using Gensim:
````python
from gensim.models import LdaModel
from gensim import corpora
common_dictionary = corpora.Dictionary(articles)
common_corpus = [common_dictionary.doc2bow(a) for a in articles]
# this line is the actual training part and might take a few minutes
n_topics = 2
lda = LdaModel(common_corpus, id2word=common_dictionary, num_topics=n_topics, passes=100)
# after training is done, we can check the top words of each topic
for k in range(n_topics):
	top_words = lda.show_topic(k, topn=5)
````

What are the top five words for each topic? Would you be able to describe in your own words what each topic is about?
Why or why not?
