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


model = load_model()


def replace_info(text):
    '''
    replace redacted info from the actual info in the config
    '''
    info = CONFIG["info"]
    for key in info:
        text = text.lower().replace(key.lower(), info[key])
    return text


def generate_full_prompt(message, instruction):
    # instruction = 'instruction text'
    if instruction:
        input_prompt = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n${}\n\n### Response:"
        return input_prompt.format(INPUT_PROMPT + message)

    return INPUT_PROMPT + message


def ask_model(message, model, instruction=False):
    input_prompt = generate_full_prompt(
        message, instruction)

    generated_text = model(input_prompt, max_length=128, do_sample=True)[
        0]['generated_text']

    return generated_text


def ask(message, instruction=False):
    return replace_info(ask_model(message, model, instruction))


def main():
    message = "how do i print something"
    response = ask(message, instruction=False)

    print("MESSAGE:\n", message)
    print("ALEMBOT:\n", response)


if __name__ == "__main__":
    main()
