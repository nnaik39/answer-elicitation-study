from nltk.corpus import wordnet
from nltk import word_tokenize
import nltk 
import pandas as pd
import json 

f = open('dataset_annotations_so_far.json')

dataset = json.load(f)
total_answers_per_context = {}
max_depth_in_context = {}
avg_depth_in_context = {}
num_words_per_context = {}

for entry in dataset:
    answers = entry['answers']
    context = entry['context']
    
    if (context not in avg_depth_in_context):
        avg_depth_in_context[context] = 0
    if (context not in num_words_per_context):
        num_words_per_context[context] = 0 
    
    avg_depth = 0

    for answer in answers:
        text = word_tokenize(answer)
        pos_tags = nltk.pos_tag(text)

        for (word, tag) in pos_tags:
            if ('NN' not in tag):
                continue 
            if (len(wordnet.synsets(word)) == 0):
                continue 
            min_depth = wordnet.synsets(word)[0].min_depth()
            avg_depth_in_context[context] += min_depth
            num_words_per_context[context] += 1

    print("Answer ", answer)
    print("Avg depth ", avg_depth)
