import unittest
import xml.etree.ElementTree as ET

import sys
sys.path.append("../../libs")

from classes.project import Project, ProjectList 

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


if __name__ == "__main__":
	unittest.main()
