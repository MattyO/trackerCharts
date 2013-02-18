import unittest
import xml.etree.ElementTree as ET
import sys
import os

from datetime import datetime
from os.path import abspath, dirname, join

sys.path.append(abspath(join(dirname(__file__),'../../libs')))

from classes.project import Project
from classes.story import Story, StoryList, keep_by_ids, exclude_by_ids, story_ids_for_project, _days_since_last_updated, _tracker_string_to_time, _prettify_days, add_project_name, add_project_names
from api.localdata import xml_to_dictonary

class StoryTest(unittest.TestCase):
    #setup and tear down classes needed to run test from any directory
    #and still find files in /test/data directory
    @classmethod
    def setUpClass(cls):
        setattr(cls, 'old_dir', os.getcwd())
        os.chdir(dirname(__file__))

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.old_dir)

    def test_story_construct_from_xml(self):
        story_xml = ET.parse("data/story_1").getroot()
        story_dict = xml_to_dictonary(story_xml)
        print story_dict

        story = Story(story_dict)
        self.assertEqual(story.name, "All The Things")

    def test_story_has_label(self):
        story_xml = ET.parse("data/story_1").getroot()
        story_dict = xml_to_dictonary(story_xml)

        story = Story(story_dict)

        self.assertEqual(story.labels, ["epic_name"])


    def test_prettyify_days_less_than_month(self):
        self.assertEqual(_prettify_days("3"), "3 days")

    def test_prettyify_days_more_than_month(self):
        self.assertEqual(_prettify_days("33"), "1 months")

    def test_prettyify_days_show_half_months(self):
        self.assertEqual(_prettify_days("48"), "1 and a half months")

    def test_add_project_name_None(self):
        story = Story( xml_to_dictonary(ET.parse("data/story_1").getroot()))
        project_list = [Project(xml_to_dictonary(ET.parse("data/project_1").getroot()))]

        new_story = add_project_name(story, project_list)

        self.assertEqual(new_story.project_name, "NA")

    def test_add_project_name_with_name(self):
        story = Story(xml_to_dictonary(ET.parse("data/story_3").getroot()))
        project_list = [Project(xml_to_dictonary(ET.parse("data/project_1").getroot()))]

        new_story = add_project_name(story, project_list)

        self.assertEqual(new_story.project_name, "Test Project")

    def test_add_project_names(self):
        story_dict = xml_to_dictonary(ET.parse("data/story_3").getroot())
        story_list = [Story(story_dict)]
        project_list = [Project(xml_to_dictonary(ET.parse("data/project_1").getroot()))]

        new_story_list = add_project_names(story_list, project_list)

        self.assertEqual(new_story_list[0].project_name, "Test Project")


    def test_story_owned_by_is_None(self):
        story_xml = ET.parse("data/story_1").getroot()
        story_dict = xml_to_dictonary(story_xml)
        print story_dict
        story = Story(story_dict)
        self.assertEqual(story.owned_by, None)

    def test_story_owned_by_is_set(self):
        story_xml = ET.parse("data/story_2").getroot()
        story_dict = xml_to_dictonary(story_xml)
        story = Story(story_dict)
        self.assertEqual(story.owned_by, "George")

    def test_story_has_days_since_last_updated(self):
        story_xml = ET.parse("data/story_2").getroot()
        story_dict = xml_to_dictonary(story_xml)
        story = Story(story_dict)
        self.assertEqual(
                        story.days_since_last_updated, 
                        _days_since_last_updated(_tracker_string_to_time(story.updated_at),datetime.today())
                        )



class StoryListTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setattr(cls, 'old_dir', os.getcwd())
        os.chdir(dirname(__file__))

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.old_dir)


    def test_construct_story_list(self):
        story_list_xml = [ET.parse("data/project_stories_1").getroot(), ET.parse("data/project_stories_2").getroot()]
        story_list = StoryList(story_list_xml)
        self.assertEqual(len(story_list), 8)
        self.assertEqual(story_list[0].name, "Test Story 1")

    def test_exclude_by_ids(self):
        story_list_xml = [ET.parse("data/project_stories_1").getroot(), ET.parse("data/project_stories_2").getroot()]
        story_list = StoryList(story_list_xml)

        reducted_story_list = exclude_by_ids(story_list, ['22222222'])
        self.assertEqual(len(reducted_story_list), 7)

    def test_keep_by_ids(self):
        story_list_xml = [ET.parse("data/project_stories_1").getroot(), ET.parse("data/project_stories_2").getroot()]
        story_list = StoryList(story_list_xml)

        reducted_story_list = keep_by_ids(story_list, ['22222222'])
        self.assertEqual(len(reducted_story_list), 1)
        self.assertEqual(reducted_story_list[0].id, '22222222')

    def test_id_for_in_progress(self):
        story_list_xml = [ET.parse("data/project_stories_1").getroot(), ET.parse("data/project_stories_2").getroot()]
        story_list = StoryList(story_list_xml)
        story_id_list = story_ids_for_project(story_list, '111111')
        self.assertEqual(len(story_id_list), 4)

    def test_days_since_last_updated(self):
        self.assertEqual(
                        _days_since_last_updated(datetime(2012, 1, 12), datetime(2012, 2, 14)), 
                        33)

    def test_tracker_string_to_time(self):
        self.assertEqual(
                _tracker_string_to_time("2012/09/20 14:10:53 UTC"),
                datetime(2012, 9, 20, 14, 10, 53))

