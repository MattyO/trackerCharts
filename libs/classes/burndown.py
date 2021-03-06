from time import strftime, strptime, localtime 
import json

class Burndown:
    def __init__(self, project_name, states=[], possible_states=None):
        self.project_name = project_name
        self.states = states
        self.possible_states = possible_states

        if self.possible_states is None:
            self.possible_states = ["unscheduled", "unstarted", "started", "finished", "delivered", "accepted"]
        if self.states == None:
            self.states = []

def burndown_labels(burndown):
    labels = set() 
    for state in burndown.states:
        for label in state:
            labels.add(label)
    if "datetime" in labels:
        labels.remove("datetime")
    
    return list(sorted(labels))


def burndown_tojson(burndown):
    burndown_states = burndown.states
    burndown_states = sorted(burndown_states, key=lambda state: strptime(state['datetime'],"%Y.%m.%d %H:%M:%S") )
    return json.dumps({"id":burndown.project_name, "states":burndown_states})

def projectlist_tojson(project_list):
    dumpable = []
    for project in project_list:
        dumpable.append(project.id)

    return json.dumps({"ids":dumpable})

def labels_tojson(labels):
    return json.dumps(labels)

def addState(burndown, stories):

    burndown_state = {"all":_initial_state()}
    for story in stories:

        if _needs_burndown_label_state(burndown_state, "all", story.current_state):
            burndown_state = _add_burndown_label_state(burndown_state, "all", story.current_state)

        burndown_state = _increment_burndown_label_state(burndown_state , "all", story.current_state)
        burndown_state = _increment_burndown_label_state(burndown_state , "all", "total")

        for label in story.labels:
            if _needs_burndown_label(burndown_state , label):
                burndown_state = _add_burndown_label(burndown_state, label)

            if _needs_burndown_label_state(burndown_state, label, story.current_state):
                burndown_state = _add_burndown_label_state(burndown_state, label, story.current_state)

            burndown_state = _increment_burndown_label_state(burndown_state , label, story.current_state)
            burndown_state = _increment_burndown_label_state(burndown_state , label, "total")

    burndown_state = _normalize_burndown_state(burndown_state, burndown.possible_states)

    burndown_state = _append_burndown_state_datetime(burndown_state)

    burndown = append_burndown_state(burndown, burndown_state)

    return burndown

def append_burndown_state(burndown, burndown_state):
    if burndown.states == []:
        burndown.states  = [burndown_state]
    else:
        burndown.states.append(burndown_state)

    return burndown

def _initial_state():
    return {"total":0}

def _needs_burndown_label(burndown_state, label):
    return not burndown_state.has_key(label)

def _needs_burndown_label_state(burndown_state, label, story_state):
    return not burndown_state[label].has_key(story_state)

def _add_burndown_label(burndown_state, label):
    burndown_state[label] = _initial_state()
    return burndown_state

def _add_burndown_label_state(burndown_state, label, story_state):
    burndown_state[label][story_state] = 0
    return burndown_state

def _increment_burndown_label_state(burndown_state, label, story_state):
    burndown_state[label][story_state] += 1
    return burndown_state

def _append_burndown_state_datetime(state):
    date = strftime('%Y.%m.%d',localtime())
    time = strftime('%H:%M:%S',localtime())
    state["datetime"] = date + " " + time
    return state

def _normalize_burndown_state(state, story_states):
    for story_state in story_states:
        for state_label in state.keys():
            if state[state_label].has_key(story_state) == False:
                state[state_label][story_state] = 0
    return state
