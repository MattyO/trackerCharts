import sys
from os import getcwd 
sys.path.append(getcwd() + "/libs")

from flask import Flask, render_template

from api import tracker
from api import localdata

from classes.project import Project, ProjectList, Burndown, addState
from classes.story import Story, StoryList 

app = Flask(__name__)
app.debug = True

@app.route("/")
def overview():
	projects = ProjectList(tracker.getProjects())
	return render_template('index.html', projects=projects)

@app.route("/<int:tracker_id>")
def project(project_id):
	pass


@app.route("/wip")
def wip(type=None):

	project_list = ProjectList(tracker.getProjects())
	product_ids = map(lambda id: project.id, project_list)
	stories = StoryList(tracker.getStories(product_ids))
	users = UserList(stories)

	return render_template('wip.html', projects=projects)
	


@app.route("/burndown/<int:tracker_id>.json")
def burndown(tracker_id, type=None):
	pass

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
