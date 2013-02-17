from flask import session

def safe_session(id):
    session_data = None
    if session.has_key(id):
        session_data = session[id]
    return session_data

