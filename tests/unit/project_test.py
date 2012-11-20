import unittest
import xml.etree.ElementTree as ET

import sys
sys.path.append("../../libs")

from classes.project import Project, ProjectList, Burndown, addState, _append_burndown_state_datetime, _initial_state, _needs_burndown_label, _needs_burndown_label_state, _add_burndown_label, _add_burndown_label_state, _increment_burndown_label_state

from classes.story import Story

class ProjectTest(unittest.TestCase):
	def test_construct_project(self):
		project_xml = ET.parse("data/project_1").getroot()
		print project_xml
		test_project = Project(project_xml)
		self.assertEqual(test_project.name, "Test Project")
	
class ProjectListTest(unittest.TestCase):

	def test_construct_project_list(self):
		project_list_xml = ET.parse("data/projects").getroot()
		project_list = ProjectList(project_list_xml)
		
		self.assertEqual(len(project_list), 2)
		self.assertEqual(project_list[0].name, "Test Project")
		self.assertEqual(project_list[1].name, "Test Project 2")

class BurndownTest(unittest.TestCase):

	def test_create_class(self):
		burndown = Burndown("test burndown")
		self.assertEqual(burndown.states, [])
		self.assertEqual(burndown.project_name, "test burndown")

	def test_needs_burndown_label(self):
		state = {"all":_initial_state()}
		self.assertTrue(_needs_burndown_label(state, "epic_name"))
		state["epic_name"] = {"all":_initial_state()}
		self.assertFalse(_needs_burndown_label(state, "epic_name"))

	def test_needs_burndown_label_state(self):
		state = {"all":_initial_state()}
		self.assertTrue(_needs_burndown_label_state(state, "all", "unscheduled"))
		state["all"]["unscheduled"] = 1
		self.assertFalse(_needs_burndown_label_state(state, "all", "unscheduled"))

	def test_add_burndown_label(self):
		state = {"all":_initial_state()}
		self.assertFalse(state.has_key("epic_name"))
		state = _add_burndown_label(state, "epic_name")
		self.assertTrue(state.has_key("epic_name"))
	
	def test_add_burndown_label_state(self):
		state = {"all":_initial_state()}
		self.assertFalse(state["all"].has_key("unscheduled"))
		state = _add_burndown_label_state(state,"all", "unscheduled")
		self.assertTrue(state["all"].has_key("unscheduled"))
	
	def test_increment_burndown_state(self):
		state = {"all":_initial_state(), "epic_name":{"total":0, "unscheduled":0}}
		_increment_burndown_label_state(state, "epic_name", "unscheduled")
		self.assertEqual(state, {"all":_initial_state(), "epic_name":{"total":0, "unscheduled":1}})

	def test_append_date_time(self):
		state = {"all":_initial_state()} 
		state = _append_burndown_state_datetime(state)
		self.assertIn("datetime", state)

	def test_add_state(self):
		burndown = Burndown("test burndown")
		story_xml = ET.parse("data/story_1").getroot()
		story = Story(story_xml)
		burndown = addState(burndown, [story])
		print burndown.states
		self.assertEqual(len(burndown.states), 3)

if __name__ == "__main__":
	unittest.main()
