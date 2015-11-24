#! /usr/bin/env python

import pycorpora as pc
import sys, codecs
from textblob import TextBlob
from random import choice

#using Jabba Laci's Markov Chain code: https://pythonadventures.wordpress.com/2014/01/23/generating-pseudo-random-text-using-markov-chains/
EOS = ['.', '?', '!']
def build_dict(words):
    d = {}
    for i, word in enumerate(words):
        try:
            first, second, third = words[i], words[i+1], words[i+2]
        except IndexError:
            break
        key = (first, second)
        if key not in d:
            d[key] = []
        #
        d[key].append(third)

    return d

def generate_sentence(d):
    li = [key for key in d.keys() if key[0][0].isupper()]
    key = choice(li)

    li = []
    first, second = key
    li.append(first)
    li.append(second)
    while True:
        try:
            third = choice(d[key])
        except KeyError:
            break
        li.append(third)
        if third[-1] in EOS:
            break
        # else
        key = (second, third)
        first, second = key

    return ' '.join(li)

def count_words(text):
    wordcounts={}
    for w in text.split():
        if w not in wordcounts:
            wordcounts[w] = 1
        else:
            wordcounts[w] += 1
    return wordcounts

def replace_nouns(text, wordlist):
    blob = TextBlob(text)
    nouns = [b[0] for b in blob.tags if 'NN' in b[1] and b[0] != 'O' and b[0] != 'men']
    nouns = list(set(nouns))
    wc = count_words(text)
    nouns = [k for k,v in wc.items() if v > 1 and k in nouns]
    for word in nouns:
        text = text.replace(word, choice(wordlist))
    return text

def get_random_corpus():
    d = choice(pc.get_categories())
    dict = pc.get_file(d, choice(pc.get_files(d)))
    global title
    for k,v in dict.items():
        if k == 'description':
            if 'List' in v or 'list' in v:
                v = v.replace('list', 'Marriage')
                v = v.replace('List', 'Marriage')
                title = '##'+v
            else:
                title = '##The Marriage of '+v
        else:
            corpus = list(v)
    return title, corpus

commonprayer = open("commonprayer.txt", "r").read()

ceremonies = []
for y in range(0,100):
    ceremony = None
    while ceremony is None:
        try:
            t, c = get_random_corpus()
            ceremony = replace_nouns(commonprayer, c)
        except TypeError:
             pass

    d = build_dict(ceremony.split())

    ceremonies.append(t+'\n\n')
    for x in range(0,20):
        ceremonies.append(generate_sentence(d)+'\n')
    ceremonies.append('\n')

with codecs.open('ceremony.md', 'wb', 'utf8') as output:
    output.writelines(ceremonies)
