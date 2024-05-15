'''
This file checks coverage of questions in the experiment,
saves all completed datapoints to a new file, and fills 'new_pilot_exp.json'
with the datapoints that have yet to be covered.
'''

import json
from math import e
from random import shuffle

f = open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-answer-elicitation-study-dataset-expansion-export (44).json')
study_info = json.load(f)

questions_per_image_context_pair = {}
new_pilot_exp = {}
new_pilot_exp['images'] = []

f = open('pilot_exp.json')
pilot_exp = json.load(f)

answers = {}
collected_datapoints = []

# File storing all questions collected

for participant in study_info:
    for trial in study_info[participant]:
        if (trial['glb_comments'] != ''):
            print('GLB comments: ', trial['glb_comments'])
        if (trial['comments'] != ''):
            print(trial['comments'])
        found_in_pilot_exp = False 
        for pilot_exp_entry in pilot_exp['images']:
            if (trial['picture'] == pilot_exp_entry['filename'] and trial['category'] == pilot_exp_entry['category']
                and trial['description'] == pilot_exp_entry['description'] and trial['question'] == pilot_exp_entry['question']):
                    found_in_pilot_exp = True
        
        if (found_in_pilot_exp):
            if ((trial['picture'], trial['category'], trial['description'], trial['question']) not in answers):
                answers[(trial['picture'], trial['category'], trial['description'], trial['question'])] = []
            answers[(trial['picture'], trial['category'], trial['description'], trial['question'])].append(trial['answer'])

all_answers = {}

for participant in study_info:
    for trial in study_info[participant]:
            if ((trial['picture'], trial['category'], trial['description'], trial['question']) not in all_answers):
                all_answers[(trial['picture'], trial['category'], trial['description'], trial['question'])] = []
            all_answers[(trial['picture'], trial['category'], trial['description'], trial['question'])].append(trial['answer'])

questions_not_covered = []

questions_covered = []

images_not_covered = []

for (image, context, description, question) in answers:
    # Check if there are at least two unanswerable ratings!!
    unanswerable = False 
    if (answers[(image, context, description, question)].count('') >= 2):
        unanswerable = True 

    if (len(answers[(image, context, description, question)]) >= 3 or unanswerable):
        i = {
            'image': image,
            'context': context,
            'description': description,
            'question': question,
            'answers': answers[(image, context, description, question)]}
        collected_datapoints.append(i)
    else:
        new_pilot_exp['images'].append({
            'filename': image,
            'category': context,
            'description': description,
            'question': question
        })

# TODO: Add what hasn't been covered to the study as well!
for pilot_exp_entry in pilot_exp['images']:
    if (pilot_exp_entry['filename'], pilot_exp_entry['category'], pilot_exp_entry['description'], pilot_exp_entry['question']) not in answers:
        new_pilot_exp['images'].append({
            'filename': image,
            'category': context,
            'description': description,
            'question': question
        })

print("Length of new pilot exp ", len(new_pilot_exp['images']))

#print("Collected datapoints: ", collected_datapoints)

with open("new_pilot_exp.json", "w") as outfile:
    outfile.write(json.dumps(new_pilot_exp, indent = 4))

with open("collected_datapoints.json", "w") as outfile:
    outfile.write(json.dumps(collected_datapoints, indent = 4))