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
	def __init__(self, states, project_name):
		self.project_name = project_name
		self.states = states
		if self.states is None:
			self.states = []

def burndown_tojson(burndown):
	return json.dumps({"name":burndown.project_name, "states":burndown.states})

def addState(burndown, stories):

	date = strftime('%Y.%m.%d',localtime())
	time = strftime('%H:%M:%S',localtime())
	datetime = date + " " + time 

	state = {"datetime": datetime,"all":{"total":0}} 
	for story in stories:
		if state["all"].has_key(story.current_state) == False:
			state["all"][story.current_state] = 0

		for label in story.labels:
			if not state.has_key(label):
				state[label] = {story.current_state:0}
			elif state[label].has_key(story.current_state) == False:
				state[label][story.current_state] = 0
				state[label]["total"] = 0
			state[label][story.current_state] += 1
			state[label]["total"] += 1
		state["all"][story.current_state] += 1
		state["all"]["total"] += 1

		_normalizeState(state)

	burndown.states.append(state)

	return burndown

def _normalizeState(state):
	for story_states in state["all"].keys():
		for state_label in state.keys():
				if state_label != "datetime" and state[state_label].has_key(story_states) == False:
					state[state_label][story_states] = 0


