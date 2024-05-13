# TODO: Select the questions in my dataset and prune it down!
# Also select questions that can't be answered by unimodal models

# For each unique image-context pair, select one question at random as representative!
# Then elicit answers for this particular question.
# Leave out unanswerable questions
# In my paper, let's include a unimodal model as well
# to answer the questions both on its own and with the contextual condition!
# This shouldn't perform as well, giving indication that this task DOES ned
# visual stimuli.

import json 

data = json.load(open('all_questions_collected.json'))

# Load the answers collected so far.
answers_collected_so_far = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-answer-elicitation-study-dataset-expansion-export (7).json'))

# Load all the questions collected so far
questions_so_far = json.load(open('/Users/nanditanaik/Downloads/ig-vqa-default-rtdb-question-elicitation-study-dataset-expansion-export (1).json'))

# TODO: Identify all the image-context pairs

# Make an image-context pair map, where each image-context is mapped to all of the questions elicited
# And each question (in the IC pair) is mapped to its equivalent

# map (image, context, description) to a bunch of questions
# and map each question to a list of answers
ic_pair_map = {}

for participant in answers_collected_so_far:
    for trial in answers_collected_so_far[participant]:
        print(trial['answer'])
        if (trial['image', 'context', 'description'])
# If an image-context pair does not have any answerable questions,
# then see if it has one

# If an image-context pair needs another question as representative,
# then print it out!!

# In total, add 1700 questions to the dataset,
# one question per image-context pair...

# Otherwise, I'll need to elicit some more question data!