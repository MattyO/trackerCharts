import xml.etree.ElementTree as ET
import yaml

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
	
def addState(burndown, stories):
	state = {"all":{}} 

	for story in stories:
		if state["all"].has_key(story.current_state) == False:
			state["all"][story.current_state] = 0

		for label in story.labels:
			if not state.has_key(label):
				state[label] = {story.current_state:0}
			elif state[label].has_key(story.current_state) == False:
				state[label][story.current_state] = 0
			state[label][story.current_state] += 1
		state["all"][story.current_state] += 1

		for story_states in state["all"].keys():
			for state_label in state.keys():
					if state[state_label].has_key(story_states) == False:
						state[state_label][story_states] = 0

	burndown.states.append(state)

	return burndown

