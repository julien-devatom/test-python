import json

from email_analyzer import EmailAnalyzer

import unittest
from unittest.mock import patch


class TestEmailAnalyzer(unittest.TestCase):
    def setUp(self):
        self.subject = ""
        self.body = ""
        self.clean_subject = [""]  # données pour mocker "return_value" du "clean_text"
        self.clean_body = [""]  # données pour mocker "return_value" du "clean_text"
        self.spam_ham_body_prob_true = (
            1,
            0,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.spam_ham_subject_prob_true = (
            1,
            0,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.spam_ham_body_prob_false = (
            0,
            1,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.spam_ham_subject_prob_false = (
            0,
            1,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.vocab = {
            "p_sub_spam": {
                "bad_subject": 1
            },
            "p_sub_ham": {
                "good_subject": 1,
                "really_good_subject": 1000
            },
            "p_body_spam": {
                "bad_word": 1
            },
            "p_body_ham": {
                "good_word": 1
            }
        }  # vocabulaire avec les valeurs de la probabilité pour mocker "return_value" du "load_dict"
        self.spam_ham_body_prob_expected = 0, 0  # valeurs de la probabilité attendus
        self.spam_ham_subject_prob_expected = 0, 0  # valeurs de la probabilité attendus

    def tearDown(self):
        pass

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_subject_prob")
    def test_is_spam_Returns_True_if_spam_prob_is_higher(
            self, mock_spam_ham_subject_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être True si probabilité spam > probabilité ham
        """
        mock_spam_ham_subject_prob.return_value = self.spam_ham_subject_prob_true  # spam > ham
        mock_spam_ham_body_prob.return_value = self.spam_ham_body_prob_true  # spam > ham
        analyzer = EmailAnalyzer()
        self.assertTrue(analyzer.is_spam("", ""))

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_subject_prob")
    def test_is_spam_Returns_False_if_spam_prob_is_lower(
            self, mock_spam_ham_subject_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être False si probabilité spam  probabilité ham
        """

        mock_spam_ham_subject_prob.return_value = self.spam_ham_subject_prob_false  # spam < ham
        mock_spam_ham_body_prob.return_value = self.spam_ham_body_prob_false  # spam < ham
        analyzer = EmailAnalyzer()
        self.assertFalse(analyzer.is_spam("", ""))

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_spam_ham_body_prob_Returns_expected_probability(self, mock_load_dict):
        """
        Il faut mocker la fonction "load_dict"
        Il faut vérifier que probabilité est calculée correctement donné le "body" à l'entrée



        INFO : J'ai remplacé la ligne 53 de email_analyzer par
                for word in body.split(" "):
            car on bouclait sur les caractères et non les mots
        """
        mock_load_dict.return_value = self.vocab
        analyzer = EmailAnalyzer()
        p_spam, p_ham = analyzer.spam_ham_body_prob("bad_word")
        self.assertGreater(p_spam, p_ham)  # on vérifir que le mot est bien qualifié de spam

        # Et que les probas sont corrects
        p_spam_expected = 0.5925
        p_ham_expected = 0.20375
        self.assertEqual(p_spam, p_spam_expected)
        self.assertEqual(p_ham, p_ham_expected)

        p_spam, p_ham = analyzer.spam_ham_body_prob("neutral sentence without bad words and with a good_word")
        self.assertGreater(p_ham,
                           p_spam)  # on vérifir que le mot est bien qualifié de ham seulement, car effectuer la formule commence a être lourd

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_subject_spam_ham_prob_Returns_expected_probability(self, mock_load_dict):
        """
        Il faut mocker la fonction "load_dict"
        il faut vérifier que probabilité est calculée correctement donné le "sujet" a l'entrée
        """
        mock_load_dict.return_value = self.vocab
        analyzer = EmailAnalyzer()
        p_spam, p_ham = analyzer.spam_ham_subject_prob("bad_subject".split(" "))
        self.assertGreater(p_spam, p_ham)  # on vérifir que le sujet est bien qualifié de spam

        mock_load_dict.return_value = self.vocab
        analyzer = EmailAnalyzer()
        p_spam, p_ham = analyzer.spam_ham_subject_prob("bad_subject good_subject".split(" "))
        self.assertGreater(p_spam, p_ham)  # on vérifir que le spam est toujours un peu plus fort que le ham

        mock_load_dict.return_value = self.vocab
        analyzer = EmailAnalyzer()
        p_spam, p_ham = analyzer.spam_ham_subject_prob("bad_subject really_good_subject".split(" "))
        self.assertGreater(p_ham, p_spam)  # Le bon mot est plus puissant

        p_spam, p_ham = analyzer.spam_ham_subject_prob("good_subject".split(" "))
        self.assertGreater(p_ham, p_spam)  # Sujet non spam

        p_spam, p_ham = analyzer.spam_ham_subject_prob("Neutral subject".split(" "))
        self.assertGreater(p_spam, p_ham )  # Sujet neutre devient spam

