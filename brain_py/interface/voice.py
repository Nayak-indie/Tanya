# brain_py/interface/voice.py

class VoiceInterface:
    def listen(self) -> str:
        return input("🎙️ You: ")

    def speak(self, text: str):
        print(f"\n🧠 Tanya: {text}\n")
