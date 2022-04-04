import requests
from requests.structures import CaseInsensitiveDict
import sys
import csv
import json
import pandas as pd
import time
import random

url = "https://api.languagetoolplus.com/v2/check"
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
}
username = "YOURUSERNAMEFORPREMIUM"
apiKey = "YOURAPIKEYFORPREMIUM"
random.seed(333)
def spell_checker(args):
    text_file = args[0]
    language = args[1]
    total_rows = sum(1 for _ in open(text_file)) - 1
    with open(text_file) as csvfile:
        x = csv.DictReader(csvfile)
        print("Tables in the file:")
        for i in x.fieldnames:
            print(f"   {i}")

        table = ["original_text","perturbed_text","attack"]

        fID = open("id_description.csv","w")
        fCHECK = open("text_errors_o.csv","w")
        fCHECKP = open("text_errors_p.csv","w")
        headerC = ['TEXT',"ATTACK","NUMBER_OF_ERRORS","ID_ERRORS"]
        headerID = ['ID_ERRORS','DESCRIPTION']

        writerID = csv.writer(fID,lineterminator='\n')
        writerID.writerow(headerID)
        writerCO = csv.writer(fCHECK,lineterminator='\n')
        writerCO.writerow(headerC)
        writerCP = csv.writer(fCHECKP,lineterminator='\n')
        writerCP.writerow(headerC)
        writers = [writerCO,writerCP]

        errors_obtained = []
        count = 1
        for i in x:

            try:

                print(f"{count}/{total_rows}")

                textO = i[table[0]]
                textP = i[table[1]]
                attack = i[table[2]]
                print(attack)
                textO = textO.replace("[","")
                textO = textO.replace("]","")
                textP = textP.replace("[","")
                textP = textP.replace("]","")
                texts = [textO,textP]
                dataO = [
                    ('username', f'{username}'),
                    ('apiKey', f'{apiKey}'),
                    ('language', f'{language}'),
                    ('text', f'{textO}'),
                ]
                dataP = [
                    ('username', f'{username}'),
                    ('apiKey', f'{apiKey}'),
                    ('language', f'{language}'),
                    ('text', f'{textP}'),
                ]

                respF = []
                respO = requests.post(url, headers=headers, data=dataO)
                respP = requests.post(url, headers=headers, data=dataP)
                respF.append(respO)
                respF.append(respP)

                forbidden = ["UPPERCASE_SENTENCE_START","COMMA_PARENTHESIS_WHITESPACE"]
                l = 0
                for resp in respF:
                    if resp.status_code == 200:
                        answer = resp.json()
                        matches = answer['matches']
                        sentence = texts[l]
                        nb_erros = 0
                        errors_sentence = []
                        for j in matches:
                            check_rule = j['rule']
                            if check_rule['category']['id'] == "GRAMMAR":
                                id_ = check_rule['id']
                                descrip_ = check_rule['description']
                                if (id_ not in forbidden):
                                    nb_erros += 1
                                    errors_sentence.append(id_)
                                    if (id_ not in errors_obtained):
                                        errors_obtained.append(id_)
                                        writerID.writerow([id_,descrip_])
                        writers[l].writerow([sentence,attack,nb_erros,errors_sentence])
                    l += 1

                count += 1


                time.sleep(1)

            except:
                pass





if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) <= 1:
        print("Syntax to use : main.py [csv] [language]")
        exit()

    if len(args) > 2:
        print("Too much arguments!")
        exit()

    if len(args) == 2:
        spell_checker(args)

