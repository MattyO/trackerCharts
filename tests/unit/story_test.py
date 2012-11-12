import unittest
import xml.etree.ElementTree as ET
import sys
sys.path.append("../../libs")
from classes.story import Story, StoryList


class StoryTest(unittest.TestCase):

	def test_story_construct(self):
		story_xml = ET.parse("data/story_1").getroot()
		story = Story(story_xml)
		self.assertEqual(story.name, "Test Story 1")

	def test_story_owned_by_is_None(self):
		story_xml = ET.parse("data/story_1").getroot()
		story = Story(story_xml)
		self.assertEqual(story.owned_by, None)

	def test_story_owned_by_is_set(self):
		story_xml = ET.parse("data/story_2").getroot()
		story = Story(story_xml)
		self.assertEqual(story.owned_by, "Eric Hankinson")

class StoryListTest(unittest.TestCase):

	def test_construct_story_list(self):
		story_list_xml = [ET.parse("data/project_stories_1").getroot(), ET.parse("data/project_stories_2").getroot()]
		story_list = StoryList(story_list_xml)
		self.assertEqual(len(story_list), 6)
		self.assertEqual(story_list[0].name, "Test Story 1")


