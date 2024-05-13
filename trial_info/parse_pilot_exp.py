import json 

pilot_exp = json.load(open('pilot_exp.json'))

new_pilot_exp = {}
new_pilot_exp['images'] = []

for item in pilot_exp['images']:
    print(item)
    
    new_pilot_exp['images'].append({
        'filename': item['filename'],
        'description': item['description'],
        'category': item['category'],
        'question': item['questions'][0]
    })

with open('formatted_pilot_exp.json', 'w') as f:
    f.write(json.dumps(new_pilot_exp, indent = 4))