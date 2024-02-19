from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

"""
ASR with subscribe. 

Each time the speech recognizer signals the end of some input with 'final',
the example prints this sentence
When the user says bye or goodbye, the program finishes
"""
finish_dialogue = False


def asr(frames):
    global finish_dialogue
    if frames['data']['body']['final']:
        print(frames["data"]["body"]["text"])
        if frames["data"]["body"]["text"] == "bye" or \
                frames["data"]["body"]["text"] == "goodbye":
            finish_dialogue = True


@inlineCallbacks
def main(session, details):
    # set language to English (use 'nl' for Dutch)
    yield session.call("rie.dialogue.config.language", lang="en")
    # prompt from the robot to the user to say something
    yield session.call("rie.dialogue.say", text="Say something")

    text = yield session.call("rie.dialogue.stt.read")
    print("I heard ", text)

    # subscribes the asr function with the input stt stream
    yield session.subscribe(asr, "rie.dialogue.stt.stream")
    # calls the stream. From here, the robot prints each 'final' sentence
    yield session.call("rie.dialogue.stt.stream")

    # loop while user did not say goodbye or bye
    while not finish_dialogue:
        yield sleep(0.5)

    yield session.call("rie.dialogue.stt.close")
    session.leave()


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65ccac62c01d7b6600471940",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
