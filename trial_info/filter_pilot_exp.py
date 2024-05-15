import json 

pilot_exp_data = json.load(open('pilot_exp.json'))
collected_datapoints = json.load(open('collected_datapoints.json'))

new_pilot_exp = {}
new_pilot_exp['images'] = []

for item in pilot_exp_data['images']:
    # Check if it's found in collected_datapoints
    found = False
    for j in collected_datapoints:
        if (item['filename'] == j['image'] and item['category'] == j['context']):
            found = True 
    
    if (not found):
        new_pilot_exp['images'].append({
            'filename': item['filename'],
            'category': item['category'],
            'description': item['description'],
            'question': item['question']
        })

with open("new_pilot_exp_fixed.json", "w") as f:
    f.write(json.dumps(new_pilot_exp, indent = 4))