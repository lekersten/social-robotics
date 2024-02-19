from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

<<<<<<< Updated upstream
@inlineCallbacks
def main(session, details):
    question = "Is Paul a good prof?"
    answers = {"yes": ["yes", "sure", "yeah"], "super": ["super", "the best", "definitely"]}

    answer = yield session.call("rie.dialogue.ask",
                                question=question,
                                answers=answers)

    if answer == "yes":
        yield session.call("rie.dialogue.say_animated",
                           text="Good to hear that you think Paul is a good prof. I agree")
    elif answer == "super":
        session.call("rie.dialogue.say",
                     text="Great. Paul is indeed a super-duper prof")
        yield session.call("rom.optional.behavior.play", name="BlocklyHappy")
    else:
        yield session.call("rie.dialogue.say",
                           text="Sorry. What did you say? Be positive about Paul")
    yield session.call("rie.dialogue.stop")

    session.leave()  # Close the connection with the robot
=======
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

import random

def initial_model():
    model_name = "microsoft/GODEL-v1_1-large-seq2seq"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    instruction = f'You are a social robot that like to entertain users and be a friend to them.'

    openings = ["Hello! How are you?", "Hi! How's it going?", "Hey! What's up?", "Hello"]

    knowledge = ''
    dialog = []

    dialog.append(openings[random.randint(0, len(openings) - 1)])

    return model, tokenizer, instruction, knowledge, dialog


def asr(frames):
    global finish_dialogue
    if frames['data']['body']['final']:
        print(frames["data"]["body"]["text"])
        if frames["data"]["body"]["text"] == "bye" or \
                frames["data"]["body"]["text"] == "goodbye":
            finish_dialogue = True


def generate(instruction, knowledge, dialog):
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

    yield session.call("rie.dialogue.say", text=dialog[0])

    text = yield session.call("rie.dialogue.stt.read")
    print("I heard ",text)

    dialog.append(text)

    yield session.subscribe(asr, "rie.dialogue.stt.stream")
    yield session.call("rie.dialogue.stt.stream")

    # loop while user did not say goodbye or bye
    while not finish_dialogue:
        response = generate(instruction, knowledge, dialog)

        dialog.append(response)
        yield session.call("rie.dialogue.say", text=response)
       
        yield sleep(0.5)

    yield session.call("rie.dialogue.stt.close")

    yield session.call("rie.dialogue.say", text="Goodbye! It was nice talking to you.")
    session.leave()

>>>>>>> Stashed changes

wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
<<<<<<< Updated upstream
    realm="rie.65ccac62c01d7b6600471940",
=======
    realm="rie.65d35051ead719a540fad216",
>>>>>>> Stashed changes
)

wamp.on_join(main)

if __name__ == "__main__":
<<<<<<< Updated upstream
    run([wamp])
=======
    run([wamp])
>>>>>>> Stashed changes
