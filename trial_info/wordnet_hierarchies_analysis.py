from nltk.corpus import wordnet
from nltk import word_tokenize
import nltk 
import pandas as pd

import json 

df = pd.read_csv('dataset_annotations_so_far.csv')

# Hypernyms of dog
print('Hypernyms ', wordnet.synset('people.n.01').hypernyms())
print('Hyponyms ', wordnet.synset('person.n.01').hyponyms())

# Measure the mean words from each answer, and then the max word depth for each answer

total_answers_per_context = {}
max_depth_in_context = {}
avg_depth_in_context = {}

for row in df.iterrows():
    answers = [row['answer1'], row['answer2'], row['answer3']]
    context = row['context']
    
    if (context not in max_depth_in_context):
        max_depth_in_context[context] = 0
    if (context not in avg_depth_in_context):
        avg_depth_in_context = 0

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
            max_depth = max(max_depth, min_depth)

    avg_depth /= len(answer.split(' '))

    print("Answer ", answer)
    print("Avg depth ", avg_depth)
    print("Max depth ", max_depth)

# TODO: Count the number of answers in context as well here.
