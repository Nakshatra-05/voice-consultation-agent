import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-agent")


def log_interaction(
    session_id: str,
    language: str,
    user_text: str,
    agent_reply: str,
    fallback: bool
):
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": session_id,
        "event": "voice_interaction",
        "language": language,
        "user_text": user_text,
        "agent_reply": agent_reply,
        "fallback": fallback
    }

    logger.info(json.dumps(log_data))
