#! /usr/bin/python 

__author__ = "Haibo Jin"

import json

#part1, exercise of week3, from coursera NLP course lectured by Michael Collins
#a program which can replace the infrequent words(count < 5) by symbol _RARE_, in the parse_train.dat


def replace_infreq(filename):
    """replace the infrequent words(count < 5) by symbol _RARE_, given the target file, based on 'cfg.counts'."""
    #getting counts from cfg.counts 
    file_in = open('cfg.counts', 'rb')
    file_out = open('parse_train2.dat', 'wb')
    #recording rare words 
    rare = set()
    #for a specific word, summing the counts of all different kinds of POS
    rare_sum = {}
    for line in file_in:
        line = line.split()
        if line[1] == 'UNARYRULE':
            if line[3] in rare_sum: rare_sum[line[3]] += int(line[0])
            else: rare_sum[line[3]] = int(line[0])

    #choosing those words with less than 5 counts 
    for key in rare_sum.keys():
        if rare_sum[key] < 5:
            rare.add(key)
    file_in.close()

    #replace the rare words in target file 
    file_in = open(filename, 'rb')
    for tree in file_in:
        tree = json.loads(tree)
        tree_new = tree_replace(tree, rare)
        tree_new = json.dumps(tree_new)
        file_out.write(tree_new + '\n')


def tree_replace(tree, rare):
    """based on given rare words, replace the infrequent words in the given tree."""
    #recursively replace infrequent words 
    if isinstance(tree, list) and len(tree) == 3:
        new_1 = tree_replace(tree[1], rare)
        new_2 = tree_replace(tree[2], rare)
        return [tree[0], new_1, new_2]
    elif isinstance(tree, list) and len(tree) == 2:
        new = tree_replace(tree[1], rare)
        return [tree[0], new]
    else:
        if tree in rare: return '_RARE_'
        else: return tree
    

if __name__ == '__main__':
    replace_infreq('parse_train.dat')
