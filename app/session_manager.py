import uuid
from typing import Dict, List

# In-memory session store
_sessions: Dict[str, List[dict]] = {}

def create_session() -> str:
    session_id = str(uuid.uuid4())
    _sessions[session_id] = []
    return session_id

def add_message(session_id: str, role: str, content: str):
    if session_id not in _sessions:
        _sessions[session_id] = []

    _sessions[session_id].append({
        "role": role,      # "user" or "agent"
        "content": content
    })

def get_history(session_id: str):
    return _sessions.get(session_id, [])
