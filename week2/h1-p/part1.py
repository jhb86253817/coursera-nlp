#! /usr/bin/python 

__author__ = "Haibo Jin"

import operator

#part1, exercise of week2, from coursera course NLP lectured by Michael Collins
#POS tagging with a simple tagger and some preprocessing for later use

def replace_infreq():
    """map infrequent words whcih has less than 5 counts in the training data to a common class named _RARE_"""
    #find the rare words
    file_in = open('gene.counts', 'rb')
    words_counts = {}
    for line in file_in:
        line = line.split()
        if line[1] == 'WORDTAG':
            if line[-1] in words_counts: words_counts[line[-1]] += int(line[0])
            else: words_counts[line[-1]] = int(line[0])
    file_in.close()
    rare_words = set()
    for key in words_counts:
        if words_counts[key] < 5: rare_words.add(key)
    #replace the rare words in training data
    file_in = open('gene.train', 'rb')
    file_out = open('gene.train2', 'wb')
    for line in file_in:
        line = line.split()
        if line and line[0] in rare_words:
            line[0] = '_RARE_'
        file_out.write(' '.join(line)+'\n')
    file_in.close()
    file_out.close()

def pre_emission():
    """calculate emission probability for all the x,y pairs in gene.counts2, and build an index for it."""
    emission_index = {}
    file_in = open('gene.counts2', 'rb')
    count_o = 0
    count_gene = 0
    for line in file_in:
        line = line.split()
        if line[1] == 'WORDTAG':
            emission_index[(line[3], line[2])] = int(line[0])
            if line[2] == 'O': count_o += int(line[0])
            else: count_gene += int(line[0])
    file_in.close()
    for (x,y) in emission_index:
        if y == 'O': emission_index[(x,y)] = emission_index[(x,y)] * 1.0 / count_o
        if y == 'I-GENE': emission_index[(x,y)] = emission_index[(x,y)] * 1.0 / count_gene
    return emission_index

def emission(x, emission_index):
    """calculate the emission probability of given x, for both O and I-GENE ."""
    if (x,'O') not in emission_index.keys() and (x,'I-GENE') not in emission_index.keys():
        return emission_index[('_RARE_','O')], emission_index[('_RARE_','I-GENE')]
    elif (x,'O') in emission_index.keys() and (x,'I-GENE') not in emission_index.keys():
        return emission_index[(x,'O')], 0
    elif (x,'O') not in emission_index.keys() and (x,'I-GENE') in emission_index.keys():
        return 0, emission_index[(x,'I-GENE')]
    else:
        return emission_index[(x,'O')], emission_index[(x, 'I-GENE')]
    
def simple_tagger(filename):
    """a simple tagger that choose y which maximize the emission probability for x."""
    emission_index = pre_emission()
    file_in = open(filename, 'rb')
    file_out = open('gene_test.p1.out', 'wb')
    for word in file_in:
        word = word.strip()
        if not word: 
            file_out.write('\n')
            continue
        emission_o, emission_gene = emission(word, emission_index)
        if emission_o > emission_gene:
            word_tagged = word + ' O'
        else:
            word_tagged = word + ' I-GENE'
        file_out.write(word_tagged + '\n')
    file_in.close()
    file_out.close()

if __name__ == '__main__':
    #replace_infreq()
    simple_tagger('gene.test')



