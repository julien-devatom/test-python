import csv
import json
from unittest import TestCase
import random as rd

from src.main import evaluate
from src.renege import RENEGE
from src.vocabulary_creator import VocabularyCreator

WORDS = ['counselled', 'overneat', 'enzymatically', 'inaptness', 'nonsport', 'cane-trash', 'stealingly', "pandus",
         'guilted', 'electrolytes', 'anethum', 'sorts', 'guiltie', 'wordhood', 'mountainous', 'ingredients',
         'nonfliers', 'misleadingly', 'mahi-mahi', 'unsent', 'puckishness', 'toiletries', 'Nordloh', 'recreancy',
         'chargeful', 'encrypts', 'shantey', 'forment', 'vesuvin', 'stannite', 'anticollision', 'destoor', 'pentamer',
         'overfill', 'unbolts', 'preveniences', 'reasty', 'galega', 'effemination', 'retroelement', 'bunglesome',
         'wooziest', 'hemophilia', 'brewmaster', 'sesbania', 'scratchie', 'wholewheat', 'phonies', 'baudrey',
         'hydrarthrosis', 'subsannation', 'phonotactics', 'metre', 'hijabs', 'outpoints', 'PICCs', 'synchroniser',
         'pushpit', 'achatours', 'ristorante', 'liquorice', 'linkify', 'hutches', 'ground-robin', 'serger', 'nephelium',
         'bioscopic', 'compersion', 'Gran Chaco', 'teocalli', 'theft', 'molle', 'dysteleologist', 'phenakistoscope',
         'sidewinders', 'water-bar', 'watercolor', 'hydrograph', 'outspin', 'runnier', 'divorces', 'columniated',
         'jurant', 'clothe', 'Saskatonian', 'facemask', 'decodings', 'resolutionists', 'kamacite', 'sageship',
         'megalodon', 'isobilateral', 'volcanogenic', 'jovially', 'icaridin', 'addendum', 'conjugative', 'programs',
         'bigheaded', 'fishtailed']


class TestMain(TestCase):
    initial_accuracy = None
    NOISE_THRESHOLD = 10  # On ajoute du bruit si on a plus de 10 mots
    ERROR_THRESHOLD = .03  # On regarde si l'accuracy ne varie pas de plus de 3%
    result_filename = 'result.csv'
    default_train_filename = "train_set.json"
    default_test_filename = "test_set.json"
    train_filename = default_train_filename
    test_filename = default_test_filename
    results = []  # On sauvegarde chaque résultats

    @classmethod
    def setUpClass(cls) -> None:
        print('Initialize accuracy')
        vocab = VocabularyCreator(cls.default_train_filename)
        vocab.create_vocab()
        renege = RENEGE(cls.default_train_filename)
        if not renege.classify_emails():
            raise RuntimeError('Error classify emails')
        evaluation = evaluate(cls.default_test_filename)
        cls.initial_accuracy = evaluation['accuracy']
        cls.property_id = 0  # Numéro de la propriété testée
        # cls.initial_accuracy = 0.68
        print('Initial accuracy : ', cls.initial_accuracy)

    @classmethod
    def tearDownClass(cls) -> None:
        print('Save results')
        print(cls.results)
        with open(cls.result_filename, 'w') as res_csv_file:
            writer = csv.writer(res_csv_file)
            writer.writerow(
                ['property number', 'train filename', 'test filename', 'initial accuracy', 'new accuracy', 'difference',
                 'is test passed'])
            writer.writerows(cls.results)

    def setUp(self) -> None:
        self.train_filename = self.default_train_filename
        self.test_filename = self.default_test_filename
        self.property_id += 1
        self.new_acc = 0
        print("Start test of property n°", self.property_id)

    def tearDown(self) -> None:
        res = [
            str(self.property_id),
            self.train_filename,
            self.test_filename,
            str(self.initial_accuracy),
            str(self.new_acc),
            str(self.get_diff()),
            str(self.get_diff() <= self.ERROR_THRESHOLD)
        ]
        print("Res :", ' '.join(res))
        self.results.append(res)  # Save results

    def test_property1(self) -> None:
        """
        changement de l’ordre des e-mails dans le ”train dataset”
        """
        trainset = self._load_data("train_set.json")['dataset']
        self.assertIsInstance(trainset, list)
        rd.shuffle(trainset)
        self.train_filename = "train700_mails.json"
        self._save_data(self.train_filename, {"dataset": trainset})
        self.new_acc = self._test_from_filenames()
        diff = self.get_diff()
        self.assertLessEqual(diff, self.ERROR_THRESHOLD,
                             "Le changement d'ordre des emails dans le trainset modifie trop l'accuracy")

    def test_property2(self) -> None:
        """
        changement de l’ordre des e-mails dans le ”test dataset”
        """
        testset = self._load_data("test_set.json")['dataset']
        self.assertIsInstance(testset, list)
        rd.shuffle(testset)
        self.test_filename = "test300_mails.json"
        self._save_data(self.test_filename, {"dataset": testset})
        self.new_acc = self._test_from_filenames()
        diff = self.get_diff()
        self.assertLessEqual(diff, self.ERROR_THRESHOLD,
                             "Le changement d'ordre des emails dans le testset modifie trop l'accuracy")

    def test_property3(self) -> None:
        """
        changement de l’ordre des mots dans le ”train dataset”
        """
        trainset = self._load_data("train_set.json")['dataset']

        shuffled_emails_words = list(map(self._shuffle_email_words, trainset))

        self.train_filename = "train700_words.json"
        self._save_data(self.train_filename, {"dataset": shuffled_emails_words})
        self.new_acc = self._test_from_filenames()
        diff = self.get_diff()
        self.assertLessEqual(diff, self.ERROR_THRESHOLD,
                             "Le changement d'ordre des mots dans le 'train dataset' modifie trop l'accuracy")

    def test_property4(self) -> None:
        """
        changement de l’ordre des mots dans le ”test dataset”
        """
        testset = self._load_data("test_set.json")['dataset']

        shuffled_emails_words = list(map(self._shuffle_email_words, testset))

        self.test_filename = "test300_words.json"
        self._save_data(self.test_filename, {"dataset": shuffled_emails_words})
        self.new_acc = self._test_from_filenames()
        diff = self.get_diff()
        self.assertLessEqual(diff, self.ERROR_THRESHOLD,
                             "Le changement d'ordre des mots dans le 'test dataset' modifie trop l'accuracy")

    def test_property5(self) -> None:
        """
        ’ajout des mˆemes e-mails dans le ”train dataset”
        """
        trainset = self._load_data("train_set.json")['dataset']

        trainset = trainset + trainset

        self.train_filename = "train700x2.json"
        self._save_data(self.train_filename, {"dataset": trainset})
        self.new_acc = self._test_from_filenames()
        diff = self.get_diff()
        self.assertLessEqual(diff, self.ERROR_THRESHOLD,
                             "Le changement d'ordre des mots dans le 'train dataset' modifie trop l'accuracy")

    def test_property6(self) -> None:
        """
        ’ajout des mˆemes e-mails dans le ”test dataset”
        """
        testset = self._load_data("test_set.json")['dataset']

        testset = testset + testset

        self.test_filename = "test300x2.json"
        self._save_data(self.test_filename, {"dataset": testset})
        self.new_acc = self._test_from_filenames()
        diff = self.get_diff()
        self.assertLessEqual(diff, self.ERROR_THRESHOLD,
                             "Le changement d'ordre des mots dans le 'test dataset' modifie trop l'accuracy")

    def test_property7(self) -> None:
        """
         ajout du ”bruit” dans le ”train dataset”
        """
        trainset = self._load_data("train_set.json")['dataset']
        trainset = list(map(self._add_email_noise, trainset))

        self.train_filename = "train700_noise.json"
        self._save_data(self.train_filename, {"dataset": trainset})
        self.new_acc = self._test_from_filenames()
        diff = self.get_diff()
        self.assertLessEqual(diff, self.ERROR_THRESHOLD,
                             "Le changement d'ordre des mots dans le 'train dataset' modifie trop l'accuracy")

    def test_property8(self) -> None:
        """
         ajout du ”bruit” dans le ”test dataset”
        """
        testset = self._load_data("test_set.json")['dataset']
        testset = list(map(self._add_email_noise, testset))

        self.test_filename = "test300_noise.json"
        self._save_data(self.test_filename, {"dataset": testset})
        self.new_acc = self._test_from_filenames()
        diff = self.get_diff()
        self.assertLessEqual(diff, self.ERROR_THRESHOLD,
                             "Le changement d'ordre des mots dans le 'test dataset' modifie trop l'accuracy")

    def get_diff(self):
        return abs(self.initial_accuracy - self.new_acc)

    def _save_data(self, filename, data) -> bool:
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=2)
        return True

    def _load_data(self, filename) -> dict:
        with open(filename, "r") as json_data:
            data_dict = json.load(json_data)
        return data_dict

    def _test_from_filenames(
            self
    ) -> float:
        """
        return: l'accuracy pour les données des fichiers fournis en entrée.
        """
        print('Configuration :')
        print('Train:', self.train_filename, ', Test:', self.test_filename)
        # 1. Creation de vocabulaire.
        vocab_filename = "vocabulary.json"
        vocab = VocabularyCreator(self.train_filename, vocab_filename)
        vocab.create_vocab()

        # 2. Classification des emails et initialisation de utilisateurs et groupes.
        renege = RENEGE(self.train_filename)
        if not renege.classify_emails():
            raise RuntimeError('Error classify emails')

        # 3. Evaluation de performance du modele avec la fonction evaluate()
        evaluation = evaluate(self.test_filename)

        return evaluation['accuracy']

    def _shuffle_email_words(self, email) -> dict:
        """
        Modifie l'ordre des mots dans le Subject et le Body d'un email
        """
        email = email['mail']
        subject = email['Subject'].split(' ')
        body = email['Body'].split(' ')
        rd.shuffle(subject)
        rd.shuffle(body)
        return {
            "mail": {
                **email,
                "Subject": ' '.join(subject),
                "Body": ' '.join(body)
            }
        }

    def _add_email_noise(self, email) -> dict:
        """
        Ajoute du bruit dans le Subject et le Body d'un email,
        s'il fait plus de 10 mots.
        """
        email = email['mail']
        subject = self._add_noise(email['Subject'])
        body = self._add_noise(email['Body'])
        return {
            "mail": {
                **email,
                "Subject": subject,
                "Body": body
            }
        }

    def _add_noise(self, sentence: str) -> str:
        sentence_arr = sentence.split(' ')
        sentence_length = len(sentence_arr)
        if sentence_length < self.NOISE_THRESHOLD:
            return sentence
        number_of_words_to_add = int(len(sentence_arr) / self.NOISE_THRESHOLD)  # 1/10 ème
        words = [rd.choice(WORDS) for _ in range(number_of_words_to_add)]
        sentence_arr += words
        return ' '.join(sentence_arr)
