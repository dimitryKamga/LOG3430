import json

from email_analyzer import EmailAnalyzer

import unittest
from unittest.mock import patch


class TestEmailAnalyzer(unittest.TestCase):
    def setUp(self):
        self.subject = ""
        self.body = ""
        self.clean_subject = []  # données pour mocker "return_value" du "clean_text"
        self.clean_body = []  # données pour mocker "return_value" du "clean_text"
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
        self.vocab = (
            {
                "p_sub_spam":{
                    "spam_sub": 1,
                },
                "p_sub_ham":{
                    "ham_sub": 1,
                },
                "p_body_spam":{
                    "spam_body": 1,
                },
                "p_body_ham":{
                    "ham_body" : 1,
                }
            }
        )  # vocabulaire avec les valeurs de la probabilité pour mocker "return_value" du "load_dict"
        self.spam_ham_body_prob_expected_spam = 0.5925, 0.20375  # valeurs des probabilités attendues
        self.spam_ham_subject_prob_expected_spam = 0.5925, 0.20375      # valeurs des probabilités attendues
        self.spam_ham_body_prob_expected_ham = 0.29625, 0.4075  # valeurs des probabilités attendues
        self.spam_ham_subject_prob_expected_ham = 0.29625, 0.4075  # valeurs des probabilités attendues

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
        emailAnalyzer = EmailAnalyzer()
        mock_spam_ham_body_prob.return_value = self.spam_ham_body_prob_true  
        mock_spam_ham_subject_prob.return_value = self.spam_ham_body_prob_true
        print("If spam > ham -> true : test executed")
        self.assertTrue(emailAnalyzer.is_spam(self.subject, self.body))
        
    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_subject_prob")
    def test_is_spam_Returns_False_if_spam_prob_is_lower(
        self, mock_spam_ham_subject_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être False si probabilité spam < probabilité ham
        """
        emailAnalyzer = EmailAnalyzer()
        mock_spam_ham_body_prob.return_value = self.spam_ham_body_prob_false 
        mock_spam_ham_subject_prob.return_value = self.spam_ham_body_prob_false
        print("If spam < ham -> false : test executed")
        self.assertFalse(emailAnalyzer.is_spam(self.subject, self.body))

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_spam_ham_body_prob_Returns_expected_probability(self, mock_load_dict):
        """
        Il faut mocker la fonction "load_dict"
        Il faut vérifier que probabilité est calculée correctement en fonction du "body"
        """
        emailAnalyzer = EmailAnalyzer()
        mock_load_dict.return_value = self.vocab
        print("probability of the body performed correctly (spam) : test executed")
        self.assertEqual(emailAnalyzer.spam_ham_body_prob(["spam_body"]), self.spam_ham_body_prob_expected_spam) 

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_subject_spam_ham_prob_Returns_expected_probability(self, mock_load_dict):
        """
        Il faut mocker la fonction "load_dict"
        il faut vérifier que probabilité est calculée correctement en fonction du "sujet"
        """
        emailAnalyzer = EmailAnalyzer()
        mock_load_dict.return_value = self.vocab
        print("probability of the sujet performed correctly (spam) : test executed")
        self.assertEqual(emailAnalyzer.spam_ham_subject_prob(["spam_sub"]), self.spam_ham_subject_prob_expected_spam)

    ###########################################
    #               CUSTOM TEST               #
    ###########################################
    
    """
    Il est nécessaire de tester 2 cas supplémentaires pour avoir un coverage maximum.
    Il faut vérifier que la probabilité est correctement calculé em fonction du "sujet" et du "body" pour le cas ham 
    """
    
    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_spam_ham_body_prob_Returns_expected_probability_ham(self, mock_load_dict):
        emailAnalyzer = EmailAnalyzer()
        mock_load_dict.return_value = self.vocab
        print("probability of the body performed correctly (ham) : test executed")
        self.assertEqual(emailAnalyzer.spam_ham_body_prob(["ham_body"]), self.spam_ham_body_prob_expected_ham) 

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_subject_spam_ham_prob_Returns_expected_probability_ham(self, mock_load_dict):
        emailAnalyzer = EmailAnalyzer()
        mock_load_dict.return_value = self.vocab
        print("probability of the sujet performed correctly (ham) : test executed")
        self.assertEqual(emailAnalyzer.spam_ham_subject_prob(["ham_sub"]), self.spam_ham_subject_prob_expected_ham)
    