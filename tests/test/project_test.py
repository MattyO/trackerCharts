import unittest
import xml.etree.ElementTree as ET
import sys
import os
from os.path import abspath, dirname, join

sys.path.append(abspath(join(dirname(__file__),'../../libs')))

from classes.project import Project, ProjectList,  find_project,  filter_on_ids,   list_private_ids, reduce_list

from classes.story import Story
from helpers.xml import xml_to_dictonary 
import config

class ProjectTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setattr(cls, 'old_dir', os.getcwd())
        os.chdir(dirname(__file__))

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.old_dir)

    def test_construct_project(self):
        project_xml = ET.parse("data/project_1").getroot()
        test_project = Project(xml_to_dictonary(project_xml))

        self.assertEqual(test_project.name, "Test Project")

class ProjectListTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setattr(cls, 'old_dir', os.getcwd())
        os.chdir(dirname(__file__))

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.old_dir)

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

        self.assertEquals(
                reduce_list(private_ids, [222222,111111]), 
                [333333, 444444])

