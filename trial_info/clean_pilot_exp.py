import json

f = open('pilot_exp.json')
pilot_exp = json.load(f)

f = open('dataset_annotations_so_far.json')
dataset_annotations_so_far = json.load(f)

f = open('ig-vqa-default-rtdb-answer-elicitation-study-gpt4-descriptions-export.json')
study_data = json.load(f)

seen_in_dataset_annotations = {}

for datapoint in dataset_annotations_so_far:
    # Mark it if it's seen an image, context, and question before!!
    seen_in_dataset_annotations[(datapoint['image'], datapoint['context'], datapoint['question'])] = 1

count_seen = {}

for participant in study_data:
    for trial in study_data[participant]:
        if ((trial['picture'], trial['category'], trial['question']) not in count_seen):
            count_seen[(trial['picture'], trial['category'], trial['question'])] = 0
        count_seen[(trial['picture'], trial['category'], trial['question'])] += 1

for (filename, category, question) in count_seen:
    if (count_seen[(filename, category, question)] >= 3):
        seen_in_dataset_annotations[(filename, category, question)] = 1

new_pilot_exp = {}
new_pilot_exp['images'] = []

print("Number of datapoints in pilot exp: ", len(pilot_exp['images']))

for datapoint in pilot_exp['images']:
    if ((datapoint['filename'], datapoint['category'], datapoint['question']) not in seen_in_dataset_annotations):
        new_pilot_exp['images'].append(datapoint)

json_object = json.dumps(new_pilot_exp, indent=4)
 
print("Length of new pilot exp: ", len(new_pilot_exp['images']))

# Writing to sample.json
with open("pilot_exp_no_repeated_questions.json", "w") as outfile:
    outfile.write(json_object)
