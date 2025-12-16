def generate_response(user_text: str) -> str:
    """
    Placeholder for LLM logic.
    For now, uses simple rules until we plug in Llama / GPT.
    """
    text = user_text.lower()

    if "services" in text or "what do you do" in text:
        return "iTechSeed provides AI, data, and software consultation services."
    elif "hello" in text or "hi" in text:
        return "Hello! I am the iTechSeed Voice Consultation Agent. How can I help you today?"
    elif "thank you" in text:
        return "You are welcome! Let me know if you have more questions."
    else:
        return "I can help you with consultation details, services, or general queries about iTechSeed."
