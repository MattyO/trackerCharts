import xml.etree.ElementTree as ET
import yaml
import json
from time import strftime, localtime 

class Project:
	def __init__(self, xml):
		attrs = dict()
		for child in xml:
			if len(child.findall('.//*')) == 0:
				attrs[child.tag] = child.text
		self.__dict__ = attrs


def ProjectList(project_xml):
	projects = [] 

	for project in project_xml.findall('project'):
		projects.append(Project(project))

	return projects

class Burndown:
	def __init__(self, project_name, states=[]):
		self.project_name = project_name
		self.states = states
		if self.states is None:
			self.states = []

def burndown_tojson(burndown):
	return json.dumps({"name":burndown.project_name, "states":burndown.states})

def addState(burndown, stories):

	burndown_state = {"all":_initial_state()}
	for story in stories:

		for label in story.labels:
			if _needs_burndown_label(burndown_state , label):
				burndown_state = _add_burndown_label(burndown_state, label)

			if _needs_burndown_label_state(burndown_state, label, story.current_state):
				burndown_state = _add_burndown_label_state(burndown_state, label, story.current_state)
			if _needs_burndown_label_state(burndown_state, "all", story.current_state):
				burndown_state = _add_burndown_label_state(burndown_state, "all", story.current_state)

			burndown_state = _increment_burndown_label_state(burndown_state , label, story.current_state)
			burndown_state = _increment_burndown_label_state(burndown_state , label, "total")
			burndown_state = _increment_burndown_label_state(burndown_state , "all", story.current_state)
			burndown_state = _increment_burndown_label_state(burndown_state , "all", "total")

	_normalize_burndown_state(burndown_state)

	burndown_state = _append_burndown_state_datetime(burndown_state)

	burndown = append_burndown_state(burndown, burndown_state)

	return burndown

def append_burndown_state(burndown, burndown_state):
	if burndown.states == []:
		burndown.states  = burndown_state
	else:
		burndown.states.append(burndown_state)

	return burndown

def _initial_state():
	return {"total":0}

def _increment_burndown_label_state(burndown_state, label, story_state):
	burndown_state[label][story_state] += 1
	return burndown_state

def _needs_burndown_label(burndown_state, label):
	return not burndown_state.has_key(label)

def _add_burndown_label(burndown_state, label):
	burndown_state[label] = _initial_state()
	return burndown_state

def _needs_burndown_label_state(burndown_state, label, story_state):
	return not burndown_state[label].has_key(story_state)

def _add_burndown_label_state(burndown_state, label, story_state):
	burndown_state[label][story_state] = 0
	return burndown_state

def _append_burndown_state_datetime(state):
	date = strftime('%Y.%m.%d',localtime())
	time = strftime('%H:%M:%S',localtime())
	state["datetime"] = date + " " + time 
	return state

def _normalize_burndown_state(state):
	for story_states in state["all"].keys():
		for state_label in state.keys():
				if state_label != "datetime" and state[state_label].has_key(story_states) == False:
					state[state_label][story_states] = 0


