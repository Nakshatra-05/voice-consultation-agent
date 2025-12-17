def generate_response(user_text: str, language: str) -> str:
    if language == "hi":
        if "सेवा" in user_text or "services" in user_text:
            return "आईटेकसीड एआई, डेटा और सॉफ्टवेयर कंसल्टिंग सेवाएं प्रदान सकती है।"
        elif "नमस्ते" in user_text:
            return "नमस्ते! मैं आपकी कैसे मदद कर सकती हूँ?"
        else:
            return "आईटेकसीड से संपर्क करने के लिए धन्यवाद। मैं आपकी क्या सहायता कर सकती हूँ।"

    # Default: English
    if "services" in user_text.lower():
        return "iTechSeed provides AI, data engineering, and software consulting services."
    elif "hello" in user_text.lower():
        return "Hello! How can I assist you today?"
    else:
        return "Thank you for contacting iTechSeed. How can I help you?"
