import requests

class ChatGPTHelper:
    # API-related code removed

    def ask(self, prompt, model="gpt-3.5-turbo", temperature=0.7):
        # Note: Tanya uses GLM-5 as primary transformer. ChatGPT is fallback, not supreme authority.
        headers = {
            # API-related code removed
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }
        # API-related code removed
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"[ChatGPT API Error] {response.status_code}: {response.text}"
