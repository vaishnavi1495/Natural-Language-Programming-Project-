from nltk.corpus import wordnet as wn
import pysolr
import os
import nltk
import nltk.tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from rake_nltk import Rake
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

# URL of SOLR with core mentioned as task1
server = pysolr.Solr('http://localhost:8983/solr/task1/', timeout=100000)

# create Lemmatizer to get different inflected forms of a lemma
create_lemma = WordNetLemmatizer()
# crate Stemmer to get derivationally related words
create_stem = LancasterStemmer()
# Rapid Automatic Keyword Extraction algorithm
# uses stopwords for english from NLTK & all punctuation characters
r = Rake()


def build_features(sentence, index):
    tokens = word_tokenize(sentence)
    hypernym_of_word = []
    hyponym_of_word = []
    pos_of_sentence = []
    lemma_of_sentence = []
    stem_of_sentence = []
    # determine key phrases by analyzing the frequency of word
    # appearance and its co-occurrence with other words in the text
    r.extract_keywords_from_text(sentence)
    # To get keyword phrases ranked highest to lowest.
    ranked_phrases = r.get_ranked_phrases()
    # Consider only top 6 phrases
    top_phrases = ranked_phrases[0:6]

    for token in tokens:
        synsets = wn.synsets(token)
        for synset in synsets:
            # If hypernyms are available then extract it and only save first most common Hypernym
            if len(synset.hypernyms()) > 0:
                hypernym_of_synset = synset.hypernyms()
                hypernym_of_word.append(hypernym_of_synset[0].name())
            # If hyponyms are available then extract it and only save first most common Hyponym
            if len(synset.hyponyms()) > 0:
                hyponym_of_synset = synset.hyponyms()
                hyponym_of_word.append(hyponym_of_synset[0].name())

        # Extract Lemma of each word
        lemma_of_sentence.append(create_lemma.lemmatize(token))
        # Extract Stem words of each token
        stem_of_sentence.append(create_stem.stem(token))
    # Extract POS tags using nltk
    for pos_tag in nltk.pos_tag(tokens):
        pos_of_sentence.append(pos_tag[0] + "|" + pos_tag[1])
    # NLP features Data which will be added as index on SOLR
    doc = {
        "id": index,
        "sentence": sentence,
        "lemma": lemma_of_sentence,
        "stem": stem_of_sentence,
        "hypernym": hypernym_of_word,
        "hyponym": hyponym_of_word,
        "pos": pos_of_sentence,
        "words": tokens,
        "phrases": top_phrases
    }
    return doc


def semantic_search():
    input_sen = input("Please, Enter the Query to perform semantic search on it. \n")
    # Extract all the NLP features regarding user input Query
    doc = build_features(input_sen, 0)
    tryq = []
    q = ""
    for key, value in doc.items():
        if key != "id" and key != "sentence":
            for v in value:
                q += key + ":" + v + " || "
            q = q[:-4]
            print(q)
            tryq.append(q)
            q = ""
    # Format the query in the required format for SOLR
    new_query = ' || '.join(item for item in tryq)
    print("Following query will be searched on SOLR :")
    print(new_query)
    # Search the new query which contains all NLP features using SOLR
    output = server.search(new_query)
    print("----------------------------------------------------------------------------------------------------------")
    for data in output:
        print(data['id'] + " " + data['sentence'][0])


def create_index():
    number_of_words = 0
    number_of_sentences = 0
    documents = []
    # The path to the corpus
    corpus_file = input("Please, Enter A Corpus File Path : ")
    # "C:/Users/bhosa/Desktop/NLP/Project/Reuter/corpus/"
    print("Creating the Index on Corpus. Happy Searching!")
    for file in os.listdir(corpus_file):
        f = open(corpus_file + '/' + file)
        # Read the file content from the path given
        raw = f.read()
        # Tokenize the data to sentences
        sentence = sent_tokenize(raw)
        s = 1
        for sen in sentence:
            number_of_sentences += 1
            # Tokenize the sentences to words
            words = word_tokenize(sen)
            # Calculate the count of words for the information purposes
            number_of_words += len(words)
            # Unique Id is the file name with sentence count
            index = str(file) + "|" + str(s)
            # Extract all the NLP features associated with the sentence
            doc = build_features(sen, index)
            documents.append(doc)
            s += 1
        f.close()

    print("Total Words:", number_of_words)
    # Add the NLP features Data to SOLR as index using which SOLR will search the data
    server.add(documents)


if __name__ == '__main__':
    create_index()
    print("Data successfully added to SOLR")
    semantic_search()
