import sys
from os import getcwd 
sys.path.append(getcwd() + "/libs")

from flask import Flask, render_template

from api import tracker
from api import localdata

from classes.project import Project, ProjectList, Burndown, addState, burndown_tojson
from classes.story import Story, StoryList 
from classes.user import  User, UserList, userlist_tojson

app = Flask(__name__)
app.debug = True

@app.route("/")
def overview():
	projects = ProjectList(tracker.getProjects())
	return render_template('index.html', projects=projects)

@app.route("/<int:tracker_id>")
def project(project_id):
	return "project burndowns go here"

@app.route("/<int:project_id>/burndown.json")
def projects_json(project_id):
	project_id = str(project_id)
	return burndown_tojson(Burndown(localdata.getBurndownStates(project_id), project_id))
	
@app.route("/wip.json")
def wip_json():
	project_list = ProjectList(localdata.getProjectsXML())
	project_ids = map(lambda project: project.id, project_list)
	stories_xml_list = []
	app.logger.debug(project_ids)
	for id in project_ids :
		stories_xml_list.append(localdata.getStoriesXML(id))

	stories = StoryList(stories_xml_list)
	users = UserList(stories)

	return userlist_tojson(users)


@app.route("/wip")
def wip(type=None):

	project_list = ProjectList(localdata.getProjectsXML())
	project_ids = map(lambda project: project.id, project_list)
	stories_xml_list = []
	app.logger.debug(project_ids)
	for id in project_ids :
		stories_xml_list.append(localdata.getStoriesXML(id))

	stories = StoryList(stories_xml_list)
	users = UserList(stories)

	return render_template('wip.html', projects=project_list , users=users)
	


@app.route("/config/")
def config():
	pass

@app.route("/update")
def update():

	localdata.saveProjectsXML(tracker.getProjects())
	project_list = ProjectList(localdata.getProjectsXML())

	for project in project_list:
		test_stories = tracker.getStories(project.id)
		localdata.saveStoriesXML(test_stories, str(project.id))

	for project in project_list:
		burndown = Burndown(localdata.getBurndownStates(project.id), project.id)
		test_stories = StoryList([localdata.getStoriesXML(project.id)])
		burndown = addState(burndown, test_stories)
		localdata.saveBurndownStates(burndown.states, project.id)

	return "updated"


if __name__ == "__main__":
	print "running flask"
	app.run(port=4567, host='0.0.0.0') 
