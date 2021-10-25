import json
import math

from text_cleaner import TextCleaning


class EmailAnalyzer:
    """Classe pour classifier les e-mails comme spam ou non spam (ham)"""

    def __init__(self):
        self.vocab    = "vocabulary.json"
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
        email_body    = self.clean_text(body_orig, cleaning_mode)

        # Get the spam/ham probabilities
        p_subject_spam, p_subject_ham = self.spam_ham_subject_prob(email_subject, log_prob)
        p_body_spam,    p_body_ham    = self.spam_ham_body_prob(email_body, log_prob)

        # Compute the merged probabilities
        p_spam = 0
        p_ham = 0

        if log_merge:
            p_spam = math.exp(k * math.log(p_subject_spam) + (1 - k) * math.log(p_body_spam))
            p_ham = math.exp(k * math.log(p_subject_ham) + (1 - k) * math.log(p_body_ham))
        else:
            p_spam = k * p_subject_spam + (1 - k) * p_body_spam
            p_ham = k * p_subject_ham + (1 - k) * p_body_ham

        # Decide is the email is spam or ham
        if p_spam > p_ham:
            return True 
        else:
            return False

    def spam_ham_body_prob(self, body, use_log):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''
        p_spam = 1.0
        p_ham  = 1.0

        voc_data = self.load_dict()
        # Walk the text to compute the probability
        if use_log:
            for word in body:
                # Check the spam probability
                if word in voc_data["p_body_spam"]:
                    p_spam += math.log(voc_data["p_body_spam"][word])
                else:
                    p_spam += math.log(1.0 / (len(voc_data["p_body_spam"]) + 1.0))

                # Check the ham probability
                if word in voc_data["p_body_ham"]:
                    p_ham += math.log(voc_data["p_body_ham"][word])
                else:
                    p_ham += math.log(1.0 / (len(voc_data["p_body_ham"]) + 1.0))
            p_spam = math.exp(p_spam)
            p_ham = math.exp(p_ham)
        else:
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
        p_ham  *= 0.4075
        return (p_spam, p_ham)

    def spam_ham_subject_prob(self, subject, use_log):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''
        p_spam = 1.0
        p_ham  = 1.0

        voc_data = self.load_dict()

        # Walk the text to compute the probability
        if use_log:
            for word in subject:
                # Check the spam probability
                if word in voc_data["p_sub_spam"]:
                    p_spam += math.log(voc_data["p_sub_spam"][word])
                else:
                    p_spam += math.log(1.0 / (len(voc_data["p_sub_spam"]) + 1.0))

                # Check the ham probability
                if word in voc_data["p_sub_ham"]:
                    p_ham += math.log(voc_data["p_sub_ham"][word])
                else:
                    p_ham += math.log(1.0 / (len(voc_data["p_sub_ham"]) + 1.0))
            p_spam = math.exp(p_spam)
            p_ham = math.exp(p_ham)
        else:
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

        p_spam *= 0.5925
        p_ham  *= 0.4075
        
        return (p_spam, p_ham)
    
    def clean_text(self, text, mode): #pragma: no cover
        return self.cleaning.clean_text(text, mode)

    def load_dict(self): #pragma: no cover
        # Open vocabulary 
        with open(self.vocab) as json_data:
            vocabu = json.load(json_data)
        
        return vocabu