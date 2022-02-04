import copy
from datetime import datetime
import unittest
from unittest.mock import patch

from crud import CRUD


class TestCRUD(unittest.TestCase):
    def setUp(self):
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_users_file
        self.users_data = {
            "1": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "SpamN": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }
        }
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_groups_file
        self.groups_data = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

    def tearDown(self):
        pass

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_add_new_user_Passes_correct_data_to_modify_users_file(
            self, mock_modify_users_file, mock_modify_groups_file, mock_read_users_file
    ):
        """Description: il faut utiliser les mocks des fonctions "read_users_file",
        "modify_users_file" pour tester que l'information a ajouter pour l'utilisateur a été formée correctement
        par la fonction, e.g. self.modify_users_file(data) -> "data" doit avoir un format et contenu expecté
        il faut utiliser ".assert_called_once_with(expected_data)"

        Note: Ce test a deja ete complete pour vous
        """

        # Ici on mock pour que read_users_file retourne la liste d'utilisateurs
        mock_read_users_file.return_value = self.users_data

        # Les informations du nouvel utilisateur
        new_user_data = {
            "name": "james@gmail.com",
            "Trust": 50,
            "SpamN": 0,
            "HamN": 0,
            "Date_of_first_seen_message": 1596844800.0,
            "Date_of_last_seen_message": 1596844800.0,
            "Groups": ["default"],
        }

        # On effectue une copie de la liste d'utilisateurs
        users_data_final = {}
        users_data_final["1"] = self.users_data["1"]
        users_data_final["2"] = self.users_data["2"]
        # On ajoute les infos du nouvel utilisateur
        users_data_final["0"] = new_user_data

        crud = CRUD()
        crud.add_new_user("james@gmail.com", "2020-08-08")
        # On vérifie que quand on ajoute un nouvel utilisateur, modify_users_file est appelée avec la nouvelle liste mise à jour
        mock_modify_users_file.assert_called_once_with(users_data_final)

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_add_new_group_Passes_correct_data_to_modify_groups_file(
            self, mock_modify_groups_file, mock_read_groups_file):
        """Description: il faut utiliser les mocks des fonctions "read_groups_file",
        "modify_groups_file" (ou selon votre realisation) pour tester que
        l'information a ajouter pour le groupe a été formée correctement par la fonction e.g.
        self.modify_groups_file(data) -> "data" doit avoir un format et contenu attendu
        il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_read_groups_file.return_value = self.groups_data

        expected_group_data = {
            "name": "test",
            "Trust": "00",
            "List_of_members": [],
        }

        group_data_final = {}
        group_data_final["1"] = self.groups_data["1"]
        group_data_final["2"] = self.groups_data["2"]
        # On ajoute les infos du nouveau groupe
        group_data_final["0"] = expected_group_data

        crud_ = CRUD()
        crud_.add_new_group("test", "00", [])
        mock_modify_groups_file.assert_called_once_with(group_data_final)

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_id(self, mock_read_users_file):
        """Description: il faut utiliser le mock de fonction "read_users_file",
        (ou selon votre realisation) pour tester que false (ou bien une exception)
        est retourne par la fonction si ID non-existant est utilisé
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """
        mock_read_users_file.return_value = self.users_data

        crud_ = CRUD()
        self.assertFalse(crud_.get_user_data(-1, "Trust"))

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_field(self, mock_read_users_file):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que false (ou bien une exception)
        est retourne par la fonction si champ non-existant est utilisé
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """
        mock_read_users_file.return_value = self.users_data

        crud_ = CRUD()
        self.assertFalse(crud_.get_user_data(1, "Trost"))

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_correct_value_if_field_and_id_are_valid(
            self, mock_read_users_file
    ):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que une bonne valeur est fournie
        si champ et id valide sont utilises
        il faut utiliser ".assertEqual()""
        """
        mock_read_users_file.return_value = self.users_data

        crud_ = CRUD()
        self.assertEqual(crud_.get_user_data(1, "Trust"), 100)

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_id(self, mock_read_groups_file):
        """
        Similaire au test_get_user_data_Returns_false_for_invalid_id mais pour un groupe
        """
        mock_read_groups_file.return_value = self.groups_data

        crud_ = CRUD()
        self.assertFalse(crud_.get_groups_data(-1, "Trust"))

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_field(
            self, mock_read_groups_file
    ):
        """
        Similaire au test_get_user_data_Returns_false_for_invalid_field mais pour un groupe
        """
        mock_read_groups_file.return_value = self.groups_data

        crud_ = CRUD()
        self.assertFalse(crud_.get_groups_data(1, "Trost"))

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_correct_value_if_field_and_id_are_valid(
            self, mock_read_groups_file
    ):
        """
        Similaire au test_get_user_data_Returns_correct_value_if_field_and_id_are_valid mais pour un groupe
        """
        mock_read_groups_file.return_value = self.groups_data

        crud_ = CRUD()
        self.assertEqual(crud_.get_groups_data(1, "Trust"), 50)

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_false_for_invalid_user_name(
            self, mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        crud_ = CRUD()
        self.assertFalse(crud_.get_user_id("00@gmail.com"))

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_id_for_valid_user_name(self, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        crud_ = CRUD()
        self.assertEqual(crud_.get_user_id("alex@gmail.com"), '1')

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_false_for_invalid_group_name(
            self, mock_read_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        crud_ = CRUD()
        self.assertFalse(crud_.get_group_id("doofault"))

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_id_for_valid_group_name(self, mock_read_groups_file):
        mock_read_groups_file.return_value = self.groups_data
        crud_ = CRUD()
        self.assertEqual(crud_.get_group_id("default"), '1')

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    # Modify_user_file mock est inutile pour tester False pour update
    def test_update_users_Returns_false_for_invalid_id(
            self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """
        mock_read_users_file.return_value = self.users_data

        crud_ = CRUD()
        self.assertFalse(crud_.update_users(-1, "data", "data"))
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_for_invalid_field(
            self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """
        mock_read_users_file.return_value = self.users_data

        crud_ = CRUD()
        self.assertFalse(crud_.update_users(1, "field", "data"))
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_data_to_modify_users_file(
            self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_read_users_file.return_value = self.users_data
        user_data_final = copy.deepcopy(self.users_data)
        user_data_final["1"]["name"] = "test@gmail.com"

        crud_ = CRUD()
        self.assertFalse(crud_.update_users(1,"name","/*885"))
        crud_.update_users(1, "name", "test@gmail.com")
        mock_modify_users_file.assert_called_once_with(user_data_final)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_id(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """
        mock_read_groups_file.return_value = self.groups_data

        crud_ = CRUD()
        self.assertFalse(crud_.update_groups(-1, "field", "data"))
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_field(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """
        mock_read_groups_file.return_value = self.groups_data

        crud_ = CRUD()
        self.assertFalse(crud_.update_groups(1, "dofault", "test"))
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Passes_correct_data_to_modify_groups_file(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_read_groups_file.return_value = self.groups_data
        expected_data = copy.deepcopy(self.groups_data)
        expected_data["1"]["name"] = "test"

        crud_ = CRUD()
        self.assertFalse(crud_.update_groups(1,"name",""))

        crud_.update_groups(1, "name", "test")
        mock_modify_groups_file.assert_called_once_with(expected_data)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_Returns_false_for_invalid_id(
            self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud_ = CRUD()
        self.assertFalse(crud_.remove_user(9))
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_Passes_correct_value_to_modify_users_file(
            self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        expected_data = {"1": self.users_data["1"]}
        crud_ = CRUD()
        crud_.remove_user(2)
        mock_modify_users_file.assert_called_once_with(expected_data)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Returns_false_for_invalid_id(
            self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud_ = CRUD()
        self.assertFalse(crud_.remove_user_group(9, "default"))
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Returns_false_for_invalid_group(
            self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud_ = CRUD()
        self.assertEqual(crud_.remove_user_group(1, "dofault"), False)
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Passes_correct_value_to_modify_users_file(
            self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        group_data_final = copy.deepcopy(self.users_data)
        group_data_final["1"]["Groups"].remove("default")

        crud_ = CRUD()
        crud_.remove_user_group("1", "default")
        mock_modify_users_file.assert_called_once_with(group_data_final)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_Returns_false_for_invalid_id(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        crud_ = CRUD()
        self.assertFalse(crud_.remove_group(-1))
        mock_modify_groups_file.assert_not_called();

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_Passes_correct_value_to_modify_groups_file(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        group_data_final = copy.deepcopy(self.groups_data)
        group_data_final.pop("1")

        crud_ = CRUD()
        crud_.remove_group("1")
        mock_modify_groups_file.assert_called_once_with(group_data_final)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_member_Returns_false_for_invalid_id(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        crud_ = CRUD()
        self.assertFalse(crud_.remove_group_member(-1, "test@gmail.com"))
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_member_Returns_false_for_invalid_group_member(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        crud_ = CRUD()
        self.assertFalse(crud_.remove_group_member(0, "dofault"))
        mock_modify_groups_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_member_Passes_correct_value_to_modify_groups_file(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        group_data_final = copy.deepcopy(self.groups_data)
        group_data_final["1"]["List_of_members"] = ["mark@mail.com"]

        crud_ = CRUD()
        crud_.remove_group_member("1", "alex@gmail.com")
        mock_modify_groups_file.assert_called_once_with(group_data_final)

    ###########################################
    #               CUSTOM TEST               #
    ###########################################

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_add_new_user_return_false_on_email_unicity_and_format(
        self,mock_read_groups_file,mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value= self.groups_data

        crud_ = CRUD()
        crud_.users_lookup = ["test@gmail.com"]
        self.assertFalse(crud_.add_new_user("test@gmail.com","2022-02-03"))
        self.assertFalse(crud_.add_new_user("testgmail.com","2022-02-03"))

    @patch("crud.CRUD.read_users_file")
    def test_get_new_user_id_when_adding_correct_user(
        self,mock_read_users_file):
        mock_read_users_file.return_value = self.users_data

        crud_ = CRUD()
        crud_.add_new_user("user3@gmail.fr","2022-02-03")
        self.assertEqual(crud_.get_new_user_id(),'3')

    @patch("crud.CRUD.read_groups_file")
    def test_get_new_group_id_when_adding_correct_group(
        self,mock_read_groups_file):
        mock_read_groups_file.return_value= self.groups_data

        crud_ = CRUD()
        crud_.add_new_group("group3",90,[])
        self.assertEqual(crud_.get_new_group_id(),'3')


    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_add_new_group_fail_name_in_groups_lookup(
        self,mock_read_groups_file,mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data

        crud_ = CRUD()
        crud_.users_lookup = ['memberOne']
        crud_.groups_lookup = ["test@gmail.com"]
        self.assertFalse(crud_.add_new_group("test",100,[""]))
        self.assertFalse(crud_.add_new_group("test",100,['memberOne', 'memberTwo']))

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.get_user_id")
    def test_add_new_group_Passes_correct_values(
        self,mock_get_user_id,mock_read_groups_file,mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value= self.groups_data

        mock_get_user_id.return_value = "1"

        crud_ = CRUD()
        crud_.users_data = copy.deepcopy(self.users_data)
        crud_.users_lookup = ["alex@gmail.com"]
        crud_.add_new_group("group3",100,["alex@gmail.com"])
        self.assertTrue("group3" in crud_.users_data["1"]["Groups"])



    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_and_invalid_is_Date_of_last_seen_message_data_to_modify_users_file_when_field(
            self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        user_data_final = copy.deepcopy(self.users_data)
        date = datetime.utcfromtimestamp(1598918400.0)
        user_data_final["1"]["Date_of_last_seen_message"] = 1598918400.0

        crud_ = CRUD()
        self.assertFalse(crud_.update_users(1,"Date_of_last_seen_message", date.strftime('2020-07-08')))
        crud_.update_users(1, "Date_of_last_seen_message", date.strftime('%Y-%m-%d'))
        mock_modify_users_file.assert_called_once_with(user_data_final)


    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_and_invalid_is_Date_of_first_seen_message_data_to_modify_users_file_when_field(
            self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        user_data_final = copy.deepcopy(self.users_data)
        date = datetime.utcfromtimestamp(1596844800.0)
        user_data_final["1"]["Date_of_first_seen_message"] = 1596844800.0

        crud_ = CRUD()
        self.assertFalse(crud_.update_users(1,"Date_of_first_seen_message", date.strftime('2022-07-08')))
        crud_.update_users(1, "Date_of_first_seen_message", date.strftime('%Y-%m-%d'))
        mock_modify_users_file.assert_called_once_with(user_data_final)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_and_invalid_Trust_data_to_modify_users(
        self, mock_read_users_file, mock_modify_users_file
    ):

        mock_read_users_file.return_value = self.users_data
        expected_data = copy.deepcopy(self.users_data)
        expected_data["1"]["Trust"] = 100

        crud_ = CRUD()
        self.assertFalse(crud_.update_users(1,"Trust",-1))
        crud_.update_users(1, "Trust", 100)
        mock_modify_users_file.assert_called_once_with(expected_data)


    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_and_invalid_SpamN_data_to_modify_users(
        self, mock_read_users_file, mock_modify_users_file
    ):

        mock_read_users_file.return_value = self.users_data
        expected_data = copy.deepcopy(self.users_data)
        expected_data["1"]["SpamN"] = 100

        crud_ = CRUD()
        self.assertFalse(crud_.update_users(1,"SpamN",-1))
        crud_.update_users(1, "SpamN", 100)
        mock_modify_users_file.assert_called_once_with(expected_data)


    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_Groups_modify_user_file(
        self, mock_read_users_file, mock_modify_users_file, mock_read_groups_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data

        crud_ = CRUD()
        crud_.update_users(1, "Groups", ["default"])
        mock_modify_users_file.assert_called_once()

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_return_False_on_invalid_user_Groups(
        self, mock_read_users_file, mock_modify_users_file, mock_read_groups_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data

        crud_ = CRUD()
        self.assertFalse(crud_.update_users(1, "Groups", "test"))
        mock_modify_users_file.assert_not_called()

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Passes_correct_and_invalid_field_Trust_data_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        expected_data = copy.deepcopy(self.groups_data)
        expected_data["1"]["Trust"] = 100

        crud_ = CRUD()
        self.assertFalse(crud_.update_groups(1, "Trust", -1))
        crud_.update_groups(1, "Trust", 100)
        mock_modify_groups_file.assert_called_once_with(expected_data)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_update_groups_Passes_correct_on_invalid_List_of_members(
        self,
        mock_read_users_file,
        mock_read_groups_file,
        mock_modify_groups_file,
    ):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data

        crud_ = CRUD()
        self.assertEqual(crud_.update_groups(1, "List_of_members", ["test"]), False)
        mock_modify_groups_file.assert_called_once()