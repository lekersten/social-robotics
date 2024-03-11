from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep


@inlineCallbacks
def main(session, details):
    question = "Yes or No?"
    answers = {"yes": ["yes", "sure", "yeah"], "no": ["no", "nope", "non"]}

    print("Test1")

    answer = yield session.call("rie.dialogue.ask",
                                question=question,
                                answers=answers)
    print("Test2")

    if answer == "yes":
        yield session.call("rie.dialogue.say_animated",
                           text="Yes")
        print("Test3")
    elif answer == "no":
        session.call("rie.dialogue.say",
                     text="No")
        print("Test4")
        yield session.call("rom.optional.behavior.play", name="BlocklyHappy")
    else:
        yield session.call("rie.dialogue.say",
                           text="Sorry")
        print("Test5")
    yield session.call("rie.dialogue.stop")
    print("Test6")

    session.leave()  # Close the connection with the robot


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65eeee61d9eb6cfb396e75c8",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
