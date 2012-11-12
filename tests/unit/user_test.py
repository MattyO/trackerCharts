import unittest
import xml.etree.ElementTree as ET
import sys
sys.path.append("../../libs")
from classes.user import User, UserList
from classes.story import Story

class UserTest(unittest.TestCase):
	def test_construct_user(self):
		a_user = User("matt")
		self.assertEqual(a_user.name, "matt")
		self.assertEqual(a_user.wip, 0)


	def test_updateWip(self):
		a_user = User("Eric Hankinson")
		story_xml = ET.parse("data/story_2").getroot()
		story = Story(story_xml)

		a_user.updateWip(story)
		self.assertEquals(a_user.wip, 1)

	def test_doesnt_updateWip(self):
		a_user = User("Eric Hankinson")
		story_xml = ET.parse("data/story_1").getroot()
		story = Story(story_xml)

		a_user.updateWip(story)
		self.assertEquals(a_user.wip, 0)

	def test_doesnt_updateWip_wrong_user(self):
		a_user = User("matt")
		story_xml = ET.parse("data/story_1").getroot()
		story = Story(story_xml)

		a_user.updateWip(story)
		self.assertEquals(a_user.wip, 0)

