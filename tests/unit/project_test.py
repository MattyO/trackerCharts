import unittest
import xml.etree.ElementTree as ET

import sys
sys.path.append("../../libs")

from classes.project import Project, ProjectList, Burndown, addState, _append_burndown_state_datetime, _initial_state, _needs_burndown_label, _needs_burndown_label_state, _add_burndown_label, _add_burndown_label_state, _increment_burndown_label_state, find_project, _normalize_burndown_state, filter_on_ids, burndown_labels, labels_tojson, list_private_ids, reduce_list

from classes.story import Story
import config
import json

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
		
		self.assertEqual(len(project_list), 3)
		self.assertEqual(project_list[0].name, "Test Project")
		self.assertEqual(project_list[1].name, "Test Project 2")
	
	def test_find_project(self):
		project_list_xml = ET.parse("data/projects").getroot()
		project_list = ProjectList(project_list_xml)

		project_found = find_project(project_list, '666666')
		self.assertEqual(project_found.id, '666666')

	def test_cant_find_project(self):
		project_list_xml = ET.parse("data/projects").getroot()
		project_list = ProjectList(project_list_xml)
		project_found = find_project(project_list,'999999')
		self.assertEqual(project_found, None)

	def test_filter_on_ids(self):
		project_list_xml = ET.parse("data/projects").getroot()
		project_list = ProjectList(project_list_xml)
		project_list = filter_on_ids(project_list, [666666])
		self.assertEqual(len(project_list), 2)

	def test_construct_private_id_list(self):
		project_list_xml = ET.parse("data/projects").getroot()
		project_list = ProjectList(project_list_xml)
		project_ids = list_private_ids(project_list)
		self.assertEquals(project_ids,[222222, 333333])

	
	def test_filter_on_viability(self):
		project_list_xml = ET.parse("data/projects").getroot()
		project_list = ProjectList(project_list_xml)
		private_ids = list_private_ids(project_list)
		project_list = filter_on_ids(project_list, private_ids)
		self.assertEqual(len(project_list), 1)

	def test_reduce_list(self):
		private_ids = [222222, 333333, 444444]
		self.assertEquals(reduce_list(private_ids, [222222,111111]), [333333, 444444])

class BurndownTest(unittest.TestCase):

	def test_create_class(self):
		burndown = Burndown("test burndown")
		self.assertEqual(burndown.states, [])
		self.assertEqual(burndown.project_name, "test burndown")
		self.assertEqual(burndown.possible_states, ["unscheduled","unstarted", "started","finished", "delivered", "accepted"])

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
	
	def test_normalize_burndown_state(self):
		state = {"all":{"total":1, "unscheduled":1}, "epic_name":{"total":1, "unscheduled":1}}
		print config.states("tracker")
		state = _normalize_burndown_state(state, config.states("tracker")) 
		self.assertEqual(state, {"all":{"total":1, "unscheduled":1, "unstarted":0, "accepted":0, "started":0,"finished":0, "delivered":0}, "epic_name":{"total":1, "unscheduled":1, "unstarted":0, "accepted":0, "delivered":0, "started":0, "finished":0}})


	def test_add_state(self):
		burndown = Burndown("test burndown")
		story_xml = ET.parse("data/story_1").getroot()
		story = Story(story_xml)
		burndown = addState(burndown, [story])
		print burndown.states
		self.assertEqual(len(burndown.states), 1)

	def test_generate_list_labels(self):
		burndown = Burndown("test burndown")
		story_xml = ET.parse("data/story_1").getroot()
		story = Story(story_xml)
		burndown = addState(burndown, [story])
		burndown = addState(burndown, [story])
		self.assertEqual(burndown_labels(burndown),['all','epic_name']) 
	
	def test_label_list_tojson(self):
		burndown = Burndown("test burndown")
		story_xml = ET.parse("data/story_1").getroot()
		story = Story(story_xml)
		burndown = addState(burndown, [story])
		labels = burndown_labels(burndown) 
		self.assertEqual(labels_tojson(labels ), json.dumps(['all','epic_name']))

if __name__ == "__main__":
	unittest.main()
