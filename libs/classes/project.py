import xml.etree.ElementTree as ET

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
