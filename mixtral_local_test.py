from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# Only load if already downloaded locally, do not trigger download
LOCAL_PATH = "./hf_model/mixtral/"

def main():
    print("Loading Mixtral tokenizer and model from local path...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(LOCAL_PATH)
        model = AutoModelForCausalLM.from_pretrained(LOCAL_PATH)
        print("Model and tokenizer loaded successfully from local cache.")
        while True:
            user = input("You: ")
            if user.lower() in ("exit", "quit"): break
            input_ids = tokenizer.encode(user, return_tensors="pt")
            output = model.generate(input_ids, max_new_tokens=64, pad_token_id=tokenizer.eos_token_id)
            reply = tokenizer.decode(output[0], skip_special_tokens=True)
            print("Mixtral:", reply)
    except Exception as e:
        print("Error loading or running Mixtral from local path:", e)
        print("Model not found locally. Please download it first.")

if __name__ == "__main__":
    main()
