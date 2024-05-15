import json 
import copy 

ic_pairs = json.load(open('remaining_image_context_pairs.json'))

# Take out the 60 pairs that are in new_pilot_exp.json

new_pilot_exp = json.load(open('new_pilot_exp.json'))

new_icpairs = copy.deepcopy(ic_pairs)

for [image, context] in ic_pairs:
    for item in new_pilot_exp['images']:
        if (item['filename'] == image and item['category'] == context):
            new_icpairs.remove([image, context])

new_file = []

for [image, context] in new_icpairs:
    new_file.append((image, context))

print("Length of new IC pairs: ", len(list(set(list(new_file)))))

# Pick a question for each of the new image-context pairs!
question_study = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-question-elicitation-study-dataset-expansion-export (10).json'))

questions = {}

for participant in question_study:
    for trial in question_study[participant]:
        if ((trial['picture'], trial['category']) not in new_file):
            continue 
        if ((trial['picture'], trial['category'], trial['description']) not in question_study):
            questions[(trial['picture'], trial['category'], trial['description'])] = []
        questions[(trial['picture'], trial['category'], trial['description'])].append(trial['q1'])
        questions[(trial['picture'], trial['category'], trial['description'])].append(trial['q2'])

all_remaining_coverage = {}
all_remaining_coverage['images'] = []

for (picture, category, description) in questions:
    print("picture: ", picture)
    print("category: ", category)
    print("description: ", description)

    dic = {
        'filename': picture,
        'category': category,
        'description': description,
        'questions': questions[(picture, category, description)]
    }

    all_remaining_coverage['images'].append(dic)

print("all remaining coverage length: ", len(all_remaining_coverage['images']))

print(all_remaining_coverage['images'])

with open("remaining_questions.json", "w") as f:
    f.write(json.dumps(all_remaining_coverage, indent = 4))