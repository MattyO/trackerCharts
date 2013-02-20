import sys
import os
from os.path import abspath, dirname, join

sys.path.append(abspath(join(dirname(__file__),'libs')))

from flask import Flask, render_template, redirect, url_for, make_response, session, request

from api import tracker
from api import localdata
from api import flask_helper
from api.localdata import listify

from classes.project import Project, ProjectList, projectlist_tojson, find_project, filter_on_ids,  list_private_ids, reduce_list, list_ids, remove_private_projects
from classes.burndown import Burndown, addState, burndown_tojson, burndown_labels, labels_tojson
from classes.story import Story, StoryList, keep_by_ids, ids_for_in_progress,story_ids_for_project, prettify_stories, add_project_names
from classes.user import  User, UserList, userlist_tojson

import config

app = Flask(__name__)
app.debug = config.debug
app.secret_key = config.secret_key

def _get_filtered_projects():
    projects = ProjectList(localdata.getProjectsXML())
    current_user = flask_helper.safe_session('user_id')

    user_projects = listify(localdata.get_cached_data(current_user))

    projects = remove_private_projects(projects, user_projects)
    projects = filter_on_ids(projects,  config.ignore)

    return remove_private_projects(projects, user_projects)


def _stories_for(project_ids):
    story_xml_list = [localdata.getStoriesXML(str(id)) for id in project_ids]
    stories = StoryList(story_xml_list)

    return stories

@app.route("/")
def overview():
    current_user = flask_helper.safe_session('user_id')
    projects = _get_filtered_projects()
    possible_states = config.states('tracker')

    project_ids = list_ids(projects)
    stories = _stories_for(project_ids)

    in_progress_ids = ids_for_in_progress(stories)

    stories = keep_by_ids(stories, in_progress_ids)
    stories = prettify_stories(stories)
    stories = add_project_names(stories, projects)

    return render_template('index.html', projects=projects,user=current_user,states=possible_states, stories=stories)

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'GET' :
        return render_template("login.html")

    username = request.form['username']
    user_token = tracker.get_auth_token(request.form['username'], request.form['password'])

    project_list = ProjectList(tracker.getProjects(user_token))
    project_ids = list_ids(project_list)
    localdata.cache_data(username, project_ids)

    session['user_id'] = username

    return redirect(url_for('overview'))

@app.route('/logout')
def logout():
    if 'user_id' in session:
        del session['user_id']
    return redirect(url_for('overview'))


@app.route("/<int:project_id>")
def project(project_id):
    current_user =flask_helper.safe_session('user_id')

    project_list = _get_filtered_projects()
    project_found = find_project(project_list, str(project_id))

    if project_found == None:
        return redirect(url_for('overview'))

    project_id = str(project_id)
    burndown = Burndown(project_id,localdata.getBurndownStates(project_id))
    labels = burndown_labels(burndown)
    possible_states = config.states('tracker')

    return render_template("project.html", project=project_found, labels=labels, states=possible_states )

@app.route("/<int:project_id>/burndown.json")
def project_json(project_id):
    project_id = str(project_id)
    return burndown_tojson(Burndown(project_id,localdata.getBurndownStates(project_id)))

@app.route("/<int:project_id>/labels.json")
def labels(project_id):
    project_id = str(project_id)
    burndown = Burndown(project_id,localdata.getBurndownStates(project_id))
    labels = burndown_labels(burndown)
    return labels_tojson(labels)

@app.route("/projects.json")
def projects_json():
    project_list = _get_filtered_projects()
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
    project_ids = list_ids(project_list)

    stories_xml_list = [localdata.getStoriesXML(str(id)) for id in project_ids]

    stories = StoryList(stories_xml_list)
    users = UserList(stories)

    return userlist_tojson(users)


@app.route("/wip")
def wip(type=None):

    project_list = ProjectList(localdata.getProjectsXML())
    project_ids = list_ids(project_list)

    stories_xml_list = [localdata.getStoriesXML(str(id)) for id in project_ids]

    stories = StoryList(stories_xml_list)
    users = UserList(stories)

    return render_template('wip.html', projects=project_list , users=users)

@app.route("/config/")
def config_page():
    pass

if __name__ == "__main__":
    print "running flask"
    app.run(port=4567, host='0.0.0.0') 
