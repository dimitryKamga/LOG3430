import unittest
from main import evaluate
import json
import random
import copy
from text_cleaner import TextCleaning
from vocabulary_creator import VocabularyCreator
from renege import RENEGE


def clean(fileName):
    with open("./dataset/" + fileName + "_set.json") as email_file:
        emails = json.load(email_file)

    textCleaner = TextCleaning()

    for index, e_mail in enumerate(emails["dataset"]):
        emails["dataset"][index]["mail"]["Body"] = ' '.join(textCleaner.clean_text(e_mail["mail"]["Body"]))

    with open("./dataset/" + fileName + "_clean.json", "w") as outfile:
        json.dump(emails, outfile, indent=2)


def shuffle(fileName):
    with open("./dataset/" + fileName + "_set.json") as email_file:
        emails = json.load(email_file)

    for index, e_mail in enumerate(emails["dataset"]):
        bodyMail = e_mail["mail"]["Body"].split(' ')
        # tokenize
        for i in range(9):
            randomIndexOne = random.randint(0, len(bodyMail) - 1)
            randomIndexTwo = random.randint(0, len(bodyMail) - 1)
            temp = bodyMail[randomIndexOne]
            bodyMail[randomIndexOne] = bodyMail[randomIndexTwo]
            bodyMail[randomIndexTwo] = temp

        # detokenize
        emails["dataset"][index]["mail"]["Body"] = ' '.join(bodyMail)

    with open("./dataset/" + fileName + "_shuffle.json", "w") as outfile:
        json.dump(emails, outfile, indent=2)


def triple_emails(fileName):
    with open("./dataset/" + fileName + "_set.json") as email_file:
        emails = json.load(email_file)

    emails_dp = copy.deepcopy(emails)
    emails["dataset"] += emails["dataset"]
    emails["dataset"] += emails_dp["dataset"]

    with open("./dataset/" + fileName + "_3x.json", "w") as outfile:
        json.dump(emails, outfile, indent=2)


def duplicate_words(fileName):
    with open("./dataset/" + fileName + "_set.json") as email_file:
        emails = json.load(email_file)

    for index, e_mail in enumerate(emails["dataset"]):
        body = e_mail["mail"]["Body"]
        # duplicating body
        bodyMail = body + body
        emails["dataset"][index]["mail"]["Body"] = bodyMail

    with open("./dataset/" + fileName + "_words.json", "w") as outfile:
        json.dump(emails, outfile, indent=2)


class TestMain(unittest.TestCase):
    TRAIN_SET = "train_set"
    TEST_SET = "test_set"
    pre_mt_score = 0.96
    post_mt_score = 1.02

    def setUp(self):
        options = ["train", "test"]
        for option in options:
            clean(option)
            shuffle(option)
            triple_emails(option)
            duplicate_words(option)

    def test_clean_emails(self):
        print("\n")
        print("----------test_clean_test_dataset----------")
        vocab = VocabularyCreator(self.TRAIN_SET)
        vocab.create_vocab()
        renege = RENEGE(self.TRAIN_SET)
        renege.classify_emails()

        f1_initial = evaluate(self.TEST_SET)
        f1_final = evaluate("test_clean")
        self.assertTrue(((f1_initial / f1_final) < self.post_mt_score) and ((f1_initial / f1_final) > self.pre_mt_score))

    def test_shuffle(self):
        print("\n")
        print("----------test_shuffle_test_dataset----------")
        vocab = VocabularyCreator(self.TRAIN_SET)
        vocab.create_vocab()
        renege = RENEGE(self.TRAIN_SET)
        renege.classify_emails()

        f1_initial = evaluate(self.TEST_SET)
        f1_final = evaluate("test_shuffle")
        print("F1 initial : " + str(f1_initial))
        print("F1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < self.post_mt_score) and ((f1_initial / f1_final) > self.pre_mt_score))

    def test_triple(self):
        print("\n")
        print("----------test_triple_test_dataset----------")
        vocab = VocabularyCreator(self.TRAIN_SET)
        vocab.create_vocab()
        renege = RENEGE(self.TRAIN_SET)
        renege.classify_emails()

        f1_initial = evaluate(self.TEST_SET)
        f1_final = evaluate("test_300x3")
        self.assertTrue(((f1_initial / f1_final) < self.post_mt_score) and ((f1_initial / f1_final) > self.pre_mt_score))

    def test_words(self):
        print("\n")
        print("----------test_words_test_dataset----------")
        vocab = VocabularyCreator(self.TRAIN_SET)
        vocab.create_vocab()
        renege = RENEGE(self.TRAIN_SET)
        renege.classify_emails()

        f1_initial = evaluate(self.TEST_SET)
        f1_final = evaluate("test_words")

        self.assertTrue(((f1_initial / f1_final) < self.post_mt_score) and ((f1_initial / f1_final) > self.pre_mt_score))

    def test_train_clean_emails(self):
        print("\n")
        print("----------test_clean_train_dataset----------")

        vocab = VocabularyCreator(self.TRAIN_SET)
        vocab.create_vocab()
        renege = RENEGE(self.TRAIN_SET)
        renege.classify_emails()
        f1_initial = evaluate(self.TEST_SET)

        vocab = VocabularyCreator("train_clean")
        vocab.create_vocab()
        renege = RENEGE("train_clean")
        renege.classify_emails()
        f1_final = evaluate(self.TEST_SET)

        self.assertTrue(((f1_initial / f1_final) < self.post_mt_score) and ((f1_initial / f1_final) > self.pre_mt_score))

    def test_train_shuffle(self):
        print("\n")
        print("----------test_shuffle_train_dataset----------")

        vocab = VocabularyCreator(self.TRAIN_SET)
        vocab.create_vocab()
        renege = RENEGE(self.TRAIN_SET)
        renege.classify_emails()
        f1_initial = evaluate(self.TEST_SET)

        vocab = VocabularyCreator("train_shuffle")
        vocab.create_vocab()
        renege = RENEGE("train_shuffle")
        renege.classify_emails()
        f1_final = evaluate(self.TEST_SET)

        self.assertTrue(((f1_initial / f1_final) < self.post_mt_score) and ((f1_initial / f1_final) > self.pre_mt_score))

    def test_train_triple(self):
        print("\n")
        print("----------test_triple_train_dataset----------")

        vocab = VocabularyCreator(self.TRAIN_SET)
        vocab.create_vocab()
        renege = RENEGE(self.TRAIN_SET)
        renege.classify_emails()
        f1_initial = evaluate(self.TEST_SET)

        vocab = VocabularyCreator("train_700x3")
        vocab.create_vocab()
        renege = RENEGE("train_700x3")
        renege.classify_emails()
        f1_final = evaluate(self.TEST_SET)

        self.assertTrue(((f1_initial / f1_final) < self.post_mt_score) and ((f1_initial / f1_final) > self.pre_mt_score))

    def test_train_words(self):
        print("\n")
        print("----------test_word_train_dataset----------")

        vocab = VocabularyCreator(self.TRAIN_SET)
        vocab.create_vocab()
        renege = RENEGE(self.TRAIN_SET)
        renege.classify_emails()
        f1_initial = evaluate(self.TEST_SET)

        vocab = VocabularyCreator("train_words")
        vocab.create_vocab()
        renege = RENEGE("train_words")
        renege.classify_emails()
        f1_final = evaluate(self.TEST_SET)
        self.assertTrue(((f1_initial / f1_final) < self.post_mt_score) and ((f1_initial / f1_final) > self.pre_mt_score))
