import secrets

from crud import CRUD
import unittest
from unittest.mock import patch

from datetime import datetime, timezone


class TestCRUD(unittest.TestCase):
    def setUp(self):
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_users_file
        self.users_data = {
            "1": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default", "friends"],
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "SpamN": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }
        }
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_groups_file
        self.groups_data = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

    def tearDown(self):
        pass

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_add_new_user_Passes_correct_data_to_modify_users_file(
            self, mock_modify_users_file, mock_modify_groups_file, mock_read_users_file,
            mock_read_groups_file
    ):
        """Description: il faut utiliser les mocks des fonctions "read_users_file",
        "modify_users_file", "modify_groups_file" (ou selon votre realisation) pour tester que
        l'information a ajouter pour l'utilisateur a été formée correctement par la fonction, e.g.
        self.modify_users_file(data) -> "data" doit avoir un format et contenu expectee
        il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        # on utilise nos fixtures
        # On vérifie que le fichier utilisateur a bien été appelé.
        mock_read_users_file.assert_called_once()

        # On ajoute l'utilisateur
        crud.add_new_user("test@example.com", "1998-04-18")

        # Transformation de la date pour obtenir le timestamp
        dt = datetime.strptime("1998-04-18", '%Y-%m-%d')
        date = dt.replace(tzinfo=timezone.utc).timestamp()

        # La forme que doit avoir le nouvel utilisateur dans le
        current_data = {'0': {
            "name": "test@example.com",
            "Trust": 50,
            "SpamN": 0,
            "HamN": 0,
            "Date_of_first_seen_message": date,
            "Date_of_last_seen_message": date,
            "Groups": ["default"]
        }}
        # Est ce que le nouvel utilisateur est bien ajouté en tête de dictionnaire pour la modification ?
        mock_modify_users_file.assert_called_once_with({**self.users_data, **current_data})

        # est ce que l'adresse email a bien été ajoutée au groupe par défault pour la modification ?
        mock_modify_groups_file.assert_called_once_with({'1': {'name': 'default', 'Trust': 50,
                                                               'List_of_members': ['alex@gmail.com', 'mark@mail.com',
                                                                                   'test@example.com']},
                                                         '2': {'name': 'friends', 'Trust': 90,
                                                               'List_of_members': ['alex@gmail.com']}})
        # Est ce que le noubvel utilisateur a été ajouté au groupe par défault
        # self.assertIn('test@example.com', crud.groups_data['1']['List_of_members'])

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_add_new_group_Passes_correct_data_to_modify_groups_file(
            self, mock_modify_groups_file, mock_read_groups_file
    ):
        """Description: il faut utiliser les mocks des fonctions "read_groups_file",
        "modify_groups_file" (ou selon votre realisation) pour tester que
        l'information a ajouter pour le groupe a étée formée correctement par la fonction e.g.
        self.modify_groups_file(data) -> "data" doit avoir un format et contenu attendu
        il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        # On vérifie si la fonction est bien appelé à l'initialisation
        mock_read_groups_file.assert_called_once()
        crud.add_new_group("group_test", 50, [])
        new_group = {'0': {'name': 'group_test', 'Trust': 50, 'List_of_members': []}}

        # Est ce que le nouveau groupe a bien été ajouté en fin de dictionnaire ?
        mock_modify_groups_file.assert_called_once_with({**self.groups_data, **new_group})

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_id(self, mock_read_users_file):
        """Description: il faut utiliser le mock de fonction "read_users_file",
        (ou selon votre realisation) pour tester que false (ou bien une excepton)
        est returnee par la fonction si ID non-existant est utilisée
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        # nos fixtures ne contiennent pas de user avec un id de 10
        self.assertFalse(crud.get_user_data(10, 'name'))

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_field(self, mock_read_users_file):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que false (ou bien une excepton)
        est returnee par la fonction si champ non-existant est utilisée
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        # nos fixtures contiennent un user avec un id de 10, mais pas le champ renseigné
        self.assertFalse(crud.get_user_data(1, 'not_existing_field_' + str(secrets.token_hex(11))))

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_correct_value_if_field_and_id_are_valid(
            self, mock_read_users_file
    ):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que une bonne valeur est fournie
        si champ est id valide sont utilisee
        il faut utiliser ".assertEqual()""
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        # On vérifie que ca marche pour chaque champ !
        for field, value in self.users_data['1'].items():
            self.assertEqual(crud.get_user_data(1, field), value)

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_id(self, mock_read_groups_file):
        """
        Similare test_get_user_data_Returns_false_for_invalid_id
        """
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        # nos fixtures ne contiennent pas de user avec un id de 10
        self.assertFalse(crud.get_groups_data(10, 'name'))

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_field(
            self, mock_read_groups_file
    ):
        """
        Similare test_get_user_data_Returns_false_for_invalid_field
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        # nos fixtures ne contiennent pas de user avec un id de 10
        self.assertFalse(crud.get_groups_data(1, 'not_existing_field_' + str(secrets.token_hex(11))))

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_correct_value_if_field_and_id_are_valid(
            self, mock_read_groups_file
    ):
        """
        Similare test_get_user_data_Returns_correct_value_if_field_and_id_are_valid
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()

        # On vérifie que ca marche pour chaque champ !
        for field, value in self.groups_data['1'].items():
            self.assertEqual(crud.get_groups_data(1, field), value)

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_false_for_invalid_user_name(
            self, mock_read_users_file
    ):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.get_user_id("not_existing_name@example.com"))

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_id_for_valid_user_name(self, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.get_user_id("alex@gmail.com"), '1')

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_false_for_invalid_group_name(
            self, mock_read_groups_file
    ):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.get_group_id("not_existing_group_name"))

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_id_for_valid_group_name(self, mock_read_groups_file):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertEqual("1", crud.get_group_id("default"))

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    # Modify_user_file mock est inutile pour tester False pour update
    # On peut vérifier que la méthode n'est pas appelée
    def test_update_users_Returns_false_for_invalid_id(
            self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.update_users(10, 'name', 'fake_name@test.com'))

        # On peut vérifier que la méthode modify_users_file n'est pas appelée
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_for_invalid_field(
            self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.update_users(1, 'not_existing_field_' + str(secrets.token_hex(11)), 'fake_name@test.com'))
        # On peut vérifier que la méthode modify_users_file n'est pas appelée
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_data_to_modify_users_file(
            self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        crud.update_users(1, 'name', 'fake_name@test.com')

        # on vérifie l'appel à la fonction modify_users_file
        updated_data = {
            "1": {
                "name": "fake_name@test.com",  # nouveau name
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default", "friends"]
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "SpamN": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }
        }
        mock_modify_users_file.assert_called_once_with(updated_data)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_id(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.update_groups(10, 'name', 'new_default'))

        # On peut vérifier que la méthode modify_groups_file n'est pas appelée
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_name_format(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.update_groups(1, 'name', ''))  # too short
        self.assertFalse(crud.update_groups(1, 'name', '1' * 70))  # too long

        # On peut vérifier que la méthode modify_groups_file n'est pas appelée
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_field(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.update_groups(1, 'not_existing_field', 'new_default'))

        # On peut vérifier que la méthode modify_groups_file n'est pas appelée
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Passes_correct_data_to_modify_groups_file(
            self, mock_read_groups_file, mock_modify_groups_file, mock_read_users_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.update_groups('2', 'name', 'old_friends')  # on modifie pas le groupe default qui est particulier

        # On peut vérifier que la méthode modify_groups_file est bien appelé
        new_groups = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "2": {
                "name": "old_friends",  # new value
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }
        mock_modify_groups_file.assert_called_once_with(new_groups)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_Returns_false_for_invalid_id(
            self, mock_read_users_file, mock_modify_users_file
    ):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.remove_user(10))

        # On peut vérifier que la méthode modify_users_file n'est pas appelée
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_Passes_correct_value_to_modify_users_file(
            self, mock_read_users_file, mock_modify_users_file
    ):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        crud.remove_user(1)

        # On peut vérifier que la méthode modify_users_file n'est pas appelée
        new_users_data = {
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "SpamN": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }
        }
        mock_modify_users_file.assert_called_once_with(new_users_data)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Returns_false_for_invalid_id(
            self, mock_read_users_file, mock_modify_users_file
    ):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.remove_user_group(10, 'default'))

        # On peut vérifier que la méthode modify_users_file ne sont pas appelées
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Returns_false_for_invalid_group(
            self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        # on vérifie avec un groupe qui n'existe pas
        self.assertFalse(crud.remove_user_group(1, 'not_existing_group'))

        # et un groupe qui ne contient pas l'utilisateur
        self.assertFalse(crud.remove_user_group(2, 'friends'))  # 2 n'est pas dans le groupe friends

        # On peut vérifier que la méthode modify_users_file ne sont pas appelées
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Passes_correct_value_to_modify_users_file(
            self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        # on vérifie avec un groupe qui n'existe pas
        crud.remove_user_group(1, 'friends')

        new_users_data = {'1': {'name': 'alex@gmail.com', 'Trust': 100, 'SpamN': 0, 'HamN': 20,
                                'Date_of_first_seen_message': 1596844800.0, 'Date_of_last_seen_message': 1596844800.0,
                                'Groups': ['default']},
                          '2': {'name': 'mark@mail.com', 'Trust': 65.45454, 'SpamN': 171, 'HamN': 324,
                                'Date_of_first_seen_message': 1596844800.0, 'Date_of_last_seen_message': 1596844800.0,
                                'Groups': ['default']}}
        mock_modify_users_file.assert_called_once_with(new_users_data)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_Returns_false_for_invalid_id(
            self, mock_read_groups_file, mock_modify_groups_file
    ):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.remove_group(10))

        # On peut vérifier que la méthode modify_users_file ne sont pas appelées
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_Passes_correct_value_to_modify_groups_file(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group(2)  # on remove le groupe friends

        mock_modify_groups_file.assert_called_once_with(
            {'1': {'name': 'default', 'Trust': 50, 'List_of_members': ['alex@gmail.com', 'mark@mail.com']}})

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_member_Returns_false_for_invalid_id(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.remove_group_member(10, 'alex@gmail.com'))

        # On peut vérifier que la méthode mock_modify_groups_file n'est pas appelée
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_member_Returns_false_for_invalid_group_member(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.remove_group_member(1, 'not_a_member@example.com'))

        # on test un utilisateur existant mais qui n'appartient pas au groupe renseigné
        self.assertFalse(crud.remove_group_member(2, 'mark@mail.com'))  # mark n'est pas dans friends

        # On peut vérifier que la méthode mock_modify_groups_file n'est pas appelée
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_member_Passes_correct_value_to_modify_groups_file(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member(2, 'alex@gmail.com')

        # On peut vérifier que la méthode mock_modify_groups_file n'est pas appelée
        mock_modify_groups_file.assert_called_once_with(
            {'1': {'name': 'default', 'Trust': 50, 'List_of_members': ['alex@gmail.com', 'mark@mail.com']},
             '2': {'name': 'friends', 'Trust': 90, 'List_of_members': []}})

    ###########################################
    #               CUSTOM TEST               #
    ###########################################

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_open_not_existing_file(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.side_effect = FileNotFoundError
        mock_read_groups_file.side_effect = FileNotFoundError
        crud = CRUD()

        # les méthodes sont appelés
        mock_read_users_file.assert_called_once()  # read user file va générer une erreur
        mock_read_groups_file.assert_not_called()  # et read_groups_file ne sera pas appelé

        self.assertDictEqual(crud.groups_data, {
            '0': {'List_of_members': [], 'Trust': 50, 'name': 'default'}})  # seul le groupe par défaut est ajouté
        self.assertDictEqual(crud.users_data, {})  # aucun utilisateur n'est défini

    def test_convert_to_unix_Returns_correct_timestamp(self):
        crud = CRUD()
        self.assertEqual(crud.convert_to_unix("2021-09-10"), 1631232000.0)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_add_new_user_with_an_existing_name_Returns_False(self,
                                                              mock_read_users_file, mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.add_new_user('alex@gmail.com', '2021-09-10'))
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_add_new_user_with_invalid_email_format_Returns_False(self,
                                                                  mock_read_users_file, mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.add_new_user('not_an_email', '2021-09-10'))
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_with_invalid_email_format_Returns_False(self,
                                                                  mock_read_users_file, mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.update_users(1, "name", "not_an_email"))
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_with_invalid_Date_of_last_seen_message_Returns_False(self,
                                                                               mock_read_users_file,
                                                                               mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.update_users(1, "Date_of_last_seen_message", "1900-06-06"))
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_with_invalid_Date_of_first_seen_message_Returns_False(self,
                                                                                mock_read_users_file,
                                                                                mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.update_users(1, "Date_of_first_seen_message", "2200-06-06"))
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_with_valid_Date_of_first_seen_message_Passes_correct_value_to_modify_users_file(self,
                                                                                                          mock_read_users_file,
                                                                                                          mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        new_date = "1200-06-06"
        self.assertTrue(crud.update_users(1, "Date_of_first_seen_message", new_date))
        timestamp = crud.convert_to_unix(new_date)
        mock_modify_users_file.assert_called_once_with({'1': {'name': 'alex@gmail.com', 'Trust': 100, 'SpamN': 0,
                                                              'HamN': 20, 'Date_of_first_seen_message': timestamp,
                                                              'Date_of_last_seen_message': 1596844800.0,
                                                              'Groups': ['default', 'friends']},
                                                        '2': {'name': 'mark@mail.com', 'Trust': 65.45454, 'SpamN': 171,
                                                              'HamN': 324, 'Date_of_first_seen_message': 1596844800.0,
                                                              'Date_of_last_seen_message': 1596844800.0,
                                                              'Groups': ['default']}})

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_with_valid_Date_of_last_seen_message_Passes_correct_value_to_modify_users_file(self,
                                                                                                         mock_read_users_file,
                                                                                                         mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        new_date = "2200-06-06"
        self.assertTrue(crud.update_users(1, "Date_of_last_seen_message", new_date))
        timestamp = crud.convert_to_unix(new_date)
        mock_modify_users_file.assert_called_once_with({'1': {'name': 'alex@gmail.com', 'Trust': 100, 'SpamN': 0,
                                                              'HamN': 20, 'Date_of_first_seen_message': 1596844800.0,
                                                              'Date_of_last_seen_message': timestamp,
                                                              'Groups': ['default', 'friends']},
                                                        '2': {'name': 'mark@mail.com', 'Trust': 65.45454, 'SpamN': 171,
                                                              'HamN': 324, 'Date_of_first_seen_message': 1596844800.0,
                                                              'Date_of_last_seen_message': 1596844800.0,
                                                              'Groups': ['default']}})

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_with_invalid_Trust_value_Returns_False(self,
                                                                 mock_read_users_file, mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.update_users(1, "Trust", -10))  # Trust doit être entre 0 et 100
        self.assertFalse(crud.update_users(1, "Trust", 101))  # Trust doit être entre 0 et 100
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_with_correct_Trust_value_Passes_correct_value_to_modify_users_file(self,
                                                                                             mock_read_users_file,
                                                                                             mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        crud.update_users(1, "Trust", 10)  # Trust doit être entre 0 et 100
        mock_modify_users_file.assert_called_once_with({'1': {'name': 'alex@gmail.com', 'Trust': 10, 'SpamN': 0,
                                                              'HamN': 20, 'Date_of_first_seen_message': 1596844800.0,
                                                              'Date_of_last_seen_message': 1596844800.0,
                                                              'Groups': ['default', 'friends']},
                                                        '2': {'name': 'mark@mail.com', 'Trust': 65.45454, 'SpamN': 171,
                                                              'HamN': 324, 'Date_of_first_seen_message': 1596844800.0,
                                                              'Date_of_last_seen_message': 1596844800.0,
                                                              'Groups': ['default']}})

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_with_invalid_SpamN_and_HamN_values_Returns_False(self,
                                                                           mock_read_users_file,
                                                                           mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.update_users(1, "SpamN", -1))
        self.assertFalse(crud.update_users(1, "HamN", -1))
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_with_correct_SpamN_and_HamN_values_Passes_correct_value_to_modify_users_file(self,
                                                                                                       mock_read_users_file,
                                                                                                       mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        new_value = 1000
        self.assertTrue(crud.update_users(1, "SpamN", new_value))
        mock_modify_users_file.assert_called_once_with({'1': {'name': 'alex@gmail.com', 'Trust': 100,
                                                              'SpamN': new_value, 'HamN': 20,
                                                              'Date_of_first_seen_message': 1596844800.0,
                                                              'Date_of_last_seen_message': 1596844800.0,
                                                              'Groups': ['default', 'friends']},
                                                        '2': {'name': 'mark@mail.com', 'Trust': 65.45454, 'SpamN': 171,
                                                              'HamN': 324, 'Date_of_first_seen_message': 1596844800.0,
                                                              'Date_of_last_seen_message': 1596844800.0,
                                                              'Groups': ['default']}})

        # Les 2 tests couvrent le même code
        self.assertTrue(crud.update_users(1, "HamN", new_value))
        mock_modify_users_file.assert_called_with({'1': {'name': 'alex@gmail.com', 'Trust': 100, 'SpamN': new_value,
                                                         'HamN': new_value, 'Date_of_first_seen_message': 1596844800.0,
                                                         'Date_of_last_seen_message': 1596844800.0,
                                                         'Groups': ['default', 'friends']},
                                                   '2': {'name': 'mark@mail.com', 'Trust': 65.45454, 'SpamN': 171,
                                                         'HamN': 324, 'Date_of_first_seen_message': 1596844800.0,
                                                         'Date_of_last_seen_message': 1596844800.0,
                                                         'Groups': ['default']}})

    @patch("crud.CRUD.read_users_file")
    def test_add_new_group_with_not_existing_member_Returns_False(self,
                                                                  mock_read_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.add_new_group('new_group', '50', ['not_existing_user@example.com']))

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_get_new_user_id_incrementation(self,
                                            mock_read_users_file, mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()

        # On ajoute 2 nouveaux utilisateurs
        crud.add_new_user("John1@doe.fr", "2021-09-10")  # est sensé avoir l'id 0
        crud.add_new_user("John2@doe.fr",
                          "2021-09-10")  # est sensé avoir un id 3, car il y a déjà 2 utilisateurs dans nos fixtures

        self.assertEqual(crud.get_user_id('John1@doe.fr'), "0")
        self.assertEqual(crud.get_user_id('John2@doe.fr'), "3")

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_new_group_id_incrementation(
            self, mock_read_groups_file, mock_modify_groups_file
    ):

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()

        # On ajoute 2 nouveaux groupes
        crud.add_new_group("group_with_id_0", 10, [])  # est sensé avoir l'id 0
        crud.add_new_group("group_with_id_3", 10,
                           [])  # est sensé avoir un id 3, car il y a déjà 2 utilisateurs dans nos fixtures

        self.assertEqual(crud.get_group_id('group_with_id_0'), "0")
        self.assertEqual(crud.get_group_id('group_with_id_3'), "3")

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_Trust_value(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.update_groups(1, 'Trust', -1))
        self.assertFalse(crud.update_groups(1, 'Trust', 101))

        # On peut vérifier que la méthode modify_groups_file n'est pas appelée
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_with_correct_Trust_value_Passes_correct_value_to_modify_groups_file(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        trust_value = 50
        self.assertTrue(crud.update_groups(1, 'Trust', trust_value))

        # On peut vérifier que la méthode modify_groups_file est appelé avec la nouvelle valeure de trust
        mock_modify_groups_file.assert_called_once_with(
            {'1': {'name': 'default', 'Trust': trust_value, 'List_of_members': ['alex@gmail.com', 'mark@mail.com']},
             '2': {'name': 'friends', 'Trust': 90, 'List_of_members': ['alex@gmail.com']}})

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_List_of_members(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.update_groups(1, 'List_of_members', ['not_existing_user@example.com']))

        # On peut vérifier que la méthode modify_groups_file n'est pas appelée
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_field(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.update_groups(1, 'not_existing_field', None))

        # On peut vérifier que la méthode modify_groups_file n'est pas appelée
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_field(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """

        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.update_groups(1, 'not_existing_field', None))

        # On peut vérifier que la méthode modify_groups_file n'est pas appelée
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_with_invalid_Groups(self,
                                                            mock_read_users_file, mock_modify_users_file):

        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.update_users(1, "Groups", ['not_existing_group']))
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_with_correct_Groups_value_Passes_correct_value_to_modify_users_file(self,
                                                                                              mock_read_users_file,
                                                                                              mock_modify_users_file,
                                                                                              mock_read_groups_file):
        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertTrue(crud.update_users(2, "Groups", ['friends']))
        mock_modify_users_file.assert_called_once_with({'1': {'name': 'alex@gmail.com', 'Trust': 100, 'SpamN': 0,
                                                              'HamN': 20, 'Date_of_first_seen_message': 1596844800.0,
                                                              'Date_of_last_seen_message': 1596844800.0,
                                                              'Groups': ['default', 'friends']},
                                                        '2': {'name': 'mark@mail.com', 'Trust': 65.45454, 'SpamN': 171,
                                                              'HamN': 324, 'Date_of_first_seen_message': 1596844800.0,
                                                              'Date_of_last_seen_message': 1596844800.0,
                                                              'Groups': ['friends']}})

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_add_new_group_with_members_modify_members_groups(self,
                                                              mock_read_users_file, mock_modify_users_file,
                                                              mock_read_groups_file):
        """
        Les members groups sont changés dans l'instance mùais ne sont pas persisté dans les fichiers. Ainsi,
        modify_users_file n'est pas appelé, alors que les utilisateurs ont changés..
        """

        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        new_group = "new_group_for_testing"

        # on crée le nouvreau groupe
        self.assertTrue(crud.add_new_group(new_group, 20, ['alex@gmail.com']))

        # on vérifie qu'il soit bien ajouté pour l'utilisateur alex@gmail.com
        self.assertIn(new_group, crud.users_data['1']["Groups"])
