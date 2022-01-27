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
            0,
            0,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.spam_ham_subject_prob_true = (
            0,
            0,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.spam_ham_body_prob_false = (
            0,
            0,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.spam_ham_subject_prob_false = (
            0,
            0,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.vocab = (
            {}
        )  # vocabulaire avec les valeurs de la probabilité pour mocker "return_value" du "load_dict"
        self.spam_ham_body_prob_expected = 0, 0  # valeurs des probabilités attendues
        self.spam_ham_subject_prob_expected = 0, 0  # valeurs des probabilités attendues

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
        self.assertTrue(emailAnalyzer.is_spam("", ""))
        #pass

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
        self.assertFalse(emailAnalyzer.is_spam("", ""))
        #pass

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_spam_ham_body_prob_Returns_expected_probability(self, mock_load_dict):
        """
        Il faut mocker la fonction "load_dict"
        Il faut vérifier que probabilité est calculée correctement en fonction du "body"
        """
        emailAnalyzer = EmailAnalyzer()
        mock_load_dict.return_value = self.vocab
        p_spam, p_ham = emailAnalyzer.spam_ham_body_prob("")
        print("probability of the body performed correctly : test executed")
        self.assertGreater(p_spam, p_ham)
        
        prob_spam_awaited = 0.5925
        prob_ham_awaited = 0.20375 # la moitié de p_ham 
        
        # Vérification des probabilités 
        self.assertEqual(p_spam, prob_spam_awaited)
        self.assertEqual(p_ham, prob_ham_awaited)
        
        p_spam, p_ham = emailAnalyzer.spam_ham_body_prob("")
        self.assertGreater(p_ham,
                           p_spam)
        #pass

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_subject_spam_ham_prob_Returns_expected_probability(self, mock_load_dict):
        """
        Il faut mocker la fonction "load_dict"
        il faut vérifier que probabilité est calculée correctement en fonction du "sujet"
        """
        emailAnalyzer = EmailAnalyzer()
        mock_load_dict.return_value = self.vocab
        p_spam, p_ham = emailAnalyzer.spam_ham_body_prob("")
        print("probability of the sujet performed correctly : test executed")
        self.assertGreater(p_spam, p_ham)
        #pass

    ###########################################
    #               CUSTOM TEST               #
    ###########################################
    