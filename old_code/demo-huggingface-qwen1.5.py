from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig


def demo(model_name="Qwen/Qwen1.5-7B-Chat"):
    device = "cpu"
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    prompt = "Give me a short introduction to large language model."
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(response)


def conversation(model_name):
    device = "cpu"
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    prompt = input("\n> ")
    messages = [
        {"role": "system", "content": "You are a person that likes to have a talk with people about what interests them."},
        {"role": "user", "content": "I want to talk about dogs!"},
        {"role": "system",
         "content": "That sounds like an interesting topic! What kind of conversation would you like to have? Do you have any specific questions or topics in mind, or do you just want to chat generally?."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(response)


if __name__ == '__main__':
    model_name = "Qwen/Qwen1.5-0.5B-Chat"
    # demo(model_name=model_name)
    conversation(model_name)
