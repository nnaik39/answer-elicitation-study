import json 
import random 

f = open('pilot_exp.json')
 
# returns JSON object as
# a dictionary
pilot_exp = json.load(f)

f = open('ig-vqa-default-rtdb-answer-elicitation-study-gpt4-descriptions-export.json')
study_info = json.load(f)
new_pilot_exp = {}
new_pilot_exp['images'] = []

questions_per_image_context_pair = {}

for participant in study_info:
    for trial in study_info[participant]:
        if ((trial['picture'], trial['category']) not in questions_per_image_context_pair):
            questions_per_image_context_pair[(trial['picture'], trial['category'])] = 0
        questions_per_image_context_pair[(trial['picture'], trial['category'])] += 2

        if (trial['comments'] != ''):
            print(trial['comments'])
        if (trial['glb_comments'] != ''):
            print(trial['glb_comments'])

images_left = []

for i in pilot_exp['images']:
    if ((i['filename'], i['category']) in questions_per_image_context_pair and questions_per_image_context_pair[(i['filename'], i['category'])] >= 3):
        print("Image ", i['filename'])
    else:
        images_left.append((i['filename'], i['category']))
        new_pilot_exp['images'].append(i)

images_left = list(set(images_left))
print("Number of images left ", len(images_left))

json_object = json.dumps(new_pilot_exp, indent=4)
 
# Writing to sample.json
with open("new_pilot_exp.json", "w") as outfile:
    outfile.write(json_object)