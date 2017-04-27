from nltk.corpus import wordnet as wn
from textblob import TextBlob
from textblob.en.parsers import PatternParser

# As pattern has no python 3 support we integrate spaghetti spanish POS tagger
# Code from https://github.com/alvations/spaghetti-tagger
from . import spaghetti as sgt


import re
import wikipedia

class Article:
    """Retrieves and analyzes wikipedia articles"""

    def __init__(self, title, lang):
        wikipedia.set_lang(lang)
        self.page = wikipedia.page(title)
        self.summary = TextBlob(self.page.summary)
        #print(self.page.content)

    def generate_trivia_sentences(self, lang):
        sentences = self.summary.sentences
        if lang=='es':
            # Trivial sentence tokenizer
            raw_sentences = self.page.summary.split('.')
            # Trivial word tokenizer
            raw_sentences = [x.split() for x in raw_sentences if len(x)>0]
            # Spanish POS tagger
            tagged = sgt.pos_tag_sents(raw_sentences)

            for i in range(len(sentences)):
                sentences[i].tags = tagged[i]
                sentences[i].noun_phrases = []
                sentences[i].words = [mytuple[0] for mytuple in tagged[i]]

        # Remove the first sentence - it's never a good one
        del sentences[0]

        trivia_sentences = []
        for sentence in sentences:
            trivia = self.evaluate_sentence(sentence, lang)
            if trivia:
                trivia_sentences.append(trivia)

        return trivia_sentences

    def get_similar_words(self, word):
        # In the absence of a better method, take the first synset
        synsets = wn.synsets(word, pos='n')

        # If there aren't any synsets, return an empty list
        if len(synsets) == 0:
            return []
        else:
            synset = synsets[0]

        # Get the hypernym for this synset (again, take the first)
        hypernym = synset.hypernyms()[0]

        # Get some hyponyms from this hypernym
        hyponyms = hypernym.hyponyms()

        # Take the name of the first lemma for the first 8 hyponyms
        similar_words = []
        for hyponym in hyponyms:
            similar_word = hyponym.lemmas()[0].name().replace('_', ' ')

            if similar_word != word:
                similar_words.append(similar_word)

            if len(similar_words) == 8:
                break

        return similar_words

    def evaluate_sentence(self, sentence, lang):
        if (sentence.tags[0][1] in ['RB','rg'] or len(sentence.words) < 6):
            # This sentence starts with an adverb or is less than five words long
            # and probably won't be a good fit
                return None

        tag_map = {word.lower(): tag for word, tag in sentence.tags}

        replace_nouns = []
        for word, tag in sentence.tags:
            # For now, only blank out non-proper nouns that don't appear in the article title
            if (lang =='en' and tag == 'NN') or (lang == 'es' and tag != None and tag.find('nc') == 0) and word not in self.page.title:
                # Is it in a noun phrase? If so, blank out the last two words in that phrase
                for phrase in sentence.noun_phrases:
                    if phrase[0] == '\'':
                        # If it starts with an apostrophe, ignore it
                        # (this is a weird error that should probably
                        # be handled elsewhere)
                        break

                    if word in phrase:
                        # Blank out the last two words in this phrase
                        [replace_nouns.append(phrase_word) for phrase_word in phrase.split()[-2:]]
                        break

                # If we couldn't find the word in any phrases,
                # replace it on its own
                if len(replace_nouns) == 0:
                    replace_nouns.append(word)
                break

        if len(replace_nouns) == 0:
            # Return none if we found no words to replace
            return None

        trivia = {
            'title': self.page.title,
            'url': self.page.url,
            'answer': ' '.join(replace_nouns)
        }

        if len(replace_nouns) == 1:
            # If we're only replacing one word, use WordNet to find similar words
            trivia['similar_words'] = self.get_similar_words(replace_nouns[0])
        else:
            # If we're replacing a phrase, don't bother - it's too unlikely to make sense
            trivia['similar_words'] = []

        # Blank out our replace words (only the first occurrence of the word in the sentence)
        replace_phrase = ' '.join(replace_nouns)
        blanks_phrase = ('__________ ' * len(replace_nouns)).strip()

        expression = re.compile(re.escape(replace_phrase), re.IGNORECASE)
        sentence = expression.sub(blanks_phrase, str(sentence), count=1)

        trivia['question'] = sentence
        return trivia
