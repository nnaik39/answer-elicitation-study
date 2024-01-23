import json

f = open('pilot_exp.json')

data = json.load(f)

unique_images = []

for i in data['images']:
    unique_images.append(i['filename'])

unique_images = list(set(unique_images))

print("Length of unique images: ", len(unique_images))
