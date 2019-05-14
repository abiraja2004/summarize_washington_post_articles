from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

# custom imports
import scrape


def summarize_wpost(url, n=5, tag='article'):
    '''This function accepts an article link from the Washington Post assuming they have not changed their HTML design and are tagging their article sections with the tag "article" and will scrape the text and use NLP to summarize the article into n sentences (which defaults to 5 sentences) and returns an array of those 5 sentences. This is particularly useful since Washington Post articles are subscription only and cannot be read for free.
    
    It utilizes a beautiful soup scraping helper function.'''

    # scrape the website for the raw text in our article.
    text = scrape.scrapeArticle(url, tag)

    # Tokenize the words and make them lower case
    tokenized_words = word_tokenize(text.lower())

    # Tokenize the sentences
    sents = sent_tokenize(text)

    # Assign stopwords.
    _stopwords = set(stopwords.words('english') + list(punctuation) + ['’', '‘', '“', '”', '—', 'has', 'was'])

    # create a list of words that are not in our stopwords.
    tokenized_words = [word for word in tokenized_words if word not in _stopwords]

    # Lemmatize and lower-case the words into our list of base words 
        # Lemmatization is the process of converting a word to its base form FROM the root form. It is more intelligent and looks for the MEANING behind the words. Uses a dictionary to look up the words and figures out the words are the same. 
    lemmatizer = WordNetLemmatizer()
    lemmatizedWords = [lemmatizer.lemmatize(word) for word in tokenized_words]

    # Create the frequency distribution of words so we know the ones that are most mentioned are the most important.
    freq = FreqDist(lemmatizedWords)

    print(nlargest(20, freq, key=freq.get)) # print this to see your K most weighted words - and then you can add more stop words to clean up the noise.

    # Using default dict, rank the tokenized sentences per the word frequency weights
    ranking = defaultdict(int) # This default dict is setting our first number as a default = 0 so you can add weights from our frequency distribution above if needed.
    for i, sent in enumerate(sents):
        for w in word_tokenize(sent.lower()): # for each word in our lower case sentences.
            if w in freq: # frequency dictionary from before. will only add the weight ONLY if the important word is in there. Otherwise, it's a 0 thanks to our default dictionary.
                ranking[i] += freq[w]

    # get the N most important sentence INDEXES:
    sents_idx = nlargest(n, ranking, key=ranking.get)

    # get the most important sentences SORTED (so they print in order for the user):
    final = [sents[j] for j in sorted(sents_idx)]

    return final



### TESTING THE FUNCTION:

# url = 'https://www.washingtonpost.com/news/style/wp/2019/05/09/feature/cindy-mccains-life-without-john/'

# summary = summarize_wpost(url)

# print(summary)