# Placeholder for HuggingFace model integration
# This script will help you download and load a model from HuggingFace for Tanya

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "microsoft/DialoGPT-medium"  # You can change this to any conversational model

print("Downloading model and tokenizer from HuggingFace...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Save locally for Tanya to use later
model.save_pretrained("./hf_model/")
tokenizer.save_pretrained("./hf_model/")
print("Model and tokenizer saved to ./hf_model/")

# Example inference (for future integration)
def chat_with_model(prompt):
    inputs = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors="pt")
    outputs = model.generate(inputs, max_length=100, pad_token_id=tokenizer.eos_token_id)
    reply = tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    return reply

if __name__ == "__main__":
    print("Try chatting with the model:")
    while True:
        user = input("You: ")
        if user.lower() in ("exit", "quit"): break
        print("Tanya (HF):", chat_with_model(user))
