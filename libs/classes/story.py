import sys
import os
from os.path import abspath, dirname, join
from datetime import datetime

sys.path.append(abspath(join(dirname(__file__),'../../libs')))

from classes.project import Project
from helpers.xml import xml_to_dictonary, convert_elements

DAYS_IN_A_MONTH = 30

def _days_since_last_updated(first_date, second_date):
    return (second_date - first_date).days

def _prettify_days(num_days):
    pretty_string = ""

    if int(num_days) > DAYS_IN_A_MONTH:
        months, days = divmod(int(num_days), DAYS_IN_A_MONTH) 
        pretty_string += str(months)
        if days > 15: 
            pretty_string += " and a half"
        pretty_string += " months"

    else:
        pretty_string = str(num_days) + " days"

    return pretty_string

def _tracker_string_to_time(tracker_time):
    return datetime.strptime(tracker_time, "%Y/%m/%d %H:%M:%S UTC")

def prettify_stories(stories):
    for story in stories:
        story_days = story.days_since_last_updated
        story.days_since_last_updated = _prettify_days(story_days)

    return stories

def add_project_name(story, projects):
    name_found = "NA" 

    projects_found = filter(lambda project: project.id == story.project_id, projects)

    if len(projects_found) == 1:
        name_found = projects_found[0].name

    setattr(story, "project_name", name_found)

    return story

def add_project_names(stories, projects):
    return map(lambda story: add_project_name(story, projects),stories)

def _set_default(dictonary, key, default_value):
    if dictonary.has_key(key) is False:
        dictonary[key] = default_value
    return dictonary

def _split_labels(story_attributes):
    if story_attributes.has_key("labels"):
        print story_attributes['labels']
        story_attributes['labels'] = story_attributes['labels'].split(",")

    return story_attributes

class Story:
    def __init__(self, attrs):
        updated_at = _tracker_string_to_time(attrs['updated_at'])
        last_updated = _days_since_last_updated( updated_at, datetime.today())
        attrs = _split_labels(attrs)

        attrs = _set_default(attrs , 'labels', [])
        attrs = _set_default(attrs , 'owned_by', None)
        attrs = _set_default(attrs , 'days_since_last_updated', last_updated )

        self.__dict__ = attrs

def is_in_progress(story):
    #filtered_states = ["accepted", "delivered", "finished"]
    return story.owned_by != None and story.current_state == 'started' 


def StoryList(story_xml_list):

    converter = lambda proj_xml: Story(xml_to_dictonary(proj_xml))
    nested_story_list = map(lambda stories_xml: convert_elements(converter, stories_xml, 'story'), story_xml_list)

    #fastest way to flatten array of arrays
    story_list = [story for stories in nested_story_list for story in stories]

    return story_list

def keep_by_ids(storylist, id_list):
    return filter(lambda story: story.id in id_list, storylist)

def exclude_by_ids(storylist, id_list):
    return filter(lambda story: story.id not in id_list, storylist)

def ids_for_in_progress(storylist):
    return [ story.id for story in storylist if is_in_progress(story)]

def story_ids_for_project(storylist, project_id):
    return [ story.id for story in storylist if story.project_id == project_id ]

