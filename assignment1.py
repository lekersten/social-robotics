from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

import random

def initial_model():
    model_name = "microsoft/GODEL-v1_1-large-seq2seq"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    instruction = f'You are a social robot that like to entertain users and be a friend to them.'

    knowledge = ''
    dialog = []

    greetings = ["Hello!", "Hi!", "Hey!", "Good Morning!", "Good Afternoon!", " "]
    introduces = ["I'm a social robot.", "I'm Alphie", " "]
    welcomes = ["Nice to meet you!", " Let's have a chat!", "I'm here to entertain you!", "What do you want to talk about?", "What's up?", "I'm here to be your friend.", "I'm here to talk to you.", "I'm here to keep you company.", " "]

    intro = greetings[random.randint(0, len(greetings) - 1)] + " " + introduces[random.randint(0, len(introduces) - 1)] + " " + welcomes[random.randint(0, len(welcomes) - 1)]

    dialog.append(intro)

    return model, tokenizer, instruction, knowledge, dialog


def asr(frames):
    global finish_dialogue
    
    exits = ["goodbye", "bye", "exit", "quit", "stop", "end"]

    if frames['data']['body']['final']:
        print(frames["data"]["body"]["text"])

        if frames["data"]["body"]["text"] in exits:
            finish_dialogue = True


def generate(model, tokenizer, instruction, knowledge, dialog):
    if knowledge != '':
        knowledge = '[KNOWLEDGE] ' + knowledge

    dialog = ' EOS '.join(dialog)
    query = f"{instruction} [CONTEXT] {dialog} {knowledge}"
    input_ids = tokenizer(f"{query}", return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_length=128, min_length=8, top_p=0.9, do_sample=True)
    output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return output


@inlineCallbacks
def main(session, details):
    model, tokenizer, instruction, knowledge, dialog = initial_model()
    finish_dialogue = False

    yield session.call("rie.dialogue.config.language", lang="en")

    yield session.call("rie.dialogue.say_animated", text=dialog[0])

    text = yield session.call("rie.dialogue.stt.read")
    print("I heard ",text)

    dialog.append(text)

    yield session.subscribe(asr, "rie.dialogue.stt.stream")
    yield session.call("rie.dialogue.stt.stream")

    # loop while user did not say goodbye or bye
    while not finish_dialogue:
        response = generate(model, tokenizer, instruction, knowledge, dialog)

        dialog.append(response)
        yield session.call("rie.dialogue.say_animated", text=response)
       
        yield sleep(0.5)

    yield session.call("rie.dialogue.stt.close")


    signoffs = ["Goodbye!", "Bye!", "See you later!", "Take care!"]
    farewells = ["It was nice talking to you.", "Have a great day!", "I hope to see you soon.", "Enjoy the rest of your day!", " "]

    outro = signoffs[random.randint(0, len(signoffs) - 1)] + " " + farewells[random.randint(0, len(farewells) - 1)]

    yield session.call("rie.dialogue.say_animated", text=outro)

    session.leave()

wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],

    realm="rie.65d35051ead719a540fad216",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
