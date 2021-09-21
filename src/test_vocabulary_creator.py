from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch


class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        self.mails = {
            "dataset": [
                {
                    "mail": {
                        "Subject": "A spam spam subject",
                        "From": "GP@paris.com",
                        "Date": "2005-03-04",
                        "Body": "Not a good body, is a spam spam",
                        # on répète 2x le mot spam pour une meilleure couverture
                        "Spam": "true",
                        "File": "enronds//enron4/spam/4536.2005-03-04.GP.spam.txt"
                    }
                },
                {
                    "mail": {
                        "Subject": "A nice nice subject",
                        "From": "GP@paris.com",
                        "Date": "2004-03-09",
                        "Body": "Wow! really really nice mail",
                        # on répète 2 fois le mot ready pour une meilleure couverture
                        "Spam": "false",
                        "File": "enronds//enron4/spam/0559.2004-03-09.GP.spam.txt"
                    }
                }
            ]}  # données pour mocker "return_value" du "load_dict"
        self.clean_subject_spam = ["spam", "subject"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_spam = ["Not", "a", "good", "body"]  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_ham = ["good", "subject"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_ham = ["really", "good", "mail"]  # données pour mocker "return_value" du "clean_text"
        self.vocab_expected = {
            'p_body_ham': {'Wow!': 0.2, 'mail': 0.2, 'nice': 0.2, 'really': 0.4},
            'p_body_spam': {
                'Not': 0.125,
                'a': 0.25,
                'body,': 0.125,
                'good': 0.125,
                'is': 0.125,
                'spam': 0.25},
            'p_sub_ham': {
                'A': 0.25, 'nice': 0.5, 'subject': 0.25},
            'p_sub_spam': {
                'A': 0.25, 'spam': 0.5, 'subject': 0.25}}  # vocabulaire avec les valuers de la probabilité calculées correctement

    def tearDown(self):
        pass

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.VocabularyCreator.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_spam_Returns_vocabulary_with_correct_values(
            self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        """Description: Tester qu'un vocabulaire avec les probabilités calculées
        correctement va être retourné. Il faut mocker les fonctions "load dict"
         (utiliser self.mails comme un return value simulé),"clean text"
         (cette fonction va être appelé quelques fois, pour chaque appel on
         va simuler la return_value different, pour cela il faut utiliser
         side_effect (vois l'exemple dans l'énonce)) et
         "write_data_to_vocab_file" qui va simuler "return True" au lieu
         d'écrire au fichier "vocabulary.json".
         if faut utiliser self.assertEqual(appele_a_create_vocab(), self.vocab_expected)
        """

        # On défini les mocks

        mock_load_dict.return_value = self.mails
        mock_clean_text.side_effect = lambda text: text.split(
            ' ')  # Dans le cadre de mùes tests, je sais que je peux obtenir la liste des mots de chaque sujet et chaque body simplement en séparant par des espaces
        mock_write_data_to_vocab_file.return_value = True

        # On test le fonctionnement
        creator = VocabularyCreator()
        creator.create_vocab()

        # Et on vérifie que le vocabulaire est bien défini
        self.assertEqual(creator.voc_data, self.vocab_expected)

    ###########################################
    #               CUSTOM TEST               #
    ###########################################
