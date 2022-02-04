from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch

class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        self.mails = {"dataset": [ # données pour mocker "return_value" du "load_dict"
            {
                "mail": {
                "Subject": " start shopping at costco today with a complimentary gold membership in your area .",
                "From": "SA_and_HP@paris.com",
                "Date": "2005-06-22",
                "Body":"start shopping at costco today with a free gold membership . we re giving away a limited number of gold memberships in your area .\nkklynsz\n",
                "Spam": "true",
                "File": "enronds//enron2/spam/2128.2005-06-22.SA_and_HP.spam.txt"
                }
            },
            {
                "mail": {
                "Subject": " start date : 12 28 01 ; hourahead hour : 9 ;",
                "From": "williams@paris.com",
                "Date": "2001-12-28",
                "Body":"start date : 12 28 01 ; hourahead hour : 9 ; no ancillary schedules awarded . no variances detected .\nlog messages :\nparsing file - - > > o : portland westdesk california scheduling iso final schedules 2001122809 . tx\n",
                "Spam": "false",
                "File": "enronds//enron4/ham/3821.2001-12-28.williams.ham.txt"
                }
            },
        ]}  
        self.clean_subject_spam = ["spam", "subject", "log"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_spam = ["spam", "body"]  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_ham = ["spam", "subject", "security", "poly"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body_ham = ["body", "body"]  # données pour mocker "return_value" du "clean_text"
        self.vocab_expected = {
            'p_sub_spam':{
                "start": 1/8,
                "shop": 1/8,
                "costco": 1/8,
                "today": 1/8,
                "complimentary": 1/8,
                "gold": 1/8,
                "member": 1/8,
                "area": 1/8
            },
            'p_body_spam':{
                "start": 1/13,
                "shop": 1/13,
                "costco": 1/13,
                "today": 1/13,
                "complimentary": 1/13,
                "gold": 2/13,
                "member": 2/13,
                "area":1/13,
                "give":1/13,
                "limited" :1/13,
                "number":1/13
            },
            'p_sub_ham':{
                "start":1/3,
                "date" :1/3,
                "hour":1/3
            },
            'p_body_ham':{
                "start" : 1/12,
                "date"  : 1/12,
                "hour" : 1/12,
                "schedule" : 2/12,
                "variance": 1/12,
                "detect" : 1/12,
                "message": 1/12,
                "file" : 1/12,
                "portland": 1/12,
                "california":1/12,
                "final": 1/12
            },
            }  # vocabulaire avec les valeurs de la probabilité calculées correctement

    def tearDown(self):
        pass

    # @patch("vocabulary_creator.VocabularyCreator.load_dict")
    # @patch("vocabulary_creator.VocabularyCreator.clean_text")
    # @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    # def test_create_vocab_spam_Returns_vocabulary_with_correct_values(
    #     self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    # ):
    #     """Description: Tester qu'un vocabulaire avec les probabilités calculées
    #     correctement va être retourné. Il faut mocker les fonctions "load dict"
    #      (utiliser self.mails comme une simulation de valeur de retour),"clean text"
    #      (cette fonction va être appelée quelques fois, pour chaque appel on
    #      va simuler une valeur de retour differente, pour cela il faut utiliser
    #      side_effect (voir l'exemple dans l'énonce)) et
    #      "write_data_to_vocab_file" qui va simuler "return True" au lieu
    #      d'écrire au fichier "vocabulary.json".
    #      if faut utiliser self.assertEqual(appel_a_create_vocab(), self.vocab_expected)
    #     """
    #     mock_load_dict.return_value = self.mails
    #     mock_clean_text.side_effect = [ self.clean_subject_spam, self.clean_subject_ham, self.clean_body_spam, self.clean_body_ham ]
    #     mock_write_data_to_vocab_file.return_value = True
    #     vocabulary_creator = VocabularyCreator()
    #     self.assertEqual(vocabulary_creator.create_vocab(), True)
    
    ###########################################
    #               CUSTOM TEST               #
    ###########################################