from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep


@inlineCallbacks
def main(session, details):
    def touched(frame):
        if (("body.head.front" in frame["data"] and frame["data"]["body.head.front"]) or
                ("body.head.middle" in frame["data"] and frame["data"]["body.head.middle"]) or
                ("body.head.rear" in frame["data"] and frame["data"]["body.head.rear"])):
            session.call("rie.dialogue.say", text="Ow, my head!")
            sleep(2)
            session.call("rom.optional.behavior.play", name="BlocklyArmsUp")
            session.leave()  # Close the connection with the robot
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    yield session.subscribe(touched, "rom.sensor.touch.stream")
    yield session.call("rom.sensor.touch.stream")


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
