#! /usr/bin/python 

__author__ = "Haibo Jin"

import json 

#part2, exercise of week3, from coursera course lectured by Michael Collins 
#a parser based on CKY algorithm

def unary_prob_index(filename):
    """build an index which stores all the possibility of unary pairs, using MLE."""
    file_in = open(filename, 'rb')
    #storing counts of unary pairs(x -> w) 
    unary_pair = {}
    #storing counts for x
    unary_x = {}
    #getting counts
    for line in file_in:
        line = line.split()
        if line[1] == 'UNARYRULE':
            unary_pair[(line[2], line[3])] = int(line[0])
            if line[2] in unary_x: unary_x[line[2]] += int(line[0]) 
            else: unary_x[line[2]] = int(line[0])
    file_in.close()
    #calculte probabilities based on counts 
    for x,w in unary_pair:
        unary_pair[(x,w)] = unary_pair[(x,w)] * 1.0 / unary_x[x]

    return unary_pair

def unary_prob(x, w, unary_pair, words):
    """calculate the probability of w, given x, based on previous builded index"""
    #if no matching word, just return 0
    if (x,w) in unary_pair:
        return unary_pair[(x,w)]
    elif w not in words and (x,'_RARE_') in unary_pair:
        return unary_pair[(x,'_RARE_')]
    else:
        return 0.0

def binary_prob_index(filename):
    """build an index which stores all the possibility of binary pairs, usinf MLE."""
    file_in = open(filename, 'rb')
    #storing counts for binary pairs(x -> y1y2)
    binary_pair = {}
    #storing counts for x
    binary_x = {}
    #getting counts 
    for line in file_in:
        line = line.split() 
        if line[1] == 'BINARYRULE':
            binary_pair[(line[2], line[3], line[4])] = int(line[0])
            if line[2] in binary_x: binary_x[line[2]] += int(line[0])
            else: binary_x[line[2]] = int(line[0])
    file_in.close()
    #calculate probabilities based on counts 
    for x,y1,y2 in binary_pair:
        binary_pair[(x,y1,y2)] = binary_pair[(x,y1,y2)] * 1.0 / binary_x[x]

    return binary_pair

def binary_prob(x, y1, y2, binary_pair):
    """calculate the probability of y1 and y2, given x, based on previous builded index."""
    return binary_pair[(x,y1,y2)]

def nonterminal_set(filename):
    """return the set of all non-terminals."""
    file_in = open(filename, 'rb')
    s = set()
    for line in file_in:
        line = line.split()
        if line[1] == 'NONTERMINAL':
            s.add(line[2])
    file_in.close()
    return s
            
def cky_parsing(sentence, non_terminals, unary_pair, binary_pair):
    """using dynamic programming to implememnt CKY parsing algorithm. Given target sentence and PCFG model, output the most possible parse tree."""
    sentence = sentence.split()
    #storing the maximum probability for non-terminal X, spanning from i to j
    pi_table = {}
    #storing tne best position of pi_table
    bp_table = {}

    #get the set of all words in training data
    words = set()
    for x, w in unary_pair:
        words.add(w)

    #initialization of the dynamic table
    for i in range(0, len(sentence)):
        for x in non_terminals:
            pi_table[(i,i,x)] = unary_prob(x, sentence[i], unary_pair, words)

    #CKY algorithm 
    for l in range(1, len(sentence)):
        for i in range(0, len(sentence)-l):
            j = i + l
            #go through the binary pairs
            for (x,y,z) in binary_pair:
                for s in range(i, j):
                    p = binary_prob(x, y, z, binary_pair) * pi_table[(i,s,y)] * pi_table[(s+1,j,z)]
                    if (i,j,x) not in pi_table: 
                        pi_table[(i,j,x)] = p 
                        bp_table[(i,j,x)] = ((i,s,y), (s+1,j,z))
                    else:
                        if p > pi_table[(i,j,x)]:
                            pi_table[(i,j,x)] = p 
                            bp_table[(i,j,x)] = ((i,s,y), (s+1,j,z))
            #add upp those non_terminals x that not in binary_pair
            for x_ in non_terminals:
                if (i,j,x_) not in pi_table: pi_table[(i,j,x_)] = 0.0

    return bp_table

def build_parse_tree(sentence, bp_table, start, end, start_symbol):
    """given the target sentence, build a parse tree for it based on the bp_table."""
    #for binary rule, keep passing its children to next recursion
    if (start,end,start_symbol) in bp_table:
        #left_index is the first tuple in bp_table
        left_index = bp_table[(start,end,start_symbol)][0]
        left = build_parse_tree(sentence, bp_table, left_index[0], left_index[1], left_index[2])
        #right_index is the second tuple in bp_table
        right_index = bp_table[(start,end,start_symbol)][1]
        right = build_parse_tree(sentence, bp_table, right_index[0], right_index[1], right_index[2])
        return [start_symbol, left, right]
    #for unary rule, directly return them
    else:
        return [start_symbol, sentence[start]]

def write_tree(filename, unary_pair, binary_pair, non_terminals,  start_symbol):
    """for every line in the given file, build its parse tree and write it into file using json."""
    file_in = open(filename, 'rb')
    file_out = open('parse_dev.out', 'wb')
    for line in file_in:
        bp_table = cky_parsing(line, non_terminals, unary_pair, binary_pair)
        tree = build_parse_tree(line.split(), bp_table, 0, len(line.split())-1, start_symbol)
        tree = json.dumps(tree)
        file_out.write(tree + '\n')
    file_out.close()

if __name__ == '__main__':
    unary_pair = unary_prob_index('parse_train.counts.out')
    binary_pair = binary_prob_index('parse_train.counts.out')
    non_terminals = nonterminal_set('parse_train.counts.out')
    write_tree('parse_dev.dat', unary_pair, binary_pair, non_terminals, 'SBARQ')
    




