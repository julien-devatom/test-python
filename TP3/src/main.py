import json
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

    print("Evaluating emails ")
    for e_mail in new_emails["dataset"]:
        i += 1
        print("\rEmail " + str(i) + "/" + str(email_count), end="")

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
    
    print("")
    print("\nAccuracy: ", round((tp + tn) / (tp + tn + fp + fn), 2))
    print("Precision: ", round(tp / (tp + fp), 2))
    print("Recall: ", round(tp / (tp + fn), 2))
    return True


if __name__ == "__main__":

    # 1. Creation de vocabulaire.
    vocab = VocabularyCreator()
    vocab.create_vocab()

    # 2. Classification des emails et initialisation de utilisateurs et groupes.
    renege = RENEGE()
    renege.classify_emails()

    #3. Evaluation de performance du modele avec la fonction evaluate()
    evaluate()
