import json
import random 

#f = open('dataset_annotations_so_far.json')
f = open('ig-vqa-default-rtdb-answer-elicitation-study-gpt4-descriptions-export.json')
data = json.load(f)
f = open('correct_descriptions_each_image.json')
correct_descriptions = json.load(f)

new_dataset_annotations = []

all_answers_per_question = {}

for participant in data:
    for trial in data[participant]:
        image, context, description, question = trial['picture'], trial['category'], trial['description'], trial['question']
        if ((image, context, description, question) not in all_answers_per_question):
            all_answers_per_question[(image, context, description, question)] = []
        all_answers_per_question[(image, context, description, question)].append(trial['answer'])

full_answer_list = []

# Create a full answer list from this!
for (image, context, description, question) in all_answers_per_question:
    if (len(all_answers_per_question) >= 3 and (image not in correct_descriptions or description == correct_descriptions[image])):
        full_answer_list.append({
            'image': image,
            'context': context,
            'description': description,
            'question': question,
            'answers': all_answers_per_question[(image, context, description, question)]
        })

unique_images = []

for i in full_answer_list:
    num_unanswerable_votes = 0

    for answer in i['answers']:
        if (answer == ''):
            num_unanswerable_votes += 1

    if (num_unanswerable_votes >= 2):
        continue

    if (len(i['answers']) < 3):
        continue 

    unique_images.append(i['image'])
    # Take out all the unanswerable votes
    answers = [answer for answer in i['answers'] if answer != '']

    if (len(answers) > 3):
        clean_set_of_three_answers = random.sample(answers, 3)
        i['answers'] = clean_set_of_three_answers
    else:
        i['answers'] = answers 

    new_dataset_annotations.append(i)

print("Number of unique images: ", len(list(set(unique_images))))
with open('dataset_annotations_cleaned.json', 'w') as f:
    f.write(json.dumps(new_dataset_annotations, indent = 4))