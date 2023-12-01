import json 

# Remove any duplicates from this stdy!!
f = open('pilot_exp.json')

data = json.load(f)

# Add in questions with 2 hits from here!!
# Then calculate how many participants you need for collecting the rest of these answers!! :) 

images = data['images']

# Remove duplicates from pilot_exp.json!
# Also, remove anything that is already in the dataset... And that's already fully covered!

print("Images ", images)

images = [dict(t) for t in {tuple(d.items()) for d in images}]

 
dataset = open('dataset_annotations_so_far.json')

dataset_so_far = json.load(dataset)

new_pilot_exp = {}
new_pilot_exp['images'] = []

for image in images:
    if image not in dataset_so_far:
        new_pilot_exp['images'].append(image)

json_object = json.dumps(new_pilot_exp, indent=4)
# Writing to sample.json
with open("new_pilot_exp_duplicates_removed.json", "w") as outfile:
    outfile.write(json_object)
