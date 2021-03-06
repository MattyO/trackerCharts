import unittest
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import sys
import os
from os.path import abspath, dirname, join

sys.path.append(abspath(join(dirname(__file__),'../../libs')))

from classes.user import User, UserList, userlist_tojson
from classes.story import Story, StoryList, _days_since_last_updated, _tracker_string_to_time
from helpers.xml import xml_to_dictonary

class UserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setattr(cls, 'old_dir', os.getcwd())
        os.chdir(dirname(__file__))

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.old_dir)

    def test_construct_user(self):
        a_user = User("matt")
        self.assertEqual(a_user.name, "matt")
        self.assertEqual(a_user.wip, 0)


    def test_updateWip(self):
        a_user = User("George")
        story = Story({
            "name":"Some Thigns",
            "id":"2222222",
            "current_state":"",
            "owned_by":"George",
            "updated_at":"2012/09/20 14:10:53 UTC"})

        a_user.updateWip(story)
        self.assertEquals(a_user.wip, 1)

    def test_doesnt_updateWip(self):
        a_user = User("The Shadow")
        story = Story({
            "name":"Some Thigns",
            "id":"2222222",
            "current_state":"",
            "owned_by":"George",
            "updated_at":"2012/09/20 14:10:53 UTC"})

        a_user.updateWip(story)
        self.assertEquals(a_user.wip, 0)

    def test_UserList_tojson_two_stories(self):
        story_list = StoryList([ET.parse("data/project_stories_1"), ET.parse("data/project_stories_2")])
        users = UserList(story_list)

        output = json.loads(userlist_tojson(users))
        self.assertEqual(output[0]['wip'],4)
        self.assertEqual(len(output),1)

    def test_UserList_tojson(self):
        a_user = User("George")
        story_xml = ET.parse("data/story_2").getroot()
        story = Story(xml_to_dictonary(story_xml))
        a_user.updateWip(story)
        user_list = [a_user]

        self.assertEquals(
                    userlist_tojson(user_list),
                    json.dumps([{
                            "name": "George",
                            "current_stories": [{
                                "id": "22222222",
                                "name": "The Rest Of the Things",
                                "updated_at":"2012/09/20 14:10:53 UTC",
                                "days_since_updated":_days_since_last_updated(_tracker_string_to_time(story.updated_at), datetime.today())
                            }], 
                            "wip": 1
                    }], sort_keys=True))

