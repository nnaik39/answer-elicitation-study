import json 
import random 

all_image_context_pairs = json.load(open('../../question-elicitation-study/trial_info/full_question_elicitation_study.json'))

answer_study = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-answer-elicitation-study-dataset-expansion-export (56).json'))
collected_dataset = json.load(open('new_collected_dataset_so_far.json'))

image_context_pairs = []

for item in all_image_context_pairs['images']:
    image_context_pairs.append((item['filename'], item['category']))

collected_datapoints = []
answers = {}

for participant in answer_study:
    for trial in answer_study[participant]:
        if ((trial['picture'], trial['category'], trial['description'], trial['question']) not in answers):
            answers[(trial['picture'], trial['category'], trial['description'], trial['question'])] = []
        answers[(trial['picture'], trial['category'], trial['description'], trial['question'])].append(trial['answer'])

num_answerable = 0
num_unanswerable = 0

images = []

for (image, context, description, question) in answers:
    images.append(image)
    # Check if there are at least two unanswerable ratings!!
    unanswerable = False 
    if (answers[(image, context, description, question)].count('') >= 2):
        unanswerable = True 

    if (len(answers[(image, context, description, question)]) >= 3):
        i = {
            'image': image,
            'context': context,
            'description': description,
            'question': question,
            'unanswerable': unanswerable,
            'answers': random.sample(answers[(image, context, description, question)], 3)}
        collected_datapoints.append(i)
        
        num_answerable += 1
        if ((image, context) in image_context_pairs):
            image_context_pairs.remove((image, context))
    elif (unanswerable):
        i = {
            'image': image,
            'context': context,
            'description': description,
            'question': question,
            'unanswerable': unanswerable,
            'answers': []}
        collected_datapoints.append(i)
        num_unanswerable += 1
        if ((image, context) in image_context_pairs):
            image_context_pairs.remove((image, context))

print("Total images left: ", len(list(set(images))))

print("Total image-context pairs left: ", len(image_context_pairs))
print("Answerable: ", num_answerable)
print("Unanswerable: ", num_unanswerable)

with open('remaining_image_context_pairs.json', 'w') as f:
    f.write(json.dumps(image_context_pairs))