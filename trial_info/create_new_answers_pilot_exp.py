import json 
import random 

all_image_context_pairs = json.load(open('../../question-elicitation-study/trial_info/full_question_elicitation_study.json'))

answer_study = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-answer-elicitation-study-dataset-expansion-export (28).json'))
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

for (image, context, description, question) in answers:
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

        if ((image, context) in image_context_pairs):
            image_context_pairs.remove((image, context))
    
print("Total image-context pairs: ", len(image_context_pairs))

question_study = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-question-elicitation-study-dataset-expansion-export (10).json'))

questions = {}


for participant in question_study:
    for trial in question_study[participant]:
        if ((trial['picture'], trial['category'], trial['description']) not in question_study):
            questions[(trial['picture'], trial['category'], trial['description'])] = []
        questions[(trial['picture'], trial['category'], trial['description'])].append(trial['q1'])
        questions[(trial['picture'], trial['category'], trial['description'])].append(trial['q2'])

formatted_questions = []

# If there exist answers for a question already
for (image, context, description, question) in answers:
    if (image, context) in image_context_pairs:
        formatted_questions.append(
            {
                'filename': image,
                'category': context,
                'description': description,
                'question': question
            }
        )
        print("There exist answers for a question already")
        if ((image, context) in image_context_pairs):
            image_context_pairs.remove((image, context))

#for (pic, context, description) in questions:
#    question = random.choice(questions[(pic, context, description)])
 #   if (pic, context) in image_context_pairs:
  #      formatted_questions.append(
   #         {
    #            'filename': pic,
     #           'category': context,
      #          'description': description,
     #           'question': questions[(pic, context, description)]
     #       }
     #   )

# Then, write them (along with their questions so far) to a file!
with open("remaining_ic_pairs.json", "w") as f:
    f.write(json.dumps(formatted_questions, indent = 4))

# Note: By the end of this, I want a giant file
# with all the questions and answers!