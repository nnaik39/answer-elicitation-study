import json
f = open('dataset_annotations_cleaned.json')
data = json.load(f)

# Count the number of questions elicited in this dataset for each context, and try to balance it out a little bit??

context_counts = {}

for i in data: 
    if (i['context'] not in context_counts):
        context_counts[i['context']] = 0
    context_counts[i['context']] += 1

print(context_counts)