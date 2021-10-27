import csv
import json
import os.path
from pathlib import Path

from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer


def evaluate(log_prob, log_merge, cleaning_mode):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    analyzer = EmailAnalyzer()
    with open("test_set.json") as email_file:
        new_emails = json.load(email_file)

    i = 0
    email_count = len(new_emails["dataset"])
    for e_mail in new_emails["dataset"]:
        i += 1
        print("\rEmail " + str(i) + "/" + str(email_count), end='\r')

        new_email = e_mail["mail"]
        subject = new_email["Subject"]
        body = new_email["Body"]
        spam = new_email["Spam"]

        is_spam = analyzer.is_spam(subject, body, log_prob, log_merge, cleaning_mode)

        if is_spam and (spam == "true"):
            tp += 1
        if not is_spam and (spam == "false"):
            tn += 1
        if is_spam and (spam == "false"):
            fp += 1
        if not is_spam and (spam == "true"):
            fn += 1
        total += 1

    accuracy = round((tp + tn) / (tp + tn + fp + fn), 2)
    precision = round(tp / (tp + fp), 2)
    recall = round(tp / (tp + fn), 2)
    print("\nAccuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    return [accuracy, precision, recall]


if __name__ == "__main__":


    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    results = []

    test_number = 0
    with open(os.path.join(BASE_DIR, "ACTS", "output.csv")) as ACTS_parameters:
        print(ACTS_parameters.readline()) # parameters used
        line = ACTS_parameters.readline()
        while line:
            [log_prob, log_merge, cleaning_mode, frequency] = line.split(',')
            print_line = "{:>15}" * 4
            print(print_line.format('Log Prob', 'log merge', 'cleaning mode', "min frequency"))
            print(print_line.format(log_prob, log_merge, cleaning_mode, frequency))

            # reformat variables
            log_prob = log_prob == "true"
            log_merge = log_merge == 'true'
            cleaning_mode = int(cleaning_mode)
            frequency = int(frequency)
            # 1. Creation de vocabulaire.
            vocab = VocabularyCreator(frequency, cleaning_mode)
            vocab.create_vocab()
            # 2. Classification des emails et initialisation de utilisateurs et groupes.
            renege = RENEGE()
            renege.classify_emails(log_prob, log_merge, cleaning_mode)

            #3. Evaluation de performance du modele avec la fonction evaluate()
            evaluation = evaluate(log_prob, log_merge, cleaning_mode)
            results.append([str(test_number)] + [log_prob, log_merge, cleaning_mode, frequency] + evaluation)
            #nouvelle line
            test_number += 1
            line = ACTS_parameters.readline()
    with open('results.csv', "w") as results_file:
        writer = csv.writer(results_file)
        writer.writerow(['Test number', 'log prob', 'log merge', 'cleaning mode', 'frequency', 'accuracy', 'precision', 'recall'])
        writer.writerows(results)