import json
import random



with open('word.json', 'r') as f_o:
    data_from_json = json.load(f_o)


for i in data_from_json['words']:
    print(data_from_json['words'][i])
    four_words = []
    for _ in range(4):
