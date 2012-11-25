import sys, os
from os.path import abspath, dirname, join
sys.path.append(abspath(join(dirname(__file__),'libs')))

from flask import Flask, render_template, redirect, url_for, make_response

from api import tracker
from api import localdata

from classes.project import Project, ProjectList, Burndown, addState, burndown_tojson, projectlist_tojson, find_project
from classes.story import Story, StoryList 
from classes.user import  User, UserList, userlist_tojson
import config

app = Flask(__name__)
app.debug = True

@app.route("/")
def overview():
	projects = ProjectList(tracker.getProjects())
	return render_template('index.html', projects=projects)

@app.route("/<int:project_id>")
def project(project_id):
	project_list = ProjectList(localdata.getProjectsXML())
	project_found = find_project(project_list, str(project_id))
	if project_found == None:
		return redirect(url_for('overview'))
	return render_template("project.html", project=project_found )

@app.route("/<int:project_id>/burndown.json")
def project_json(project_id):
	project_id = str(project_id)
	return burndown_tojson(Burndown(project_id,localdata.getBurndownStates(project_id)))
	
@app.route("/projects.json")
def projects_json():
	project_list = ProjectList(localdata.getProjectsXML())
	response = make_response(projectlist_tojson(project_list))
	response.mimetype="application/json"
	return response

@app.route("/possible_states/<project_type>.json")
def get_states(project_type):
	response = make_response(config.states_tojson(config.states(project_type)))
	response.mimetype = "application/json"
	return response

@app.route("/wip.json")
def wip_json():
	project_list = ProjectList(localdata.getProjectsXML())
	project_ids = map(lambda project: project.id, project_list)
	stories_xml_list = []
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
def config_page():
	pass

if __name__ == "__main__":
	print "running flask"
	app.run(port=4567, host='0.0.0.0') 
