import json 
import random 

image_context_pairs = json.load(open('remaining_image_context_pairs.json'))

answer_study = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-answer-elicitation-study-dataset-expansion-export (36).json'))

collected_datapoints = []
answers = {}

for participant in answer_study:
    for trial in answer_study[participant]:
        if ((trial['picture'], trial['category'], trial['description'], trial['question']) not in answers):
            answers[(trial['picture'], trial['category'], trial['description'], trial['question'])] = []
        answers[(trial['picture'], trial['category'], trial['description'], trial['question'])].append(trial['answer'])

#print("answers ", answers)
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
    print("image ", image, " context ", context)
    if [image, context] in image_context_pairs:
        print("image, context: ", image, context)
        formatted_questions.append(
            {
                'filename': image,
                'category': context,
                'description': description,
                'question': question
            }
        )

for (pic, context, description) in questions:
    question = random.choice(questions[(pic, context, description)])

    if [pic, context] in image_context_pairs:
        formatted_questions.append(
            {
                'filename': pic,
                'category': context,
                'description': description,
                'question': questions[(pic, context, description)]
            }
        )

# Then, write them (along with their questions so far) to a file!
with open("formatted_505_questions.json", "w") as f:
    f.write(json.dumps(formatted_questions, indent = 4))
