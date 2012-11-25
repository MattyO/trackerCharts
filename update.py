import sys
from os import getcwd 
sys.path.append(getcwd() + "/libs")

from api import tracker
from api import localdata

from classes.project import Project, ProjectList, Burndown, addState, burndown_tojson, projectlist_tojson, find_project
from classes.story import Story, StoryList 
from classes.user import  User, UserList, userlist_tojson
import config

localdata.saveProjectsXML(tracker.getProjects())
project_list = ProjectList(localdata.getProjectsXML())

for project in project_list:
	test_stories = tracker.getStories(project.id)
	localdata.saveStoriesXML(test_stories, str(project.id))

for project in project_list:
	burndown = Burndown(project.id, localdata.getBurndownStates(project.id))
	test_stories = StoryList([localdata.getStoriesXML(project.id)])
	burndown = addState(burndown, test_stories)
	localdata.saveBurndownStates(burndown.states, project.id)
