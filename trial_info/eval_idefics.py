import torch, contextlib, wandb, json, os
from clipscore_helper import get_all_metrics, get_clip_score
import pandas as pd
from transformers import IdeficsForVisionText2Text, AutoProcessor
from PIL import Image
from evaluate import load
from tqdm import tqdm

wandb.init(project="comm_vqa")

device = "cuda" if torch.cuda.is_available() else "cpu"

f = open('../dataset_annotations_cleaned.json')
data = json.load(f)

results = []

def evaluate_metrics(refs, cands, images):
    # Divide the refs and candidates into 5 confidence intervals, and then return the mean and standard deviation 
    # over all of them?
    if (len(cands) > 1):
        # Divide into 5 random intervals
        with contextlib.redirect_stdout(None):
            metrics_dict = get_all_metrics([refs], [cands])

    _, per_instance_image_text, candidate_feats = get_clip_score(
            model, images, cands, device)
   
    scores = {image_id: {'CLIPScore': float(clipscore)}
        for image_id, clipscore in
        zip(images, per_instance_image_text)}

    # Add in CLIPScore and Ref-CLIPScore here, too?
    metrics_dict['clipscore'] = [s['CLIPScore'] for s in scores.values()][0]
    
    return metrics_dict

refs = []
hyps = []

checkpoint = "HuggingFaceM4/idefics-9b-instruct"
model = IdeficsForVisionText2Text.from_pretrained(checkpoint, torch_dtype=torch.bfloat16).to(device)
processor = AutoProcessor.from_pretrained(checkpoint)

formatted_contexts = {'social_media': 'social media', 'science_journals': 'science magazine'}

images = []

condition = "baseline"

for eval_datapoint in tqdm(data):
    image_path = eval_datapoint['image']

    images.append('../' + image_path)

    question = eval_datapoint['question']

    context = eval_datapoint['context']

    if (eval_datapoint['context'] in formatted_contexts):
        context = formatted_contexts[eval_datapoint['context']]

    # Context + description condition
    if (condition == "context_description"):
        question = 'Assume someone is browsing a ' + context + ' website when they encounter this image. They cannot see the image directly, but they can access this image description: ' + eval_datapoint['description'] + ' Based on this description, they asked this follow-up question. Please answer based on the image. In your answer, prioritize details relevant to this person. Question: ' + eval_datapoint['question']

    # Description-only condition
    if (condition == "description_only"):
        question = 'Assume someone is browsing a website when they encounter this image. They cannot see the image directly, but they can access this image description: ' + eval_datapoint['description'] + ' Based on this description, they asked this follow-up question. Please answer based on the image. In your answer, prioritize details relevant to this person. Question: ' + eval_datapoint['question']

    if (condition == "context_only"):
        question = 'Assume someone is browsing a ' + context + ' website when they encounter this image. They cannot see the image directly, but they can access an image description. Based on this description, they asked this follow-up question. Please answer based on the image. In your answer, prioritize details relevant to this person. Question: ' + eval_datapoint['question']

    image = Image.open('../' + image_path).convert("RGB")

    prompts = [
    [
        "User: " + question,
        image,
        "<end_of_utterance>",
        "\nAssistant: ",
    ],
    ]

    inputs = processor(prompts, add_end_of_utterance_token=False, return_tensors="pt").to(device)
    exit_condition = processor.tokenizer("<end_of_utterance>", add_special_tokens=False).input_ids
    bad_words_ids = processor.tokenizer(["<image>", "<fake_token_around_image>"], add_special_tokens=False).input_ids

    generated_ids = model.generate(**inputs, eos_token_id=exit_condition, bad_words_ids=bad_words_ids, max_new_tokens=256, do_sample=False, num_beams=1)
    generated_answer = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].replace(prompts[0][0], '').replace(' \nAssistant: ', '').replace('Assistant:', '').strip()

    metrics_dict = evaluate_metrics(refs, generated_answer, ['../' + image_path])
    results.append({
            'image': eval_datapoint['image'],
            'description': eval_datapoint['description'],
            'context': eval_datapoint['context'],
            'prompt': prompts[0][0],
            'question': eval_datapoint['question'],
            'answers': eval_datapoint['answers'],
            'generated_answer': generated_answer[0],
            'metrics': metrics_dict
            })

    if (len(eval_datapoint['answers']) == 3):
        refs.append([eval_datapoint['answers'][0].lower().strip(), eval_datapoint['answers'][1].lower().strip(), eval_datapoint['answers'][2].lower().strip()])
    else:
        refs.append([eval_datapoint['answers'][0].lower().strip(), eval_datapoint['answers'][1].lower().strip()])
    hyps.append(generated_answer[0].lower().strip())

results_per_context = {}
refs_per_context = {}
hyps_per_context = {}
images_per_context = {}

for datapoint in results:
    if (datapoint['context'] not in refs_per_context):
        refs_per_context[datapoint['context']] = []
        hyps_per_context[datapoint['context']] = []
        images_per_context[datapoint['context']] = []

    hyps_per_context[datapoint['context']].append(datapoint['generated_answer'].lower().strip())
    eval_datapoint = datapoint

    images_per_context[datapoint['context']].append('../' + datapoint['image'])
    if (len(datapoint['answers']) == 3):
        refs_per_context[datapoint['context']].append([eval_datapoint['answers'][0].lower().strip(), eval_datapoint['answers'][1].lower().strip(), eval_datapoint['answers'][2].lower().strip()])
    else:
        refs_per_context[datapoint['context']].append([eval_datapoint['answers'][0].lower().strip(), eval_datapoint['answers'][1].lower().strip()])

writeFile = "idefics_baseline"

folder_path = "results/" + writeFile + "/" + writeFile

os.mkdir("results/" + writeFile)
metrics_per_context = {}

for context in refs_per_context:
    with open(folder_path + '_percontext_metrics.json', 'w') as fp:
        json.dump(metrics_per_context, fp)

print("Metrics dict for IDEFICS evaluation: ", metrics_dict)

idx = list(range(0, len(results)))
df = pd.DataFrame(results, index=idx)
df.to_csv(folder_path + '_results.csv')

wandb.log(metrics_dict)

with open(folder_path + '_metrics_dict.json', 'w') as fp:
    json.dump(metrics_dict, fp)