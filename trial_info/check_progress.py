# TODO: Output the number of unique image-context pairs
# in the new_collected_dataset_so_far.json file!!

# I need to reach 1,700 unique image-context pairs here.
# And then I'm done!!

import json 

data = json.load(open('new_collected_dataset_so_far.json'))

unique_ic_pairs = []

for item in data:
    unique_ic_pairs.append((item['image'], item['context']))

print("Number of unique image-context pairs: ", len(list(set(unique_ic_pairs))))