#! /usr/bin/python 

__author__ = "Haibo Jin"

import operator 
import part1 

#part2, exercise of week2, from coursera course NLP lectured by Michael Collins
#POS tagging with HMM model

def pre_prob():
    """calculate the probability for all the pairs of grams permutations"""
    prob_index = {}
    file_in = open('gene.counts2', 'rb')
    for line in file_in:
        line = line.split()
        if line[1] == '1-GRAM':
            prob_index[line[2]] = int(line[0])
        elif line[1] == '2-GRAM':
            prob_index[(line[2], line[3])] = int(line[0])
        elif line[1] == '3-GRAM':
            prob_index[(line[2], line[3], line[4])] = int(line[0])
    file_in.close()
    return prob_index       

def trigram_prob(y1, y2, y3, prob_index):
    """calculate the probability of y3 given y1 and y2."""
    return prob_index[(y1,y2,y3)] * 1.0 / prob_index[(y1,y2)]

def tagger_set(index):
    """return the tagger set of a given index."""
    s = ['O', 'I-GENE']
    if int(index) == 0 or int(index) == -1:
        return ['*']
    else:
        return s

def sent_tagger(sent):
    """calculate the most possible sequence of tags given a sentence, using viterbi algorithm."""
    #a table storing the maximum probability ending with specific two letters in specific position.
    pi_table = {}
    pi_table[(0, '*', '*')] = 1
    #a table storing the best w which maximize the probability of trigram
    bp_table = {}
    #calculate the probability of trigram in advance
    prob_index = pre_prob()
    #calculate the emission probability in advance
    emission_index = part1.pre_emission()

    #finding most possible pair for certain positions with dynamic programming
    for k in range(1, len(sent)+1):
        for u in tagger_set(k-1):
            for v in tagger_set(k):
                for w in tagger_set(k-2):
                    q = trigram_prob(w, u, v, prob_index)
                    emission_o, emission_gene = part1.emission(sent[k-1], emission_index)
                    if v == 'O': e = emission_o
                    else: e = emission_gene
                    if (k, u, v) not in pi_table.keys():
                        pi_table[(k, u, v)] = pi_table[(k-1, w, u)] * q * e
                        bp_table[(k, u, v)] = w
                    else:
                        if pi_table[(k-1, w, u)] * q * e > pi_table[(k, u, v)]:
                            pi_table[(k, u, v)] = pi_table[(k-1, w, u)] * q * e
                            bp_table[(k, u, v)] = w
                            
    #for the last two words, find the most possible taggers
    max_y = 0
    for u in tagger_set(len(sent)-1):
        for v in tagger_set(len(sent)):
            r = pi_table[(len(sent), u, v)] * trigram_prob(u, v, 'STOP', prob_index)
            if r > max_y:
                max_y = r
                y = [u, v]

    #find the most possible taggers of the sentence based on bp_table 
    for k in range(len(sent)-2, 0, -1):
        y_k = bp_table[(k+2, y[0], y[1])]
        y = [y_k] + y
                
    return zip(sent, y)

def hmm_tagger(filename):
    """a HMM pos tagger which uses MLE to estimate parameters."""
    file_in = open(filename, 'rb')
    file_out = open('gene_dev.p2.out', 'wb')
    sent = []
    for word in file_in:
        word = word.strip()
        if not word:
            sent_tagged = sent_tagger(sent)
            for (w, t) in sent_tagged:
                file_out.write(str(w) + ' ' + str(t) + '\n')
            file_out.write('\n')
            sent = []
            continue
        sent = sent + [word]
    file_in.close()
    file_out.close()


if __name__ == '__main__':
    prob_index = pre_prob()
    print trigram_prob('O', 'O', 'STOP', prob_index)
    sent = "heart disease is the primary cause of morbidity and mortality among".split()
    y = sent_tagger(sent)
    print y

    hmm_tagger('gene.dev')
