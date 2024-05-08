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

word_depths_each_context = []

for entry in dataset:
    answers = entry['answers']
    context = entry['context']
    
    if (context not in avg_depth_in_context):
        avg_depth_in_context[context] = []
    
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
            
            avg_depth_in_context[context].append()
            num_words_per_context[context] += 1

print("Average depth across contexts: ", avg_depth_in_context)

# Print "Average depth from the root of every noun in each caption to measure referring expressions"
