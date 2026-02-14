import requests

class GeminiHelper:
    def __init__(self, api_key):
        # API-related code removed
        pass

    def ask(self, prompt):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        # API-related code removed
        if response.status_code == 200:
            try:
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            except Exception:
                return "[Gemini API removed]"
        else:
            return f"[Gemini API Error] {response.status_code}: {response.text}"
