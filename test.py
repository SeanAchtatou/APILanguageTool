import csv
text_file = "adversarial_sentences.csv"
with open(text_file) as csvfile:
    x = csv.DictReader(csvfile)
    for i in x:
        print(i['original_text'])
        input()
