import unittest
import xml.etree.ElementTree as ET
import sys
import json
import os
from os.path import abspath, dirname, join

sys.path.append(abspath(join(dirname(__file__),'../../libs')))

import config
from api.localdata import xml_to_dictonary
from classes.story import Story

from classes.burndown import Burndown, addState, _append_burndown_state_datetime, _initial_state, _needs_burndown_label, _needs_burndown_label_state, _add_burndown_label, _add_burndown_label_state, _increment_burndown_label_state, _normalize_burndown_state, burndown_labels, labels_tojson

class BurndownTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		setattr(cls, 'old_dir', os.getcwd())
		os.chdir(dirname(__file__))

	@classmethod
	def tearDownClass(cls):
		os.chdir(cls.old_dir)

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
		story = Story(xml_to_dictonary(story_xml))
		burndown = addState(burndown, [story])
		print burndown.states
		self.assertEqual(len(burndown.states), 1)

	def test_generate_list_labels(self):
		burndown = Burndown("test burndown")
		story_xml = ET.parse("data/story_1").getroot()
		story = Story(xml_to_dictonary(story_xml))
		burndown = addState(burndown, [story])
		burndown = addState(burndown, [story])
		self.assertEqual(burndown_labels(burndown),['all','epic_name']) 
	
	def test_label_list_tojson(self):
		burndown = Burndown("test burndown")
		story_xml = ET.parse("data/story_1").getroot()
		story = Story(xml_to_dictonary(story_xml))
		burndown = addState(burndown, [story])
		labels = burndown_labels(burndown) 
		self.assertEqual(labels_tojson(labels ), json.dumps(['all','epic_name']))

if __name__ == "__main__":
	unittest.main()
