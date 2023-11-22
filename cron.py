import json
import random



with open('word.json', 'r') as f_o:
    data_from_json = json.load(f_o)


word = random.choices(list(data_from_json['words'].items()), k=4)


four_words = ''
translate = dict(word)
for i in word:
    four_words += ' — '.join(i) + ", "



    with open('time_user.json', 'r') as f_o:
        time_json = json.load(f_o)

    for s in time_json:
        if s == "744090765":
            time_json[s]['Translate'] = translate
            time_json[s]['Four_words'] = four_words[:-2]

    with open('time_user.json', 'w') as f_o:
        json.dump(time_json, f_o, indent=4, ensure_ascii=False)









