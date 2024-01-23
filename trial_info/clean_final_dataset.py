import json
import random 

#f = open('dataset_annotations_so_far.json')
f = open('ig-vqa-default-rtdb-answer-elicitation-study-gpt4-descriptions-export.json')

data = json.load(f)

new_dataset_annotations = []

# First, just make a long list of image, context, description, question, and then answers
#     {
#        "image": "images/news/Showjumping_white_horse.jpeg",
 #       "context": "social_media",
 #       "description": "A horse and rider jumping over a white obstacle in an equestrian showjumping event, under a cloudy sky.",
 #       "question": "what's the vibe, is it happy are they winning?",
 #       "answers": [
 #           "The vibe is more serious and determined ",
 #           "The atmosphere is very passionate and active. However, it cannot be confirmed whether the match was won.",
 #           "the person is happy, they are doing what they enjoy"
 #       ]
  #  },

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
    if (len(all_answers_per_question) >= 5):
        full_answer_list.append({
            'image': image,
            'context': context,
            'description': description,
            'question': question,
            'answers': all_answers_per_question[(image, context, description, question)]
        })

for i in full_answer_list:
    num_unanswerable_votes = 0

    for answer in i['answers']:
        if (answer == ''):
            num_unanswerable_votes += 1

    if (num_unanswerable_votes >= 2):
        continue

    # Take out all the unanswerable votes
    answers = [answer for answer in i['answers'] if answer != '']

    if (len(answers) > 3):
        clean_set_of_three_answers = random.sample(answers, 3)
        i['answers'] = clean_set_of_three_answers
    else:
        i['answers'] = answers 

    new_dataset_annotations.append(i)

with open('dataset_annotations_cleaned.json', 'w') as f:
    f.write(json.dumps(new_dataset_annotations, indent = 4))