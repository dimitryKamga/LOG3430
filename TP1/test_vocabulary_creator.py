from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch


class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        self.mails = {
            "dataset": [
                {
                    "mail": {
                        "Subject": " la uncle rummie s hangover pills ! absolutely new ! naeyc",
                        "From": "GP@paris.com",
                        "Date": "2004-08-15",
                        "Body": "a recent survey shows that it takes an average of just 3",
                        "Spam": "true",
                        "File": "enronds//enron4/spam/2030.2004-08-15.GP.spam.txt"
                    }

                },
                {
                    "mail": {
                        "Subject": " enrononline launch monday 18 th .",
                        "From": "farmer@paris.com",
                        "Date": "2000-09-15",
                        "Body": "we are pleased to announce that as of monday sept",
                        "Spam": "false",
                        "File": "enronds//enron1/ham/2256.2000-09-15.farmer.ham.txt"
                    }

                },
            ]
        }  # données pour mocker "return_value" du "load_dict"
        self.clean_subject_spam = [
            "la", "uncle", "rummie", "s", "hangover", "pills", "absolutely", "new", "naeyc", "uncle"
        ]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_spam = [
            "a", "recent", "survey", "shows", "that", "it", "takes", "an", "average", "of", "just", "recent"
        ]  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_ham = [
            "enrononline", "launch", "monday", "monday"
        ]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_ham = [
            "we", "are", "pleased", "to", "announce", "that", "as", "of", "monday", "sept", "we"
        ]  # données pour mocker "return_value" du "clean_text"
        self.vocab_expected = {
            'p_sub_spam':
                {'uncl': 0.14285714285714285,
                 'rummi': 0.14285714285714285,
                 'hangov': 0.14285714285714285,
                 'pill': 0.14285714285714285,
                 'absolut': 0.14285714285714285,
                 'new': 0.14285714285714285,
                 'naeyc': 0.14285714285714285},
            'p_sub_ham':
                {'enrononlin': 0.3333333333333333,
                 'launch': 0.3333333333333333,
                 'monday': 0.3333333333333333},
            'p_body_spam':
                {'recent': 0.2,
                 'survey': 0.2,
                 'show': 0.2,
                 'take': 0.2,
                 'averag': 0.2},
            'p_body_ham':
                {'pleas': 0.25,
                 'announc': 0.25,
                 'monday': 0.25,
                 'sept': 0.25}
        }

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
         (utiliser self.mails comme une simulation de valeur de retour),"clean text"
         (cette fonction va être appelée quelques fois, pour chaque appel on
         va simuler une valeur de retour differente, pour cela il faut utiliser
         side_effect (voir l'exemple dans l'énonce)) et
         "write_data_to_vocab_file" qui va simuler "return True" au lieu
         d'écrire au fichier "vocabulary.json".
         if faut utiliser self.assertEqual(appel_a_create_vocab(), self.vocab_expected)
        """
        mock_load_dict.return_value = self.mails
        mock_write_data_to_vocab_file.return_value = True

        mock_clean_text.side_effect = [self.clean_body_ham, self.clean_subject_ham, self.clean_body_spam,
                                       self.clean_subject_spam]
        vc_ = VocabularyCreator()
        self.assertEqual(vc_.create_vocab(), True)
        self.assertEqual(vc_.voc_data, self.vocab_expected)

    ###########################################
    #               CUSTOM TEST               #
    ###########################################
