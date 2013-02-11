import unittest
import xml.etree.ElementTree as ET
import sys
import os

from datetime import datetime
from os.path import abspath, dirname, join

sys.path.append(abspath(join(dirname(__file__),'../../libs')))

from classes.story import Story, StoryList, keep_by_ids, exclude_by_ids, story_ids_for_project, _days_since_last_updated, _tracker_string_to_time

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
		story = Story(story_xml)
		self.assertEqual(story.name, "All The Things")

	def test_story_owned_by_is_None(self):
		story_xml = ET.parse("data/story_1").getroot()
		story = Story(story_xml)
		self.assertEqual(story.owned_by, None)

	def test_story_owned_by_is_set(self):
		story_xml = ET.parse("data/story_2").getroot()
		story = Story(story_xml)
		self.assertEqual(story.owned_by, "George")

	def test_story_has_days_since_last_updated(self):
		story_xml = ET.parse("data/story_2").getroot()
		story = Story(story_xml)
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

