#! /usr/bin/python 

__author__ = "Haibo Jin"

from __future__ import division 
from collections import defaultdict
import math 

#build a simple bigram language model 
#be able to be tested on a testing data, compute the perplexity, and give the most likely word given its previous word 

class Bigram():
    def __init__(self):
        self.text = None 
        self.bigrams = None 
        self.fdist1 = defaultdict(int)
        self.fdist2 = defaultdict(int)
        self.words_num = 0

    def read_text(self, training_data):
        """reading text from given source"""
        train_file = open(training_data, 'rb')
        self.text = train_file.read().split()
        train_file.close()
        self.text = [word.lower() for word in self.text]
        self.words_num = len(self.text)
        self.bigrams = zip(self.text[:-1], self.text[1:])

    def build_fdist(self):
        """build frequency distributions of the text and bigrams."""
        for word in self.text:
            self.fdist1[word] += 1
        for (w1, w2) in self.bigrams:
            self.fdist2[(w1,w2)] += 1

    def get_count_single(self, word):
        """get the count of a given word"""
        print self.fdist1[word]

    def get_count_double(self, t):
        """get the count of the given two words"""
        print self.fdist2[t]

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
        p = 1.0
        for n in range(len(uni_sent[:-1])):
            if self.fdist1[uni_sent[n]]==0: self.fdist1[uni_sent[n]] = 1
            if self.fdist2[bi_sent[n]]==0: self.fdist2[bi_sent[n]] = 1
            p *= self.fdist2[bi_sent[n]]*1.0 / self.fdist1[uni_sent[n]]
        return p

if __name__ == '__main__':
    bigram = Bigram() 
    bigram.read_text('training_data2')
    bigram.build_fdist()
    bigram.get_count_single('the')
    bigram.get_count_double(('it','is'))
    print "perplexity:", bigram.perplexity('testing_data2')
