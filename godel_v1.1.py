from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def main():
    model_name = "microsoft/GODEL-v1_1-large-seq2seq"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def generate(instruction, knowledge, dialog):
        if knowledge != '':
            knowledge = '[KNOWLEDGE] ' + knowledge
        dialog = ' EOS '.join(dialog)
        query = f"{instruction} [CONTEXT] {dialog} {knowledge}"
        input_ids = tokenizer(f"{query}", return_tensors="pt").input_ids
        outputs = model.generate(input_ids, max_length=128, min_length=8, top_p=0.9, do_sample=True)
        output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return output

    # Instruction for a chitchat task
    instruction = f'You are a social robot that like to entertain users and be a friend to them.'

<<<<<<< Updated upstream
    # Leave the knowldge empty
    knowledge = 'I have a doctors appointment tomorrow at 4pm.'
    dialog = [
        'Hello! How are you?',
        'I am great! And you?.',
        'Me as well thank you for asking.'
    ]
=======
# Leave the knowldge empty
knowledge = ''
dialog = [
    'Hello! How are you?',
    'I am great! And you?.',
    'Me as well thank you for asking.'
]
>>>>>>> Stashed changes

    for _ in range(5):
        dialog.append(input("\n> "))
        response = generate(instruction, knowledge, dialog)

        dialog.append(response)

        print(response)
        print()
        print(dialog)

        print()
        print(knowledge)

if __name__ == '__main__':
    main()