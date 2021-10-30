import json
import math

from text_cleaner import TextCleaning

SMALLEST_FLOAT = -1.7976931348623157e+308
class EmailAnalyzer:
    """Classe pour classifier les e-mails comme spam ou non spam (ham)"""

    def __init__(self):
        self.vocab = "vocabulary.json"
        self.cleaning = TextCleaning()
        self.voc_data = {}

    def is_spam(self, subject_orig, body_orig, log_prob, log_merge, cleaning_mode):
        '''
        Description: fonction pour verifier si e-mail est spam ou ham,
        en calculant les probabilites d'etre spam et ham, 
        donnee le sujet et le texte d'email. 
        Sortie: 'True' - si l'email est spam, 'False' - si email est ham.
        '''
        # Clean email's subject and body
        k = 0.5
        email_subject = self.clean_text(subject_orig, cleaning_mode)
        email_body = self.clean_text(body_orig, cleaning_mode)

        # Get the spam/ham probabilities
        p_subject_spam, p_subject_ham = self.spam_ham_subject_prob(email_subject, log_prob)
        p_body_spam, p_body_ham = self.spam_ham_body_prob(email_body, log_prob)

        # Compute the merged probabilities
        p_spam = 0
        p_ham = 0

        if log_merge:
            """
            Pour se débarasser des erreurs liés au log nul, nous avons décidé d'approximer le terme nul par le log le plus bas possible
            autorisé par python (log(très_petit)=-1.7976931348623157e+308)
            Nous aurons pu également créer des conditions sur log_merge et use_log, avec use_log == True => log_merge = True
            afin de ne pas passer par la puissance de 10. Mais ce serait une contrainte due au language Python, et non une contrainte mathématique
            
            """
            # formule utilisée : logP(spam|text) = k ∗ logP(spam sub|text) + (1 − k) ∗ logP(spam body|text)
            p_spam = k * math.log(p_subject_spam, 10) if p_subject_spam > 0 else k * SMALLEST_FLOAT
            p_spam += (1 - k) * math.log(p_body_spam, 10) if p_body_spam > 0 else (1-k) * SMALLEST_FLOAT
            p_ham = k * math.log(p_subject_ham, 10) if p_subject_ham > 0 else k * SMALLEST_FLOAT
            p_ham += (1 - k) * math.log(p_body_ham, 10) if p_body_ham > 0 else (1-k) * SMALLEST_FLOAT

            # On garde les logs qu'on compare entre eux, car la fonction log est croissante
        else:
            # formule utilisée : P(spam|text) = k ∗ P(spam sub|text) + (1 − k) ∗ P(spam body|text)
            p_spam = k * p_subject_spam + (1 - k) * p_body_spam
            p_ham = k * p_subject_ham + (1 - k) * p_body_ham

        # Decide is the email is spam or ham
        return p_spam > p_ham

    def spam_ham_body_prob(self, body, use_log):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''
        voc_data = self.load_dict()
        # Walk the text to compute the probability
        if use_log:
            # formule utilisée : logP(spam|text) = sum_i(logP(wi|spam)) + logP(spam)
            log_p_spam = 0
            log_p_ham = 0
            for word in body:
                # Check the spam probability
                if word in voc_data["p_body_spam"]:
                    log_p_spam += math.log(voc_data["p_body_spam"][word], 10)
                else:
                    log_p_spam += math.log(1.0 / (len(voc_data["p_body_spam"]) + 1.0), 10)

                # Check the ham probability
                if word in voc_data["p_body_ham"]:
                    log_p_ham += math.log(voc_data["p_body_ham"][word])
                else:
                    log_p_ham += math.log(1.0 / (len(voc_data["p_body_ham"]) + 1.0), 10)

            # On ajoute le terme logP(spam)
            log_p_spam += math.log(0.5925, 10)
            log_p_ham += math.log(0.4075, 10)

            # On renvoie les probabilités, et non le log
            # ATTENTION : on a ici parfois des approximations à zero, qui peuvent causer des problèmes par la suite
            p_spam = math.pow(10, log_p_spam)
            p_ham = math.pow(10, log_p_ham)
            return p_spam, p_ham

        else:
            # formule utilisée : P(spam|text) = P(spam) ∗ produit_i(P(wi|spam))
            p_spam = 1.
            p_ham = 1.
            for word in body:
                # Check the spam probability
                if word in voc_data["p_body_spam"]:
                    p_spam *= voc_data["p_body_spam"][word]
                else:
                    p_spam *= 1.0 / (len(voc_data["p_body_spam"]) + 1.0)

                # Check the ham probability
                if word in voc_data["p_body_ham"]:
                    p_ham *= voc_data["p_body_ham"][word]
                else:
                    p_ham *= 1.0 / (len(voc_data["p_body_ham"]) + 1.0)

            p_spam *= 0.5925
            p_ham *= 0.4075
            return p_spam, p_ham

    def spam_ham_subject_prob(self, subject, use_log):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''
        voc_data = self.load_dict()

        # Walk the text to compute the probability
        if use_log:
            # formule utilisée : logP(spam|text) = sum_i(logP(wi|spam)) + logP(spam)
            log_p_spam = 0
            log_p_ham = 0
            for word in subject:
                # Check the spam probability
                if word in voc_data["p_sub_spam"]:
                    log_p_spam += math.log(voc_data["p_sub_spam"][word], 10)
                else:
                    log_p_spam += math.log(1.0 / (len(voc_data["p_sub_spam"]) + 1.0), 10)

                # Check the ham probability
                if word in voc_data["p_sub_ham"]:
                    log_p_ham += math.log(voc_data["p_sub_ham"][word], 10)
                else:
                    log_p_ham += math.log(1.0 / (len(voc_data["p_sub_ham"]) + 1.0), 10)

            # On ajoute le terme logP(spam)
            log_p_spam += math.log(0.5925, 10)
            log_p_ham += math.log(0.4075, 10)

            # On renvoie les probabilités, et non le log
            p_spam = math.pow(10, log_p_spam)
            p_ham = math.pow(10, log_p_ham)
            return p_spam, p_ham

        else:
            # formule utilisée : P(spam|text) = P(spam) ∗ produit_i(P(wi|spam))
            p_spam = 1.
            p_ham = 1.
            for word in subject:
                # Check the spam probability
                if word in voc_data["p_sub_spam"]:
                    p_spam *= voc_data["p_sub_spam"][word]
                else:
                    p_spam *= 1.0 / (len(voc_data["p_sub_spam"]) + 1.0)

                # Check the ham probability
                if word in voc_data["p_sub_ham"]:
                    p_ham *= voc_data["p_sub_ham"][word]
                else:
                    p_ham *= 1.0 / (len(voc_data["p_sub_ham"]) + 1.0)

            # On ajoute le terme P(spam)
            p_spam *= 0.5925
            p_ham *= 0.4075

            return p_spam, p_ham

    def clean_text(self, text, mode):  # pragma: no cover
        return self.cleaning.clean_text(text, mode)

    def load_dict(self):  # pragma: no cover
        # Open vocabulary 
        with open(self.vocab) as json_data:
            vocabu = json.load(json_data)
        return vocabu
