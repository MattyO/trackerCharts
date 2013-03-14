import unittest
import xml.etree.ElementTree as ET
import sys
import os
from os.path import abspath, dirname, join

sys.path.append(abspath(join(dirname(__file__),'../../libs')))

from classes.project import Project, ProjectList,  find_project,  filter_on_ids,   list_private_ids, reduce_list, remove_private_projects, list_ids

from classes.story import Story
from helpers.xml import xml_to_dictonary 
import config

class ProjectTest(unittest.TestCase):

    def test_construct_project(self):
        xml_string = '''
        <project>
            <id> 1111111 </id>
            <name>Test Project</name>
            <public> false </public>
            <desciption>There are way more elements than this </desciption>
        </project>

        '''
        project_xml = ET.fromstring(xml_string)
        test_project = Project(xml_to_dictonary(project_xml))

        self.assertEqual(test_project.name, "Test Project")

    def test_remove_private_projects(self):
        my_project_ids=[2222222]
        project_list = [
            Project({"id":"1111111", "public":"false", "name":"Project 1"}),
            Project({"id":"2222222", "public":"false", "name":"Project 2"}),
            Project({"id":"3333333", "public":"true", "name":"Project 3"})]

        public_projects = remove_private_projects(project_list, my_project_ids)

        self.assertEqual(len(public_projects), 2)
        self.assertEqual(public_projects[0].name, "Project 2")
        self.assertEqual(public_projects[1].name, "Project 3")

class ProjectListTest(unittest.TestCase):

    def test_construct_project_list(self):
        xml_projects = '''
        <projects> 
            <project>
                <id> 1111111 </id>
                <name>Test Project</name>
                <public> false </public>
                <desciption>There are way more elements than this </desciption>
            </project>
            <project>
                <id> 2222222 </id>
                <name>Test Project 2</name>
                <public> false </public>
                <desciption>There are way more elements than this </desciption>
            </project>
            <project>
                <id> 3333333 </id>
                <name>Test Project again</name>
                <public> false </public>
                <desciption>There are way more elements than this </desciption>
            </project>
        </projects>
        '''
        project_list_xml = ET.fromstring(xml_projects)
        project_list = ProjectList(project_list_xml)

        self.assertEqual(len(project_list), 3)
        self.assertEqual(project_list[0].name, "Test Project")
        self.assertEqual(project_list[1].name, "Test Project 2")

    def test_find_project(self):
        project_list = [
                Project({"id": "111111", "public": "true", "name":"Test Project 1"}),
                Project({"id": "222222", "public": "false", "name":"Test Project 2"}),
                Project({"id": "666666", "public": "false", "name":"Test Project 3"})]

        project_found = find_project(project_list, '666666')

        self.assertEqual(project_found.id, '666666')
        self.assertEqual(project_found.name, 'Test Project 3')

    def test_cant_find_project(self):
        project_list = [
                Project({"id": "111111", "public": "true", "name":"Test Project 1"}),
                Project({"id": "222222", "public": "false", "name":"Test Project 2"}),
                Project({"id": "666666", "public": "false", "name":"Test Project 3"})]

        project_found = find_project(project_list,'999999')

        self.assertEqual(project_found, None)

    def test_filter_on_ids(self):
        project_list = [
                Project({"id": "111111", "public": "true", "name":"Test Project 1"}),
                Project({"id": "222222", "public": "false", "name":"Test Project 2"}),
                Project({"id": "666666", "public": "false", "name":"Test Project 3"})]

        project_list = filter_on_ids(project_list, [666666])

        self.assertEqual(len(project_list), 2)
        self.assertEqual(project_list[0].id, '111111')
        self.assertEqual(project_list[1].id, '222222')

    def test_list_ids(self):
        project_list = [
                Project({"id": "111111", "public": "true", "name":"Test Project 1"}),
                Project({"id": "222222", "public": "false", "name":"Test Project 2"}),
                Project({"id": "333333", "public": "false", "name":"Test Project 3"})]
        ids = list_ids(project_list)
        self.assertEqual(ids,[ 111111, 222222, 333333])
        

    def test_construct_private_id_list(self):
        project_list = [
                Project({"id": "111111", "public": "true", "name":"Test Project 1"}),
                Project({"id": "222222", "public": "false", "name":"Test Project 2"}),
                Project({"id": "333333", "public": "false", "name":"Test Project 3"})]

        project_ids = list_private_ids(project_list)

        self.assertEquals(project_ids,[222222, 333333])

    def test_filter_on_viability(self):
        project_list = [
                Project({"id": "111111", "public": "true", "name":"Test Project 1"}),
                Project({"id": "222222", "public": "false", "name":"Test Project 2"}),
                Project({"id": "333333", "public": "false", "name":"Test Project 3"})]

        private_ids = list_private_ids(project_list)
        project_list = filter_on_ids(project_list, private_ids)

        self.assertEqual(len(project_list), 1)

    def test_reduce_list(self):
        private_ids = [222222, 333333, 444444]

        self.assertEquals(
                reduce_list(private_ids, [222222,111111]), 
                [333333, 444444])

