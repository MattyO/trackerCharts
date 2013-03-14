import unittest
import xml.etree.ElementTree as ET
import sys
import os

from datetime import datetime
from os.path import abspath, dirname, join

sys.path.append(abspath(join(dirname(__file__),'../../libs')))

from classes.project import Project
from classes.story import Story, StoryList, keep_by_ids, exclude_by_ids, story_ids_for_project, _days_since_last_updated, _tracker_string_to_time, _prettify_days, add_project_name, add_project_names
from helpers.xml import xml_to_dictonary

class StoryTest(unittest.TestCase):

    def test_story_construct_from_xml(self):
        xml_string = '''
        <story> 
            <name>All The Things</name>
            <id>3333333</id>
            <updated_at>2012/09/20 14:10:53 UTC</updated_at>
            <extra>this is extra</extra>
        </story>
        '''
        story_xml = ET.fromstring(xml_string)
        story_dict = xml_to_dictonary(story_xml)

        story = Story(story_dict)
        self.assertEqual(story.name, "All The Things")

    def test_story_has_default_label_attr(self):
        story = Story({
            "name":"Some Thigns",
            "id":"2222222",
            "updated_at":"2012/09/20 14:10:53 UTC"})

        self.assertEqual(story.labels, [])

    def test_story_has_label(self):
        story = Story({
            "name":"Some Thigns",
            "id":"2222222",
            "updated_at":"2012/09/20 14:10:53 UTC",
            "labels":"epic_name"})

        self.assertEqual(story.labels, ["epic_name"])


    def test_prettyify_days_less_than_month(self):
        self.assertEqual(_prettify_days("3"), "3 days")

    def test_prettyify_days_more_than_month(self):
        self.assertEqual(_prettify_days("33"), "1 months")

    def test_prettyify_days_show_half_months(self):
        self.assertEqual(_prettify_days("48"), "1 and a half months")

    def test_add_project_name_None(self):
        story = Story({
            "name":"Some Thigns",
            "project_id":"111111",
            "id":"2222222",
            "updated_at":"2012/09/20 14:10:53 UTC",
            "labels":"epic_name"})

        project_list = [
                Project({"id":"222222", "name":"Test Project"})]

        new_story = add_project_name(story, project_list)

        self.assertEqual(new_story.project_name, "NA")

    def test_add_project_name_with_name(self):
        story = Story({
            "name":"Some Thigns",
            "project_id":"111111",
            "id":"2222222",
            "updated_at":"2012/09/20 14:10:53 UTC"})

        project_list = [
                Project({"id":"111111", "name":"Test Project"})]

        new_story = add_project_name(story, project_list)

        self.assertEqual(new_story.project_name, "Test Project")

    def test_add_project_names(self):
        story = Story({
            "name":"Some Thigns",
            "project_id":"111111",
            "id":"2222222",
            "updated_at":"2012/09/20 14:10:53 UTC"})
        story_list = [story]

        project_list = [
                Project({"id":"111111", "name":"Test Project"})]

        new_story_list = add_project_names(story_list, project_list)

        self.assertEqual(new_story_list[0].project_name, "Test Project")


    def test_story_owned_by_is_None(self):
        story = Story({
            "name":"Some Thigns",
            "id":"2222222",
            "updated_at":"2012/09/20 14:10:53 UTC"})

        self.assertEqual(story.owned_by, None)

    def test_story_owned_by_is_set(self):
        story = Story({
            "name":"Some Thigns",
            "owned_by":"George",
            "id":"2222222",
            "updated_at":"2012/09/20 14:10:53 UTC"})

        self.assertEqual(story.owned_by, "George")

    def test_story_has_days_since_last_updated(self):
        story = Story({
            "name":"Some Thigns",
            "owned_by":"George",
            "id":"2222222",
            "updated_at":"2012/09/20 14:10:53 UTC"})

        should_return = _days_since_last_updated(
                            _tracker_string_to_time(story.updated_at),
                            datetime.today())

        self.assertEqual(
                story.days_since_last_updated, 
                should_return)



class StoryListTest(unittest.TestCase):

    def test_construct_story_list(self):
        project_1_stories ='''
        <stories>
            <story>
                <name>Test Story 1</name>
                <id>3333333</id>
                <updated_at>2012/09/20 14:10:53 UTC</updated_at>
                <extra>this is extra</extra>
            </story>
            <story>
                <name>All The Rest of the Things</name>
                <id>4444444</id>
                <updated_at>2012/09/20 14:10:53 UTC</updated_at>
                <extra>this is extra</extra>
            </story>
            <story>
                <name>Some things we forgot</name>
                <id>5555555</id>
                <updated_at>2012/09/20 14:10:53 UTC</updated_at>
                <extra>this is extra</extra>
            </story>
        </stories>
        '''
        project_2_stories = '''
        <stories> 
            <story>
                <name>Some things we forgot</name>
                <id>6666666</id>
                <updated_at>2012/09/20 14:10:53 UTC</updated_at>
                <extra>this is extra</extra>
            </story>
        </stories>
        '''

        story_list_xml = [
                ET.fromstring(project_1_stories),
                ET.fromstring(project_2_stories)]

        story_list = StoryList(story_list_xml)
        self.assertEqual(len(story_list), 4)
        self.assertEqual(story_list[0].name, "Test Story 1")

    def test_exclude_by_ids(self):
        story_list = [ 
                Story({"id":"3333333", "name":"Test Story 1","project_id":"111111","updated_at":"2012/09/20 14:10:53 UTC"}),
                Story({"id":"4444444", "name":"All The Rest of the Things","project_id":"4444444","updated_at":"2012/09/20 14:10:53 UTC"}) ]

        reducted_story_list = exclude_by_ids(story_list, ['4444444'])

        self.assertEqual(len(reducted_story_list), 1)
        self.assertEqual(reducted_story_list[0].id, '3333333')


    def test_keep_by_ids(self):
        story_list = [ 
                Story({"id":"3333333", "name":"Test Story 1","project_id":"111111","updated_at":"2012/09/20 14:10:53 UTC"}),
                Story({"id":"4444444", "name":"All The Rest of the Things","project_id":"4444444","updated_at":"2012/09/20 14:10:53 UTC"}) ]

        reducted_story_list = keep_by_ids(story_list, ['3333333'])

        self.assertEqual(len(reducted_story_list), 1)
        self.assertEqual(reducted_story_list[0].id, '3333333')

    def test_id_for_projects(self):
        story_list = [ 
                Story({"id":"3333333", "name":"Test Story 1","project_id":"111111","updated_at":"2012/09/20 14:10:53 UTC"}),
                Story({"id":"5555555", "name":"All The Rest of the Things","project_id":"4444444","updated_at":"2012/09/20 14:10:53 UTC"}) ]

        story_id_list = story_ids_for_project(story_list, '111111')

        self.assertEqual(len(story_id_list), 1)
        self.assertEqual(story_id_list[0], '3333333')

    def test_days_since_last_updated(self):
        self.assertEqual(
                        _days_since_last_updated(datetime(2012, 1, 12), datetime(2012, 2, 14)), 
                        33)

    def test_tracker_string_to_time(self):
        self.assertEqual(
                _tracker_string_to_time("2012/09/20 14:10:53 UTC"),
                datetime(2012, 9, 20, 14, 10, 53))

