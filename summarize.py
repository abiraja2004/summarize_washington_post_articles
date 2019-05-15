from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict
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

    # Assign stopwords manually from nltk corpus library:
    # _stopwords = set(stopwords.words('english') + list(punctuation) + ['’', '‘', "''", "'", '"', '""', '“', '”', '—', 'var', 'has', 'was', 'said'])
    
    corpus_stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

    _stopwords = set(corpus_stopwords + list(punctuation) + ['’', '‘', "''", "'", '"', '""', '“', '”', '—', 'var', 'has', 'was', 'said'])

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

    # get the most important sentences SORTED (so they print in order for the user) 
        # remove the sentence that don't have javascript scraped together in it:
        # remove sentences that say "Read more:"
    final = [sents[j] for j in sorted(sents_idx) if ('script.src' not in sents[j]) or ('read more:' not in sents[j])]

    return final



### TESTING THE FUNCTION:

# url = 'https://www.washingtonpost.com/news/style/wp/2019/05/09/feature/cindy-mccains-life-without-john/'

# summary = summarize_wpost(url)

# print(summary)