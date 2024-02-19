from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks


@inlineCallbacks
def main(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    yield session.call("rie.vision.face.find")
    yield session.call("rie.dialogue.say", text="Hallo!")
    yield session.call("rie.vision.face.track")
    yield session.call("rie.dialogue.say", text="Ik zie je niet meer!")
    session.leave()  # Close the connection with the robot


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65c375afc01d7b660046e90c",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
