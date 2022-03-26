from email.policy import default
from crud import CRUD
import copy
import json
import unittest
from unittest.mock import patch
from datetime import datetime
import itertools


class TestCRUDMaDUM(unittest.TestCase):
    
# utlisation de données similaires à test_crud

    def setUp(self):
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

        self.groups_data = {
             "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
        }
    
    def tearDown(self):
        pass
    
    # Tests MaDUM

    # Tests des rapporteurs
    
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_new_group_id(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        newId = crud.get_new_group_id()

        self.assertEqual(newId, "2")

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_groups_data(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        name = crud.get_groups_data(1, "name")
        trust = crud.get_groups_data(1, "Trust")
        list_members = crud.get_groups_data(1, "List_of_members")

        self.assertEqual(name, "default")
        self.assertEqual(trust, 50)
        self.assertEqual(list_members, ["alex@gmail.com", "mark@mail.com"])

    # Tests des constructeurs 
    
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_init(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()

        self.assertEqual(crud.get_groups_data(1, "name"), "default")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 50)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["alex@gmail.com", "mark@mail.com"])
  
    # Tests des transformateurs
    # Tests des fonctions "add_new_group", "update_groups", "remove_group", "remove_group_member" 
    # 24 combinaisons possibles 
     
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence1(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.update_groups(2, 'Trust', 77)
        crud.remove_group("1")
        crud.remove_group_member(2, "newUser@gmail.com")

        self.assertEqual(crud.get_groups_data(1, "name"), False)
        self.assertEqual(crud.get_groups_data(1, "Trust"), False)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), False)
        self.assertEqual(crud.get_groups_data(2, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(2, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), [])
        
        
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence2(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.update_groups(1, 'Trust', 77)
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.remove_group("1")
        crud.remove_group_member(2, "alex@gmail.com")

        self.assertEqual(crud.get_groups_data(1, "name"), False)
        self.assertEqual(crud.get_groups_data(1, "Trust"), False)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), False)
        self.assertEqual(crud.get_groups_data(2, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(2, "Trust"), 100)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), [])

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence3(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group("1")
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.update_groups(1, 'Trust', 77)
        crud.remove_group_member(1, "alex@gmail.com")

        self.assertEqual(crud.get_groups_data(1, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), [])

    
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence4(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.remove_group("1")
        crud.update_groups(2, 'Trust', 77)
        crud.remove_group_member(2, "alex@gmail.com")

        self.assertEqual(crud.get_groups_data(1, "name"), False)
        self.assertEqual(crud.get_groups_data(1, "Trust"), False)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), False)
        self.assertEqual(crud.get_groups_data(2, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(2, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), [default])

    
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence5(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.update_groups(1, 'Trust', 77)
        crud.remove_group("1")
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.remove_group_member(1, "alex@gmail.com")

        self.assertEqual(crud.get_groups_data(1, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 100)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), [default])

    
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence6(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group("1")
        crud.update_groups(1, 'Trust', 77)
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.remove_group_member(1, "alex@gmail.com")

        self.assertEqual(crud.get_groups_data(1, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 100)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), [default])

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence7(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member(1, "alex@gmail.com")
        crud.update_groups(1, 'Trust', 77)
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.remove_group("1")

        self.assertEqual(crud.get_groups_data(1, "name"), "default")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["mark@mail.com"])
        self.assertEqual(crud.get_groups_data(2, "name"), False)
        self.assertEqual(crud.get_groups_data(2, "Trust"), False)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), False)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence8(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.update_groups(1, 'Trust', 77)
        crud.remove_group_member(1, "alex@gmail.com")
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.remove_group("1")

        self.assertEqual(crud.get_groups_data(1, "name"), "default")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["mark@mail.com"])
        self.assertEqual(crud.get_groups_data(2, "name"), False)
        self.assertEqual(crud.get_groups_data(2, "Trust"), False)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), False)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence9(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.remove_group_member(1, "alex@gmail.com")
        crud.update_groups(1, 'Trust', 77)
        crud.remove_group("1")

        self.assertEqual(crud.get_groups_data(1, "name"), False)
        self.assertEqual(crud.get_groups_data(1, "Trust"), False)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), False)
        self.assertEqual(crud.get_groups_data(2, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(2, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), [])

    
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence10(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member(1, "alex@gmail.com")
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.update_groups(1, 'Trust', 77)
        crud.remove_group("1")

        self.assertEqual(crud.get_groups_data(1, "name"), False)
        self.assertEqual(crud.get_groups_data(1, "Trust"), False)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), False)
        self.assertEqual(crud.get_groups_data(2, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(2, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), ["newUser@gmail.com"])

    
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence11(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.update_groups(1, 'Trust', 77)
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.remove_group_member(1, "alex@gmail.com")
        crud.remove_group("1")

        self.assertEqual(crud.get_groups_data(1, "name"), "default")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["mark@mail.com"])
        self.assertEqual(crud.get_groups_data(2, "name"), False)
        self.assertEqual(crud.get_groups_data(2, "Trust"), False)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), False)

    
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence12(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.update_groups(1, 'Trust', 77)
        crud.remove_group_member(1, "alex@gmail.com")
        crud.remove_group("1")

        self.assertEqual(crud.get_groups_data(1, "name"), "default")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["mark@mail.com"])
        self.assertEqual(crud.get_groups_data(2, "name"), False)
        self.assertEqual(crud.get_groups_data(2, "Trust"), False)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), False)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence13(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group("1")
        crud.update_groups(1, 'Trust', 77)
        crud.remove_group_member(1, "alex@gmail.com")
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])        

        self.assertEqual(crud.get_groups_data(1, "name"), "default")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["mark@mail.com"])
        self.assertEqual(crud.get_groups_data(2, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(2, "Trust"), 100)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), ["newUser@gmail.com"])

    
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence14(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.update_groups(1, 'Trust', 77)
        crud.remove_group("1")
        crud.remove_group_member(1, "alex@gmail.com")
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])        

        self.assertEqual(crud.get_groups_data(1, "name"), "default")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["mark@mail.com"])
        self.assertEqual(crud.get_groups_data(2, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(2, "Trust"), 100)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), ["newUser@gmail.com"])

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence15(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.remove_group("1")
        crud.remove_group_member(1, "alex@gmail.com")
        crud.update_groups(1, 'Trust', 77)

        self.assertEqual(crud.get_groups_data(1, "name"), False)
        self.assertEqual(crud.get_groups_data(1, "Trust"), False)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), False)
        self.assertEqual(crud.get_groups_data(2, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(2, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), [])

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence16(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group("1")
        crud.add_new_group('test_add_group', 100, ["newUser@gmail.com"])
        crud.remove_group_member(1, "alex@gmail.com")
        crud.update_groups(1, 'Trust', 77)

        self.assertEqual(crud.get_groups_data(1, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), [])

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence17(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member(1, "alex@gmail.com")
        crud.add_new_group('test_add_group', 100, ["alex@gmail.com", "john@gmail.com"])
        crud.remove_group("1")
        crud.update_groups(1, 'Trust', 77)

        self.assertEqual(crud.get_groups_data(1, "name"), False)
        self.assertEqual(crud.get_groups_data(1, "Trust"), False)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), False)
        self.assertEqual(crud.get_groups_data(2, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(2, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), ["alex@gmail.com", "john@gmail.com"])

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence18(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.add_new_group('test_add_group', 100, ["alex@gmail.com", "john@gmail.com"])
        crud.remove_group_member(1, "alex@gmail.com")
        crud.remove_group(0)
        crud.update_groups(1, 'Trust', 77)

        self.assertEqual(crud.get_groups_data(1, "name"), False)
        self.assertEqual(crud.get_groups_data(1, "Trust"), False)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), False)
        self.assertEqual(crud.get_groups_data(2, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(2, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(2, "List_of_members"), ["john@gmail.com"])

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence19(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group("1")
        crud.remove_group_member(1, "alex@gmail.com")
        crud.add_new_group('test_add_group', 100, ["alex@gmail.com", "john@gmail.com"])
        crud.update_groups(1, 'Trust', 77)

        self.assertEqual(crud.get_groups_data(1, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["alex@gmail.com", "john@gmail.com"])

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence20(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member(1, "alex@gmail.com")
        crud.remove_group("1")
        crud.add_new_group('test_add_group', 100, ["alex@gmail.com", "john@gmail.com"])
        crud.update_groups(1, 'Trust', 77)

        self.assertEqual(crud.get_groups_data(1, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 77)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["alex@gmail.com", "john@gmail.com"])
        
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence21(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member(1, "alex@gmail.com")
        crud.remove_group("1")
        crud.update_groups(1, 'Trust', 77)
        crud.add_new_group('test_add_group', 100, ["alex@gmail.com", "john@gmail.com"])

        self.assertEqual(crud.get_groups_data(1, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 100)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["alex@gmail.com", "john@gmail.com"])

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence22(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group("1")
        crud.remove_group_member(1, "alex@gmail.com")
        crud.update_groups(1, 'Trust', 77)
        crud.add_new_group('test_add_group', 100, ["alex@gmail.com", "john@gmail.com"])

        self.assertEqual(crud.get_groups_data(1, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 100)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["alex@gmail.com", "john@gmail.com"])

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence23(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.update_groups(1, 'Trust', 77)
        crud.remove_group_member(1, "alex@gmail.com")
        crud.remove_group("1")
        crud.add_new_group('test_add_group', 100, ["alex@gmail.com", "john@gmail.com"])

        self.assertEqual(crud.get_groups_data(1, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 100)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["alex@gmail.com", "john@gmail.com"])

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_sequence24(self, mock_read_groups_file, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_group_member(1, "alex@gmail.com")
        crud.update_groups(1, 'Trust', 77)
        crud.remove_group("1")
        crud.add_new_group('test_add_group', 100, ["alex@gmail.com", "john@gmail.com"])

        self.assertEqual(crud.get_groups_data(1, "name"), "test_add_group")
        self.assertEqual(crud.get_groups_data(1, "Trust"), 100)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["alex@gmail.com", "john@gmail.com"])
    
