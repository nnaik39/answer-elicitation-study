import json 
import random 

f = open('pilot_exp copy.json')
 
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
        if ((trial['picture'], trial['category'], trial['question']) not in questions_per_image_context_pair):
            questions_per_image_context_pair[(trial['picture'], trial['category'], trial['question'])] = 0
        questions_per_image_context_pair[(trial['picture'], trial['category'], trial['question'])] += 1

        print("Number of questions ", questions_per_image_context_pair[(trial['picture'], trial['category'], trial['question'])])

        if (trial['comments'] != ''):
            print(trial['comments'])
        if (trial['glb_comments'] != ''):
            print(trial['glb_comments'])

images_left = []

covered_questions = 0

# Add in ten questions with at least one hit here!

num_one_hit_questions = 0

for i in pilot_exp['images']:
    if ((i['filename'], i['category'], i['question']) in questions_per_image_context_pair and questions_per_image_context_pair[(i['filename'], i['category'], i['question'])] >= 3):
        print("Excluding image ", i['filename'])
        covered_questions += 1
    else:
        if ((i['filename'], i['category'], i['question']) in questions_per_image_context_pair):
            print("Number of hits left ", questions_per_image_context_pair[(i['filename'], i['category'], i['question'])])

        images_left.append((i['filename'], i['category'], i['question']))

        if ((i['filename'], i['category'], i['question']) in questions_per_image_context_pair and questions_per_image_context_pair[(i['filename'], i['category'], i['question'])] == 2):
            new_pilot_exp['images'].append(i)

        if ((i['filename'], i['category'], i['question']) in questions_per_image_context_pair and questions_per_image_context_pair[(i['filename'], i['category'], i['question'])] == 1 and num_one_hit_questions < 10):
            new_pilot_exp['images'].append(i)
            num_one_hit_questions += 1

images_left = list(set(images_left))
print("Number of images left ", len(images_left))

print("Number of covered questions ", covered_questions)
json_object = json.dumps(new_pilot_exp, indent=4)
 
# Writing to sample.json
with open("new_pilot_exp.json", "w") as outfile:
    outfile.write(json_object)