from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import random

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

# instruction = f'You are a social robot that like to entertain users and be a friend to them.'
instruction = f'Given a dialog context, you need to respond optimistically, friendly, empathically and easily understandable.'

knowledge = 'My name is Alphie.'
dialog = []

greetings = ["Hello!", "Hi!", "Hey!", "Good Morning!", "Good Afternoon!"]
introduces = ["I'm a social robot.", "I'm Alphie", " "]
welcomes = ["Nice to meet you!", " Let's have a chat!", "I'm here to entertain you!", "What do you want to talk about?", "What's up?", "I'm here to be your friend.", "I'm here to talk to you.", "I'm here to keep you company.", " "]

intro = greetings[random.randint(0, len(greetings) - 1)] + " " + introduces[random.randint(0, len(introduces) - 1)] + " " + welcomes[random.randint(0, len(welcomes) - 1)]

dialog.append(intro)
print(intro)

exits = ["goodbye", "bye", "exit", "quit", "stop", "end"]

for _ in range(15):
    dialog.append(input("\n> "))


    if dialog[-1] in exits:
        signoffs = ["Goodbye!", "Bye!", "See you later!", "Take care!"]
        farewells = ["It was nice talking to you.", "Have a great day!", "I hope to see you soon.", "Enjoy the rest of your day!", " "]

        outro = signoffs[random.randint(0, len(signoffs) - 1)] + " " + farewells[random.randint(0, len(farewells) - 1)]

        print(outro)

        break

    response = generate(instruction, knowledge, dialog)

    dialog.append(response)

    print(response)
    print()
    