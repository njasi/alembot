import json
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM

CONFIG = json.load(open("config/config.json"))
with open(CONFIG["model"]["prompt_path"]) as file:
    INPUT_PROMPT = "".join(file.readlines())

def load_model():
    checkpoint = CONFIG["model"]["path"]
    model = pipeline("text2text-generation", model=checkpoint)
    # tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    # model = AutoModelForCausalLM.from_pretrained(checkpoint)
    return model


def generate_full_prompt(message, instruction):
    # instruction = 'instruction text'
    if instruction:
        input_prompt = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n${}\n\n### Response:"
        return input_prompt.format(INPUT_PROMPT + message)

    return INPUT_PROMPT + message


def ask(message, model, instruction=False):
    input_prompt = generate_full_prompt(
        message, instruction)

    print("Prompt:", input_prompt)
    generated_text = model(input_prompt, max_length=512, do_sample=True)[0]['generated_text']

    return generated_text


def main():
    model = load_model()

    message = "how do i print something"
    response = ask(message, model, instruction=False)

    print("MESSAGE:\n", message)
    print("ALEMBOT:\n", response)


if __name__ == "__main__":
    main()
