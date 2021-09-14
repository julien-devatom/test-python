
import json
import sys
from crud import CRUD
from email_analyzer import EmailAnalyzer


class RENEGE:

    """Class pour realiser le filtrage du spam en utilisant vocabular.json file et
    CRUD et EmalAnalyze classes"""

    def __init__(self):
        self.email_file = "train_set.json"
        self.crud = CRUD()
        self.e_mail = EmailAnalyzer()

    def classify_emails(self):
        '''
        Description: fonction pour commencer l'analyse des e-mails.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        try:
            self.process_email(self.get_email())
            return True
        except Exception as e:
            print("Error!", e.__class__, "occurred.")
            raise e
            return False


    def process_email(self, new_emails):
        '''
        Description: fonction pour analyser chaque nouvel e-mail dans le 
        dictionare. Elle gere l'ajout des nouveux utilisateurs et/ou modification
        de l'information existante sur les utilisateurs et groupes. 
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        emails = self.get_email()
        print("Processing emails")
        i = 0
        email_count = len(emails["dataset"])
        # Load emails
        for email in emails["dataset"]:    
            i += 1
            print("\rEmail " + str(i) + "/" + str(email_count), end="")

            data    = email["mail"]
            subject = data["Subject"]
            name    = data["From"]
            date    = data["Date"]            
            body    = data["Body"]
            is_spam = data["Spam"]

            # Get registered data
            user_id = -1
            try:
                user_id = self.crud.get_user_id(name)
            except RuntimeError:
                # Create the user
                if not self.crud.add_new_user(name, date):
                    return False

                user_id = self.crud.get_user_id(name) 

            # Update user's emails info
            if is_spam == "true":
                if not self.update_user_info(user_id, date, 1, 0):
                    return False
            else:
                if not self.update_user_info(user_id, date, 0, 1):
                    return False

            # Update groups data
            groups = self.crud.get_user_data(user_id, "Groups")
            for group_name in groups:
                try:
                    group_id = self.crud.get_group_id(group_name)
                    if not self.update_group_info(group_id, user_id):
                        return False

                except RuntimeError:
                    return False
        
        print("\n")

        return True

    def update_user_info(self, user_id, new_user_date, new_email_spam, new_email_ham):
        '''
        Description: fonction pour modifier l'information de utilisateur (date de dernier message arrive,
        numero de spam/ham, trust level, etc).
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        # Update last / first seen date 
        new_date = self.crud.convert_to_unix(new_user_date)
        if new_date > self.crud.get_user_data(user_id, "Date_of_last_seen_message"):
            if not self.crud.update_users(user_id, "Date_of_last_seen_message", new_user_date):
                return False
        elif new_date < self.crud.get_user_data(user_id, "Date_of_first_seen_message"):
            if not self.crud.update_users(user_id, "Date_of_first_seen_message", new_user_date):
                return False

        # Update trust score 
        spam_n = self.crud.get_user_data(user_id, "SpamN") + new_email_spam
        ham_n  = self.crud.get_user_data(user_id, "HamN") + new_email_ham

        trust_lvl = 50
        if (spam_n + ham_n) != 0:
            trust_lvl = ham_n / (spam_n + ham_n) * 100
            if trust_lvl > 100:
                trust_lvl = 100

        if not self.crud.update_users(user_id, "SpamN", spam_n):
            return False

        if not self.crud.update_users(user_id, "HamN", ham_n):
            return False

        return self.crud.update_users(user_id, "Trust", trust_lvl)

    def update_group_info(self, group_id, user_id):
        '''
        Description: fonction pour modifier l'information de groupe dans lequel 
        l'utilisater est present (trust level, etc).
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''        
        try:
            # Get list of users and update it
            users_list = self.crud.get_groups_data(group_id, "List_of_members")
            user_name  = self.crud.get_user_data(user_id, "name")
            if user_name not in users_list:
                users_list.append(user_name)

            # Get data for trust update
            user_count = len(users_list)
            trust_lvl  = 0      

            # Compute group's trust
            for user in users_list:
                curr_user_id = self.crud.get_user_id(user)
                trust_lvl   += self.crud.get_user_data(curr_user_id, "Trust")

            if(trust_lvl > 100):
                trust_lvl = 100 
            
            # Update the group with the new trust level and the new member list
            if self.crud.update_groups(group_id, "Trust", trust_lvl):     
                return self.crud.update_groups(group_id, 'List_of_members', users_list)

            return False
        except RuntimeError:
            return False


    def get_user_email_list(self):
        '''
        Description: fonction pour creer le liste des e-mails (noms) 
        des utilisateurs uniques.
        Sortie: liste des uniques e-mails des utilisateurs
        '''
        emails = []
        for user in self.crud.users_data:
            emails.append(user["name"])
        return emails

    def get_email(self):
        '''
        Description: fonction pour lire le ficher json avec les mails et extraire les 
        donees necessaire.
        Sortie: dictionare de e-mails formate selon le JSON.
        '''
        with open(self.email_file) as email_file:
            return json.load(email_file)

    ###########################################
    #             CUSTOM FUNCTION             #
    ###########################################
