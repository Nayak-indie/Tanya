from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def main():
    print("Loading Mixtral tokenizer and model...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        print("Model and tokenizer loaded successfully.")
        while True:
            user = input("You: ")
            if user.lower() in ("exit", "quit"): break
            input_ids = tokenizer.encode(user, return_tensors="pt")
            output = model.generate(input_ids, max_new_tokens=64, pad_token_id=tokenizer.eos_token_id)
            reply = tokenizer.decode(output[0], skip_special_tokens=True)
            print("Mixtral:", reply)
    except Exception as e:
        print("Error loading or running Mixtral:", e)

if __name__ == "__main__":
    main()
