from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks


class StorySentence:
    def __init__(self, text):
        self.text = text
        self.preparation = []
        self.stroke = []
        self.post_stroke = []


@inlineCallbacks
def test_movement(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    # info = yield session.call("rom.actuator.motor.info")
    # print(info)
    yield session.call("rom.actuator.motor.write",
                       frames=[{"time": 400, "data": {"body.head.pitch": 0.1}},
                               {"time": 1200, "data": {"body.head.pitch": -0.1}},
                               {"time": 2000, "data": {"body.head.pitch": 0.1}},
                               {"time": 2400, "data": {"body.head.pitch": 0.0}}],
                       force=True
                       )
    # yield session.call("rom.optional.behavior.play", name="BlocklySitDown")
    yield session.call("rom.optional.behavior.play", name="BlocklyArmsUp")
    session.leave()  # Close the connection with the robot


@inlineCallbacks
def talk_with_movement(session, details, storySentence):
    # Maybe use say animated somewhere? (for sentences without movement?)
    yield session.call("rie.dialogue.say", text="I am talking talking talking.")
    session.call("rom.actuator.motor.write",
                 frames=[{"time": 400, "data": {"body.head.pitch": 0.1}},
                         {"time": 1200, "data": {"body.head.pitch": -0.1}},
                         {"time": 2000, "data": {"body.head.pitch": 0.1}},
                         {"time": 2400, "data": {"body.head.pitch": 0.0}}],
                 force=True
                 )

    # yield session.call("rie.dialogue.say", text=storySentence.text)
    # session.call("rom.actuator.motor.write",
    #              frames=storySentence.preparation,
    #              force=True
    #              )


@inlineCallbacks
def main(session, details):
    test_movement(session, details)


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
