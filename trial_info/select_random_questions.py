import json 
import random 

# Select 10 random questions, one from each context!
# Then run it!
f = open('questions_not_covered.json')
data = json.load(f)

questions_per_context = {}

for i in data:
    if (i['category'] not in questions_per_context):
        questions_per_context[i['category']] = []
    questions_per_context[i['category']].append(i)

contexts = ['health', 'social_media', 'science_journals', 'shopping', 'news', 'travel']

list_of_chosen_questions = []

for context in contexts:
    list_of_chosen_questions.extend(random.sample(questions_per_context[context], 10))

with open("new_questions.json", "w") as f:
    f.write(json.dumps(list_of_chosen_questions, indent = 4))