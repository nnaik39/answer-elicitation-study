import json
import random 

#f = open('dataset_annotations_so_far.json')
f = open('ig-vqa-default-rtdb-answer-elicitation-study-gpt4-descriptions-export.json')
data = json.load(f)
f = open('correct_descriptions_each_image.json')
correct_descriptions = json.load(f)

new_dataset_annotations = []

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
    if (len(all_answers_per_question) >= 3 and (image not in correct_descriptions or description == correct_descriptions[image])):
        full_answer_list.append({
            'image': image,
            'context': context,
            'description': description,
            'question': question,
            'answers': all_answers_per_question[(image, context, description, question)]
        })

unique_images = []

images = ['images/440px-Los_Altos_Main_Street_2.jpeg', 'images/Foodora_messenger.jpeg', 'images/Hemp_Oregon_State.jpeg', 'images/500px-Backzutaten_041.jpeg', 'images/500px-Diane_von_Furstenberg_Spring-Summer_2014_06.jpeg', 'images/623px-Stanford_University_Arches_with_Memorial_Church_in_the_background.jpg', 'images/Ipomoea_stir_fry.jpeg', 'images/400px-Norman_Borlaug.jpeg', 'images/440px-Vegan_Gardein_Tofu_Foods_Display_(cropped1).jpeg', 'images/440px-Protein_shake.jpg', 'images/Acorn_Soup_(4827753894).jpeg', 'images/Fruit_Stall_in_Barcelona_Market.jpeg', 'images/15718.jpg', 'images/MICHAEL_KORS_221.jpeg', 'images/MarsCuriosityRover-Drilling-Sol170++-2.jpg', 'images/440px-Redwood_Grove_logs_to_mill.jpeg', 'images/CH.VD.Bex_2007-09-02_Airshow_396_16x9-R_5120x2880_(cropped).jpg', 'images/360px-MeghanTrainor_jingle_ball_tour.jpeg', 'images/440px-Vegas_by_night_(360655015).jpeg', 'images/San_Francisco_Bay_Wheels.jpg', 'images/Blacksmoker_in_Atlantic_Ocean.jpg', 'images/Ilovechicago.jpeg', 'images/US_Navy_030124-N-1328C-510_Navy_dentist_treats_patients_aboard_ship.jpeg', 'images/Bellagio_Las_Vegas_December_2013_panorama.jpeg', 'images/440px-Mallard_Drake_on_Adobe_Creek_2010.jpeg', 'images/440px-Yoga_dog_(4045140609).jpeg', 'images/Yam_mu_yo.jpeg', 'images/15722.jpg', 'images/80px-Rocket-yoga-13_handstand_(cropped).jpeg', 'images/500px-Soldier_running_in_water_original.jpeg', 'images/20170721_Gotham_Shield_NYC_Aerials-225_medium_(cropped).jpg', 'images/15692.jpg', 'images/Nyle2.jpeg', 'images/Backpack_mounted_knife_D.D._Teoli_Jr.jpg', 'images/951_Gaspra.jpg', 'images/440px-Uber_ride_Bogota_(10277864666).jpeg', 'images/400px-Milad_Kharchegani_at_the_2016_Summer_Olympics.jpeg', 'images/Carolina_Herrera_AW14_12.jpeg', 'images/Cable_Car_No._1_and_Alcatraz_Island.jpg', 'images/Michael_Kors_Spring-Summer_2014_60.jpeg', 'images/Bebe_Rexha_-_Untold_2023_-_53113724212_(cropped).jpg', 'images/Leila_Goldkuhl_Chloe.jpeg', 'images/New_york_times_square-terabass_(cropped).jpg', 'images/440px-Kale_&_Poached_Eggs_Salad_(8733071700).jpg', 'images/Ludovic_and_Lauren_(8425515069).jpeg', 'images/P-51_Mustang_edit1.jpeg', 'images/Apollo_17_AS17-140-21497.jpeg', 'images/440px-Giant_Panda_Eating.jpg', 'images/Gordon_Ramsay_cooking_(262930612).jpeg', 'images/Veggie_burger_miikkahoo_flickr_creative_commons.jpeg', 'images/Korea-Boseong-Green.tea-09.jpg', 'images/470px-Uggs2.jpeg', 'images/400px-Retinal_camera.jpeg', 'images/Natural_foodstuff_004.jpeg', 'images/Ransom_Canyon_Texas_Vogue_Magazine_Photo_Shoot.jpeg', 'images/250px-Raphanus_sativus.jpeg', 'images/Souk_in_Tunisia_1.jpeg', 'images/Sergey_Brin_Ted_2010.jpg', 'images/Dan_+_Shay_in_2017.jpeg', 'images/15719.jpg', 'images/440px-Lazada_Laguna_warehouse.jpeg', 'images/Solar_eclipse_1999_4.jpeg', 'images/Nilgiri_Mountain_Train.jpeg', 'images/510px-Spaltlampe-2.jpeg', 'images/500px-Flying_Double_Side_Kick_in_Martial_Arts.jpeg', 'images/Faculty_of_Food_Engineering_and_Biotechnology_4.jpeg', 'images/220px-Ado-muka-shvanasana.jpeg', 'images/440px-Palace_of_Fine_Arts_during_Schon_–_Holt_Salahi_wedding.jpg', 'images/Texas_Zip_liner_5430.jpeg', 'images/Gigi_Hadid_2016.png', 'images/Aerial_view_-_Presidio-whole.jpg', 'images/440px-Telescope_Kepler-NASA.jpg', 'images/002-soymilk.jpeg', 'images/440px-Gigi_Hadid_Stuart_Weitzman.jpg', 'images/Shops_in_the_Bellagio_casino,_Las_Vegas.jpeg', 'images/Bhekasana1.jpeg', 'images/440px-Bay_to_Breakers_2011_Up.jpg', 'images/Drug_ampoule_JPN.jpeg', 'images/Bellagio_garden_crystal_ball.jpeg', 'images/Skydiving_from_a_Ukraine_Air_Force_Ilyushin_Il-76MD.jpeg']

for i in full_answer_list:
    num_unanswerable_votes = 0

    for answer in i['answers']:
        # Problem: Sometimes the checkbox was true for unanswerable but the answer was still entered here...
        # TODO: Let me fix this!!
        if (answer == ''):
            num_unanswerable_votes += 1

    if (num_unanswerable_votes >= 2):
        continue

    if (len(i['answers']) < 3):
        continue 

    unique_images.append(i['image'])

    if (i['image'] in images):
        images.remove(i['image'])
    # Take out all the unanswerable votes
    answers = [answer for answer in i['answers'] if answer != '']

    if (len(answers) > 3):
        clean_set_of_three_answers = random.sample(answers, 3)
        i['answers'] = clean_set_of_three_answers
    else:
        i['answers'] = answers 

    new_dataset_annotations.append(i)

print("Number of unique images: ", len(list(set(unique_images))))

print("Images not covered yet: ", images)

with open('dataset_annotations_cleaned.json', 'w') as f:
    f.write(json.dumps(new_dataset_annotations, indent = 4))