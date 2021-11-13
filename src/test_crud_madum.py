from datetime import timezone, datetime
from unittest import TestCase

from src.crud import CRUD

DEFAULT_HAM = 0
DEFAULT_SPAM = 0
DEFAULT_TRUST = 50
DEFAULT_GROUPS = ["default"]


def get_timestamp(date):
    dt = datetime.strptime(date, '%Y-%m-%d')
    return dt.replace(tzinfo=timezone.utc).timestamp()


class TestCrudMadum(TestCase):
    def setUp(self) -> None:
        self.initial_users_data = {'0': {
            'name': 'user1@example.com',
            'Date_of_first_seen_message': get_timestamp('2021-01-01'),
            'Date_of_last_seen_message': get_timestamp('2021-01-01'),
            'Groups': ['default', 'funny'],
            'HamN': DEFAULT_HAM,
            'SpamN': DEFAULT_SPAM,
            'Trust': DEFAULT_TRUST
        }}
        self.initial_groups_data = {}
        self.user = {
            "name": "test@example.com",
            "Trust": 100,
            "SpamN": 0,
            "HamN": 20,
            "Date_of_first_seen_message": 1596844800.0,
            "Date_of_last_seen_message": 1596844800.0,
            "Groups": ["default"],
        }
        self.crud = CRUD(_users_data=self.initial_users_data, _groups_data=self.initial_groups_data)


    #################################
    #       Tests of constructors   #
    #################################
    def test_constructor_for_users_data_slice(self):
        crud = CRUD(_users_data=self.initial_users_data)
        self.assertEqual(crud.users_data, self.initial_users_data)


    #################################
    #       Tests of getters   #
    #################################
    def test_get_user_data_for_users_data_slice(self):

        self.assertEqual(self.initial_users_data['0']['Trust'], self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(self.initial_users_data['0']['name'], self.crud.get_user_data(0, 'name'))
        self.assertEqual(self.initial_users_data['0']['Date_of_first_seen_message'], self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(self.initial_users_data['0']['Date_of_last_seen_message'], self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(self.initial_users_data['0']['SpamN'], self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(self.initial_users_data['0']['HamN'], self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(self.initial_users_data['0']['Groups'], self.crud.get_user_data(0, 'Groups'))

    def test_get_user_id_for_users_data_slice(self):
        self.assertEqual('0', self.crud.get_user_id(self.initial_users_data['0']['name']))


    #################################
    #       Tests of transformers   #
    #################################
    """
    Pour savoir l'ordre des tests effectué lors d'un test Tx, avec x dans [1, 24], 
    vous pouvez vous référer au rapport, ou au fichier transformers_tests.csv,
    qui contient l'ordre des tests
    """
    def test_transformer_T1_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.remove_user('0')
        self.crud.remove_user_group('1', 'funny')

        self.assertEqual('0', self.crud.get_new_user_id())  # replace the removed user
        self.assertEqual('1', self.crud.get_user_id(new_user_email))
        self.assertEqual(update_trust_value, self.crud.get_user_data(1, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(1, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(1, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(1, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(1, 'Groups'))

    def test_transformer_T2_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.remove_user_group('1', 'funny')
        self.crud.remove_user('0')

        self.assertEqual('0', self.crud.get_new_user_id())  # replace the removed user
        self.assertEqual('1', self.crud.get_user_id(new_user_email))
        self.assertEqual(update_trust_value, self.crud.get_user_data(1, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(1, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(1, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(1, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(1, 'Groups'))

    def test_transformer_T3_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.remove_user('0')
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.remove_user_group('1', 'funny')

        self.assertEqual('0', self.crud.get_new_user_id())  # replace the removed user
        self.assertEqual('1', self.crud.get_user_id(new_user_email))
        self.assertEqual(update_trust_value, self.crud.get_user_data(1, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(1, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(1, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(1, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(1, 'Groups'))

    def test_transformer_T4_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.remove_user('0')
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.remove_user_group('1', 'funny')

        self.assertEqual('0', self.crud.get_new_user_id())  # replace the removed user
        self.assertEqual('1', self.crud.get_user_id(new_user_email))
        self.assertEqual(update_trust_value, self.crud.get_user_data(1, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(1, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(1, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(1, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(1, 'Groups'))

    def test_transformer_T5_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        last_seen_message_date = "2021-11-15" # after new_user_date
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.remove_user('0')
        self.crud.remove_user_group('1', 'funny')
        self.crud.update_users(1, 'Date_of_last_seen_message', last_seen_message_date)

        self.assertEqual('0', self.crud.get_new_user_id())  # replace the removed user
        self.assertEqual('1', self.crud.get_user_id(new_user_email))
        self.assertEqual(get_timestamp(last_seen_message_date), self.crud.get_user_data(self.crud.get_user_id(new_user_email), 'Date_of_last_seen_message'))
        self.assertEqual(new_user_email, self.crud.get_user_data(1, 'name'))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(1, 'Trust'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_first_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(1, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(1, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(1, 'Groups'))

    def test_transformer_T6_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.remove_user_group('1', 'funny')
        self.crud.remove_user('0')
        self.crud.update_users(1, 'Trust', update_trust_value)

        self.assertEqual('0', self.crud.get_new_user_id())  # replace the removed user
        self.assertEqual('1', self.crud.get_user_id(new_user_email))
        self.assertEqual(update_trust_value, self.crud.get_user_data(1, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(1, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(1, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(1, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(1, 'Groups'))

    def test_transformer_T7_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.update_users(1, 'Trust', update_trust_value)  # Update user which not exist
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.remove_user('0')
        self.crud.remove_user_group('1', 'funny')

        self.assertEqual('0', self.crud.get_new_user_id())  # replace the removed user
        self.assertEqual('1', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(1, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(1, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(1, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(1, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(1, 'Groups'))

    def test_transformer_T8_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.remove_user_group('1', 'funny')
        self.crud.remove_user('0')

        self.assertEqual('0', self.crud.get_new_user_id())  # replace the removed user
        self.assertEqual('1', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(1, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(1, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(1, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(1, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(1, 'Groups'))

    def test_transformer_T9_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.remove_user('0')
        self.crud.remove_user_group('1', 'funny')
        self.crud.add_new_user(new_user_email, new_user_date)

        # There is only one user in users_data
        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T10_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.remove_user('0')
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.remove_user_group('1', 'funny')

        # There is only one user in users_data
        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T11_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.remove_user('0')
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.remove_user_group('1', 'funny')
        self.crud.update_users(1, 'Trust', update_trust_value)

        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T12_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.remove_user_group('1', 'funny')
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.remove_user('0')
        self.crud.update_users(1, 'Trust', update_trust_value)

        self.assertEqual('0', self.crud.get_new_user_id())
        self.assertEqual('1', self.crud.get_user_id(new_user_email))
        self.assertEqual(update_trust_value, self.crud.get_user_data(1, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(1, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(1, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(1, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(1, 'Groups'))

    def test_transformer_T13_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.remove_user('0')
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.remove_user_group('1', 'funny')

        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T14_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.remove_user('0')
        self.crud.remove_user_group('1', 'funny')
        self.crud.add_new_user(new_user_email, new_user_date)

        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T15_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.remove_user('0')
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.remove_user_group('1', 'funny')

        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T16_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.remove_user_group('1', 'funny')
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.remove_user('0')

        self.assertEqual('0', self.crud.get_new_user_id())
        self.assertEqual('1', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(1, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(1, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(1, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(1, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(1, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(1, 'Groups'))

    def test_transformer_T17_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.remove_user('0')
        self.crud.remove_user_group('1', 'funny')
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.update_users(1, 'Trust', update_trust_value)

        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T18_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.remove_user('0')
        self.crud.remove_user_group('1', 'funny')
        self.crud.add_new_user(new_user_email, new_user_date)
        self.crud.update_users(1, 'Trust', update_trust_value)

        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T19_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.remove_user('0')
        self.crud.remove_user_group('1', 'funny')
        self.crud.add_new_user(new_user_email, new_user_date)

        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T20_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.remove_user_group('1', 'funny')
        self.crud.remove_user('0')
        self.crud.add_new_user(new_user_email, new_user_date)

        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T21_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.remove_user('0')
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.remove_user_group('1', 'funny')
        self.crud.add_new_user(new_user_email, new_user_date)

        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T22_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.remove_user_group('1', 'funny')
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.remove_user('0')
        self.crud.add_new_user(new_user_email, new_user_date)

        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T23_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.remove_user('0')
        self.crud.remove_user_group('1', 'funny')
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.add_new_user(new_user_email, new_user_date)

        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))

    def test_transformer_T24_for_users_data_slice(self):
        new_user_email = "new_user@example.com"
        new_user_date = "2021-11-13"
        update_trust_value = 60
        self.crud.remove_user_group('1', 'funny')
        self.crud.remove_user('0')
        self.crud.update_users(1, 'Trust', update_trust_value)
        self.crud.add_new_user(new_user_email, new_user_date)

        self.assertEqual('1', self.crud.get_new_user_id())
        self.assertEqual('0', self.crud.get_user_id(new_user_email))
        self.assertEqual(DEFAULT_TRUST, self.crud.get_user_data(0, 'Trust'))
        self.assertEqual(new_user_email, self.crud.get_user_data(0, 'name'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_first_seen_message'))
        self.assertEqual(get_timestamp(new_user_date), self.crud.get_user_data(0, 'Date_of_last_seen_message'))
        self.assertEqual(DEFAULT_SPAM, self.crud.get_user_data(0, 'SpamN'))
        self.assertEqual(DEFAULT_HAM, self.crud.get_user_data(0, 'HamN'))
        self.assertEqual(DEFAULT_GROUPS, self.crud.get_user_data(0, 'Groups'))
