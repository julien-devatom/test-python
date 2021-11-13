from unittest import TestCase

from src.crud import CRUD


class TestCrudMadum(TestCase):

    def setUp(self) -> None:
        self.initial_users_data = {}
        self.initial_groups_data = {}

    #################################
    #       Tests of constructors   #
    #################################
    def test_constructor_for_users_data_slice(self):
        crud = CRUD(_users_data=self.initial_users_data)
        self.assertEqual(crud.users_data, self.initial_users_data)

