from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep


global sess


@inlineCallbacks
def on_keyword(frame):
    global sess
    c = frame["data"]["body"]["certainty"]
    print("certainty", c, ": ", frame)
    if "certainty" in frame["data"]["body"] and frame["data"]["body"]["certainty"] > 0.45:
        word = frame["data"]["body"]["text"]
        yield sess.call("rie.dialogue.say_animated", text=f"Test worked for {word}!")


@inlineCallbacks
def main(session, details):
    question = "This is a test."
    global sess
    sess = session

    yield session.call("rie.dialogue.config.language", lang="en")
    yield session.call("rie.dialogue.keyword.language", lang="en")
    yield session.call("rie.dialogue.say_animated", text=question)
    yield session.call("rie.dialogue.keyword.add", keywords=["yes", "test"])
    yield session.subscribe(on_keyword, "rie.dialogue.keyword.stream")
    yield session.call("rie.dialogue.keyword.stream")

    # yield session.leave()  # Close the connection with the robot


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65f82fc5a6c4715863c5768b",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])