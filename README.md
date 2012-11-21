trackerCharts
=============

burndown and WIP charts for pivotal tracker.  

Endpoints
--------
The following are some imporant endpoints
###/update###
Updates the current state of all projects, their burndowns, and wip for all persons.  Note that this makes trackerCharts only as current as the last update.
###/(project_id)/burndown.json###
returns a json for the current burndown of the project found in the url.  This is broken up by al cards as well as is broken up by labels.  Epics show up as labels.  
###/wip.json###
Returns a json of current wip computed for each individal and the stories that make up that wip
###in progress end points###
the following endpoints are in progress 
* /<project_id>
** this will be the place to provide mutliple burndown charts based on labels.  
* /config
** when the system is updated to contain other apis to pull stories from.  We will also need to provide some way to define how stories add up.  in effect ordering story states [unschedualed, started, finished...etc]

Install
-------
1. clone / downlaod repo
2. install dependencies
** found in pip-install file
3. rename and update example-config.py to config.py.  Replace containing user name and password items
** found in lib directory
4. run app
** python app.py

Testing
-------
* nosetest tests/unit
