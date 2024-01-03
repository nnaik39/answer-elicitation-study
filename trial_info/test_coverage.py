import json 
import random 

f = open('best_questions.json')
 
# returns JSON object as
# a dictionary
pilot_exp = json.load(f)

f = open('dataset_annotations_so_far.json')
dataset = json.load(f)

questions_per_image_context_pair = {}

new_pilot_exp = {}
new_pilot_exp['images'] = []

for image_question_pair in pilot_exp['images']:
    print("i ", image_question_pair)

    found_in_dataset = False

    for data in dataset:
        if (data['image'] == image_question_pair['filename'] and data['context'] == image_question_pair['category'] and data['question'] == image_question_pair['question']):
            found_in_dataset = True

    if (not found_in_dataset):
        new_pilot_exp['images'].append(image_question_pair)
 
# Writing to sample.json

# Take out any questions from new_pilot_exp that already have three or more hits in the trial data!
        
f = open('ig-vqa-default-rtdb-answer-elicitation-study-gpt4-descriptions-export.json')
study_info = json.load(f)

questions_per_image_context_pair = {}

answers = {}

for participant in study_info:
    for trial in study_info[participant]:
        if ((trial['picture'], trial['category'], trial['question']) not in questions_per_image_context_pair):
            questions_per_image_context_pair[(trial['picture'], trial['category'], trial['question'])] = 0
        questions_per_image_context_pair[(trial['picture'], trial['category'], trial['question'])] += 1

        if ((trial['picture'], trial['category'], trial['description'], trial['question']) not in answers):
            answers[(trial['picture'], trial['category'], trial['description'], trial['question'])] = []

        answers[(trial['picture'], trial['category'], trial['description'], trial['question'])].append(trial['answer'])

for (image, context, description, question) in answers:
    if (len(answers[(image, context, description, question)]) >= 3):
        i = {
            'image': image,
            'context': context,
            'description': description,
            'question': question,
            'answers': answers[(image, context, description, question)]}
        
exit()

with open("new_pilot_exp.json", "w") as outfile:
    outfile.write(json.dumps(new_pilot_exp))

f = open('ig-vqa-default-rtdb-answer-elicitation-study-gpt4-descriptions-export.json')
study_info = json.load(f)
new_pilot_exp = {}
new_pilot_exp['images'] = []

questions_per_image_context_pair = {}

dataset = []

answers = {}

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

        if ((trial['picture'], trial['category'], trial['description'], trial['question']) not in answers):
            answers[(trial['picture'], trial['category'], trial['description'], trial['question'])] = []

        answers[(trial['picture'], trial['category'], trial['description'], trial['question'])].append(trial['answer'])

for (image, context, description, question) in answers:
    if (len(answers[(image, context, description, question)]) >= 3):
        i = {
            'image': image,
            'context': context,
            'description': description,
            'question': question,
            'answers': answers[(image, context, description, question)]}

# Write this dataset to a JSON file!
json_object = json.dumps(dataset, indent=4)
 
# Writing to sample.json
with open("need_based_vqa_new.json", "w") as outfile:
    outfile.write(json_object)

images_left = []

covered_questions = 0

num_one_hit_questions = 0

answers = {}

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
#            new_pilot_exp['images'].append(i)
            num_one_hit_questions += 1

images_left = list(set(images_left))
print("Number of images left ", len(images_left))

print("Number of covered questions ", covered_questions)
json_object = json.dumps(new_pilot_exp, indent=4)
 
# Writing to sample.json
with open("new_pilot_exp.json", "w") as outfile:
    outfile.write(json_object)