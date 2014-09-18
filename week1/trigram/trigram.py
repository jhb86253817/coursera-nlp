#! /usr/bin/python 

__author__ = "Haibo Jin"

from __future__ import division 
from collections import defaultdict
import math 

#build a simple trigram language model 
#be able to be tested on a testing data and compute the perplexity

class Trigram():
    def __init__(self):
        self.text = None 
        self.bigrams = None 
        self.trigrams = None
        self.fdist1 = defaultdict(int)
        self.fdist2 = defaultdict(int)
        self.fdist3 = defaultdict(int)
        self.words_num = 0

    def read_text(self, training_data):
        """reading text from given source"""
        train_file = open(training_data, 'rb')
        self.text = train_file.read().split()
        train_file.close()
        self.text = [word.lower() for word in self.text]
        self.words_num = len(self.text)
        self.bigrams = zip(self.text[:-1], self.text[1:])
        self.trigrams = zip(self.text[:-2], self.text[1:-1], self.text[2:])

    def build_fdist(self):
        """build frequency distributions of the text and bigrams."""
        for word in self.text:
            self.fdist1[word] += 1
        for (w1, w2) in self.bigrams:
            self.fdist2[(w1,w2)] += 1
        for (w1, w2, w3) in self.trigrams:
            self.fdist3[(w1,w2,w3)] += 1

    def get_count_single(self, word):
        """get the count of a given word"""
        print self.fdist1[word]

    def get_count_double(self, t):
        """get the count of the given two words"""
        print self.fdist2[t]

    def get_count_trible(self, t):
        """get the count of the given three words."""
        print self.fdist3[t]

    def perplexity(self, testing_data):
        """calculate the perplexity of the model"""
        test_file = open(testing_data, 'rb')
        test_text = test_file.readlines()
        l = 0
        for sent in test_text:
            l += math.log(self.probability(sent))
        test_file.seek(0, 0)
        words_num = len(test_file.read().split())
        test_file.close()
        l = l * 1.0 / words_num
        return math.pow(2, -l) 

    def probability(self, sent):
        """calculate the probability of the given sentence."""
        uni_sent = [word.lower() for word in sent.split()]
        bi_sent = zip(uni_sent[:-1], uni_sent[1:])
        tri_sent = zip(uni_sent[:-2], uni_sent[1:-1], uni_sent[2:])
        p = 1.0
        for n in range(len(uni_sent[:-2])):
            if self.fdist2[bi_sent[n]]==0: self.fdist2[bi_sent[n]] = 1
            if self.fdist3[tri_sent[n]]==0: self.fdist3[tri_sent[n]] = 1
            p *= self.fdist3[tri_sent[n]]*1.0 / self.fdist2[bi_sent[n]]
        return p

if __name__ == '__main__':
    trigram = Trigram() 
    trigram.read_text('training_data3')
    trigram.build_fdist()
    trigram.get_count_single('the')
    trigram.get_count_double(('it','is'))
    print "perplexity:", trigram.perplexity('testing_data3')
