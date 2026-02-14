def send_message(messages, model="mistralai/Mistral-7B-Instruct-v0.3", max_tokens=4096, temperature=0.7, top_p=1):
    # This client is now disabled. Use Ollama local Mixtral instead.
    pass

if __name__ == "__main__":
    messages = [
        {
            "role": "user",
            "content": "Explain quantum computing in simple terms"
        }
    ]
    print(send_message(messages))
