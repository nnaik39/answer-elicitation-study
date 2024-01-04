import json
import random 

f = open('dataset_annotations_so_far.json')
data = json.load(f)

new_dataset_annotations = []

for i in data:
    num_unanswerable_votes = 0

    for answer in i['answers']:
        if (answer == ''):
            num_unanswerable_votes += 1

    if (num_unanswerable_votes >= 2):
        continue

    # Take out all the unanswerable votes
    answers = [answer for answer in i['answers'] if answer != '']

    if (len(answers) > 3):
        clean_set_of_three_answers = random.sample(answers, 3)
        i['answers'] = clean_set_of_three_answers
    else:
        i['answers'] = answers 

    new_dataset_annotations.append(i)

with open('dataset_annotations_cleaned.json', 'w') as f:
    f.write(json.dumps(new_dataset_annotations, indent = 4))