#! /usr/bin/python 

__author__ = "Haibo Jin"

from __future__ import division
from collections import defaultdict
import math

#build a simple unigram language model
#be able to be tested on a testing data and compute the perplexity

class Unigram():
    def __init__(self):
        self.text = None
        self.fdist = defaultdict(int)
        self.words_num = 0

    def read_text(self, training_data):
        """reading text from given source"""
        train_file = open(training_data, 'rb')
        self.text = train_file.read().split()
        train_file.close()
        self.text = [word.lower() for word in self.text]
        self.words_num = len(self.text)

    def build_fdist(self):
        """build frequency distribution of the text"""
        for word in self.text:
            self.fdist[word] += 1

    def get_count(self, word):
        """get the count of a given word"""
        print self.fdist[word]

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
        sent = [word.lower() for word in sent.split()]
        p = 1.0
        for word in sent:
            if self.fdist[word]==0: self.fdist[word] = 1
            p *= self.fdist[word]*1.0 / self.words_num
        return p

if __name__ == '__main__':
    unigram = Unigram()
    unigram.read_text('training_data')
    unigram.build_fdist()
    #unigram.get_count('the')
    print "perplexity:", unigram.perplexity('testing_data')
