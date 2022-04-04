import unittest
from unittest.mock import patch
from main import evaluate
from vocabulary_creator import VocabularyCreator
from renege import RENEGE



class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.prepareVocab(self,"train700.json")
        self.initialAccuracyTest=evaluate("test300.json")

    def prepareVocab(self,trainFile):
            # 1. Creation de vocabulaire.
            vocab = VocabularyCreator()
            vocab.create_vocab(trainFile)
            # 2. Classification des emails et initialisation de utilisateurs et groupes.
            renege = RENEGE(trainFile)
            renege.classify_emails()

    def test_shuffled_words_train_set(self):
        print("----------test_shuffled_words_train_set----------")
        self.prepareVocab("train_shuffle.json")
        accuracy=evaluate("test300.json")
        self.assertLessEqual(abs(self.initialAccuracyTest-accuracy),0.03)

    def test_shuffled_words_test_set(self):
        print("----------test_shuffled_words_test_set----------")
        self.prepareVocab("train700.json")
        accuracy=evaluate("test_shuffle.json")
        self.assertLessEqual(abs(self.initialAccuracyTest-accuracy),0.03)

    def test_emails_x3_train_set(self):
        print("----------test_emails_x3_train_set----------")
        self.prepareVocab("train700x3.json")
        accuracy=evaluate("test300.json")
        self.assertLessEqual(abs(self.initialAccuracyTest-accuracy),0.03)

    def test_emails_x3_test_set(self):
        print("----------test_emails_x3_test_set----------")
        self.prepareVocab("train700.json")
        accuracy=evaluate("test300x3.json")
        self.assertLessEqual(abs(self.initialAccuracyTest-accuracy),0.03)



    








