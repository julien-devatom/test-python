import json
import re
from datetime import timezone, datetime

class CRUD:
    """
    Classe pour realiser la fonctionalite CRUD.
    """

    def __init__(self):
        # Init the lookup tables
        self.users_lookup  = {}
        self.groups_lookup = {}

        # Set the files' name
        self.users_file = "users.json"
        self.groups_file = "groups.json"

        # Load data from the files
        try:
            self.users_data = self.read_users_file()
            self.groups_data = self.read_groups_file()
        except:
            # We could not load the data
            self.users_data = {}
            self.groups_data = {}            
            pass
        # Fill the lookup tables, the name are the tables' keys
        for key in self.users_data:
            self.users_lookup[self.users_data[key]["name"]] = key
        for key in self.groups_data:
            self.groups_lookup[self.groups_data[key]["name"]] = key

        # Add default group if it does not exist
        if "default" not in self.groups_data:
            self.add_new_group("default", 50, [])

    ##*************UTILS***************
    '''
    Description: retourne un id unique pour un nouvel utilisateur
    Sortie: un id unique pour un nouvel utilisateur
    '''
    def get_new_user_id(self):
        new_id = 0
        while str(new_id) in self.users_data:
            new_id += 1
        
        return str(new_id)

    '''
    Description: retourne un id unique pour un nouveau groupe
    Sortie: un id unique pour un nouveau groupe
    '''
    def get_new_group_id(self):
        new_id = 0
        while str(new_id) in self.groups_data:
            new_id += 1
        
        return str(new_id)
    
    """
    Description: Fonction pour convertir la date en unix-timestamp
    Sortie: float, la date en format unix-timestamp
    """
    def convert_to_unix(self, date):    
        dt   = datetime.strptime(date, '%Y-%m-%d')
        date = dt.replace(tzinfo=timezone.utc).timestamp()
        return date

    ##*************CREATE**************

    def add_new_user(self, user_email, date):
        '''
        Description: fonction pour ajouter un nouvel utilisateur 
        dans le fichier 'users.json', selon le format donné dans 
        la description du lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        # Check the unicity of the email address
        if user_email in self.users_lookup:
            return False

        # Check the email's format
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", user_email):
            return False

        # Init last and first message date, as the date of creation
        dt   = datetime.strptime(date, '%Y-%m-%d')
        date = dt.replace(tzinfo=timezone.utc).timestamp()

        # Create the new user
        new_id = self.get_new_user_id()
        self.users_data[new_id] = {
            "name": user_email,
            "Trust": 50,
            "SpamN": 0,
            "HamN": 0,
            "Date_of_first_seen_message": date,
            "Date_of_last_seen_message": date,
            "Groups": ["default"]
        }
        self.users_lookup[user_email] = new_id
        default_id   = self.get_group_id("default")
        default_list = self.get_groups_data(default_id, "List_of_members")
        default_list.append(user_email)
        self.update_groups(default_id, "List_of_members", default_list)

        # Success
        return self.modify_users_file(self.users_data)

    def add_new_group(self, name, trust, members_list):
        '''
        Description: fonction pour ajouter une grouppe  
        dans le fichier 'groups.json', selon le format donne dans 
        la description du lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        # Check the unicity of the group name
        if name in self.groups_lookup:
            return False

        # Check if all users exist
        for user in members_list:
            if user not in self.users_lookup:
                return False 

        # Create the new group
        new_id = self.get_new_group_id()
        self.groups_data[new_id] = {
            "name": name,
            "Trust": trust,
            "List_of_members": members_list
        }
        self.groups_lookup[name] = new_id

        try:
            # Add users to group 
            for user in members_list:
                user_id = self.get_user_id(user)
                if name not in self.users_data[user_id]["Groups"]:
                    self.users_data[user_id]["Groups"].append(name)

        except RuntimeError:
            return False
        #print(self.groups_data)
        # Success
        return self.modify_groups_file(self.groups_data)

    ###***********READ****************
    def read_users_file(self):
        '''
        Description: fonction qui lit le fichier 'users.json'
        et retourne le dictionaire
        Sortie: dictionare avec les utilisateurs 
        '''
        with open(self.users_file) as users_file:
            return json.load(users_file)

    def read_groups_file(self):
        '''
        Description: fonction qui lit le fichier 'users.json'
        et retourne le dictionaire
        Sortie: dictionare avec les groupes
        '''
        with open(self.groups_file) as group_file:
            return json.load(group_file)

    def get_user_data(self, user_id, field):
        '''
        Description: fonction qui sorte la valeur d'information specifie
        pour une utilisateur specifie.
        Par example, spam_number = get_user_data(2, "SpamN") va donner le
        numero de messages spam pour utilisateur avec id 2.
        Sortie: la valeur d'information specifie pour utilisateur
        '''
        user_id = str(user_id)

        # Check user's existance
        if user_id not in self.users_data:
            return False

        # Get the data
        user = self.users_data[user_id]
        if field not in user:
            return False

        return user[field]
        

    def get_groups_data(self, group_id, field):
        '''
        Description: fonction qui sorte la valeur d'information specifie
        pour une grouppe specifie.
        Par example, group_trust_level = get_groups_data(2, "Trust") va donner la
        valeur de "Trust" pour grouppe avec id 2.
        Sortie: la valeur d'information specifie pour le grouppe
        '''
        group_id = str(group_id)
        # Check group's existance
        if group_id not in self.groups_data:
            return False

        # Get the data
        group = self.groups_data[group_id]
        if field not in group:
            return False

        return group[field]

    def get_user_id(self, name):
        '''
        Description: fonction sorte l'id d'utilisateur, donne le nom (email d'utilisater)
        Sortie: la valeur d'id d'utilisateur
        '''
        if name not in self.users_lookup:
            return False

        return self.users_lookup[name]

    def get_group_id(self, name):
        '''
        Description: fonction sorte l'id de grouppe, donne le nom de grouppe
        Sortie: la valeur d'id de grouppe
        '''
        if name not in self.groups_lookup:
            return False

        return self.groups_lookup[name]

    ##*******UPDATE******************

    def modify_users_file(self, data):
        '''
        Description: fonction qui ecrit le dictionnaire
        d'utilisateurs dans le fichiers 'users.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        with open(self.users_file, "w") as outfile:
            json.dump(data, outfile)
        return True

    def modify_groups_file(self, data):
        '''
        Description: fonction qui ecrit le dictionnaire
        des grouppes dans le fichiers 'groups.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        with open(self.groups_file, "w") as outfile:
            json.dump(data, outfile)
        return True

    def update_users(self, user_id, field, data):
        '''
        Description: fonction qui modifie les donnes d'utilisateur
        Par example, update_users(3, "Trust", 60) va changer le valeur de "Trust"
        pour utilisateur avec id 3 au 60.
        update_users(3, "Groups", "friends") va ajouter le grouppe 'friends'
        pour utilisater avec id 3.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        user_id = str(user_id)

        # Check existence
        if user_id not in self.users_data:
            return False

        # Get user and check field validity
        if field not in self.users_data[user_id]:
            return False

        print("OK")
        try:
            # Update data
            if field == "name":
                if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", data):
                    return False
                
                # Update the data and the lookup table
                user_name = self.get_user_data(user_id, "name")
                del self.users_lookup[user_name]
                self.users_data[user_id]["name"] = data
                self.users_lookup[data] = user_id

            elif field == "Date_of_last_seen_message":
                date = self.convert_to_unix(data)
                last_msg = self.get_user_data(user_id, "Date_of_last_seen_message")
                # Check if the last message is newer than the previous last message
                if date < last_msg:
                    return False

                self.users_data[user_id]["Date_of_last_seen_message"] = date
                    
            elif field == "Date_of_first_seen_message":
                date = self.convert_to_unix(data)
                first_msg = self.get_user_data(user_id, "Date_of_first_seen_message")
                # Check if the first message is older than the previous first message
                if date > first_msg:
                    return False

                self.users_data[user_id]["Date_of_first_seen_message"] = date
                    
            elif field == "Trust":
                if data < 0 or data > 100:
                    return False
                
                self.users_data[user_id]["Trust"] = data

            elif field == "SpamN" or field == "HamN":
                if data < 0:
                    return False 

                self.users_data[user_id][field] = data

            elif field == "Groups":
                # Check if the groups exist
                for group in data:
                    if group not in self.groups_lookup:
                        return False

                # Update user's groups
                self.users_data[user_id]["Groups"] = data                  
            
            else:
                # This case should have been caught earlier and we should never 
                # execute this line (field not in self.users_data[user_id])
                return False 

        except RuntimeError:
            return False
        
        return self.modify_users_file(self.users_data)


    def update_groups(self, group_id, field, data):
        '''
        Description: fonction qui modifie les donnes du groupe
        Par example, update_groups(2, "Trust", 30) va changer le valeur de "Trust"
        pour le grouppe avec id 2 au 30.
        update_groups(3, "List_of_members", "test@mail.com") va ajouter l'utilisateur
        avec email test@mail.com dans le liste des membres de groupe
        avec id 3.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        group_id = str(group_id)

        # Check existence
        if group_id not in self.groups_data:
            return False

        # Get group and check field validity
        if field not in self.groups_data[group_id]:
            return False

        try:
            # Update data
            if field == "name":
                if len(data) < 1 or len(data) > 64:
                    return False 

                old_name = self.groups_data[group_id]["name"]
                # Update user's groups
                for user in self.users_data:
                    if old_name in user["Groups"]:
                        user["Groups"].remove(old_name)
                        user["Groups"].append(data)                   

                # Update group name
                del self.groups_lookup[self.groups_data[group_id]["name"]]
                self.groups_data[group_id]["name"] = data
                self.groups_lookup[data] = group_id            

            elif field == "Trust":
                if data < 0 or data > 100:
                    return False
                
                self.groups_data[group_id]["Trust"] = data

            elif field == "List_of_members":
                # Check if all emails exist
                for email in data:
                    if email not in self.users_lookup:
                        return False
                    
                self.groups_data[group_id]["List_of_members"] = data

            else:
                # This case should have been caught earlier and we should never 
                # execute this line (field not in self.groups_data[group_id])
                return False 

        except RuntimeError:
            return False

        return self.modify_groups_file(self.groups_data)

    ##***********DELETE***********************

    def remove_user(self, user_id):
        '''
        Description: fonction qui suprime l'utilisateur de fichier 'users.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        user_id = str(user_id)

        # Check existence       
        if user_id not in self.users_data:
            return False 
        
        try:
            user_name  = self.get_user_data(user_id, "name")
            
            # Remove user 
            del self.users_data[user_id]
            del self.users_lookup[user_name]

        except RuntimeError:
            return False

        return self.modify_users_file(self.users_data)

    def remove_user_group(self, user_id, group_name):
        '''
        Description: fonction qui suprime de le fichier 'users.json' le groupe 
        auquel appartient un utilisateur.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        user_id  = str(user_id)

        # Check existence       
        if user_id not in self.users_data:
            return False 
        
        try:
            # Get names 
            user_name = self.get_user_data(user_id, "name")

            # Check if the user is in the group
            groups = self.get_user_data(user_id, "Groups")
            if group_name not in groups:
                return False

            # Remove group
            self.users_data[user_id]["Groups"].remove(group_name)

        except RuntimeError:
            return False

        return self.modify_users_file(self.users_data)

    def remove_group(self, group_id):
        '''
        Description: fonction qui suprime le groupe de fichier 'groups.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        group_id = str(group_id)

        # Check existence       
        if group_id not in self.groups_data:
            return False 

        try:
            # Get names 
            group_name = self.get_groups_data(group_id, "name")

            # Remove group
            del self.groups_data[group_id]
            del self.groups_lookup[group_name]

        except RuntimeError:
            return False
        
        return self.modify_groups_file(self.groups_data)

    def remove_group_member(self, group_id, member):
        '''
        Description: fonction qui enleve le membre de le liste des membres pour
        un groupe dans le 'groups.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        group_id = str(group_id)

        # Check existence       
        if group_id not in self.groups_data:
            return False 

        if member not in self.groups_data[group_id]["List_of_members"]:
            return False

        # Remove from group
        self.groups_data[group_id]["List_of_members"].remove(member)

        return self.modify_groups_file(self.groups_data)