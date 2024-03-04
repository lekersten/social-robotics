from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep


class StorySentence:
    def __init__(self, text):
        self.text = text
        self.preparation = []
        self.stroke = []
        self.post_stroke = []


@inlineCallbacks
def main(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    yield session.call("rie.dialogue.config.language", lang="en")
    # Maybe use say animated somewhere? (for sentences without movement?)

    # # Huge gesture
    # session.call("rie.dialogue.say", text="My friend has a enormous dog.")
    # session.call("rom.actuator.motor.write",
    #              frames=[{"time": 400, "data": {"body.head.pitch": 0.1}},
    #                      {"time": 1200, "data": {"body.head.pitch": -0.1}},
    #                      {"time": 2000, "data": {"body.head.pitch": 0.1}},
    #                      {"time": 2400, "data": {"body.head.pitch": 0.0}}],
    #              force=True
    #              )

    # yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    # session.call("rom.actuator.motor.write",
    #              # frames=[{"time": 1200, "data": {"body.head.pitch": 0.17}}], # head down
    #              frames=[{"time": 1200, "data": {"body.arms.right.upper.pitch": -0.7}}],
    #              force=True
    #              )
    # session.call("rom.actuator.motor.write",
    #              # frames=[{"time": 1200, "data": {"body.head.pitch": 0.17}}], # head down
    #              frames=[{"time": 2400, "data": {"body.arms.right.lower.roll": -1.74}}],
    #              force=True
    #              )

    # # Sad gesture
    # yield sleep(5)
    # session.call("rie.dialogue.say", text="It makes me very sad that you don't want to hear my story.")

    # 'body.arms.right.upper.pitch': {'max': 1.5943951023931953, 'min': -2.5943951023931953, 'type': 'joint'},
    # 'body.arms.right.lower.roll': {'max': 6.46259971647245e-05, 'min': -1.745264625997165, 'type': 'joint'},
    # 'body.torso.yaw': {'max': 0.8726646259971648, 'min': -0.8726646259971648, 'type': 'joint'},

    target_word_time = 5000
    target_word_duration = 1000
    prep_time = target_word_time - 2400
    # preparation
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    session.call("rom.actuator.motor.write",
                 frames=[{"time": prep_time, "data": {"body.torso.yaw": 0}}],
                 force=True
                 )
    session.call("rom.actuator.motor.write",
                 frames=[
                     {"time": prep_time+600, "data": {"body.arms.right.upper.pitch": -1, "body.arms.left.upper.pitch": -1}}],
                 force=True
                 )
    session.call("rom.actuator.motor.write",
                 frames=[
                     {"time": prep_time+1200, "data": {"body.arms.right.lower.roll": -1.5, "body.arms.left.lower.roll": -1.5}}],
                 force=True
                 )
    session.call("rom.actuator.motor.write",
                 frames=[{"time": prep_time+1200, "data": {"body.legs.right.upper.pitch": -0.0}},
                         {"time": prep_time+2400,
                          "data": {"body.legs.right.upper.pitch": -0.4, "body.legs.left.upper.pitch": -0.4}}],
                 force=True
                 )

    # # at start of stroke
    session.call("rom.actuator.motor.write",
                 frames=[{"time": target_word_time, "data": {"body.arms.right.upper.pitch": -1.7, "body.arms.left.upper.pitch": -1.7}}],
                 force=True
                 )
    session.call("rom.actuator.motor.write",
                 frames=[{"time": target_word_time, "data": {"body.arms.right.lower.roll": -1.5, "body.arms.left.lower.roll": -1.5}}],
                 force=True
                 )
    session.call("rom.actuator.motor.write",
                 frames=[{"time": target_word_time,
                          "data": {"body.legs.right.upper.pitch": -0.8, "body.legs.left.upper.pitch": -0.8}}],
                 force=True
                 )
    # during stroke
    # # TODO: try to move body left/right
    # session.call("rom.actuator.motor.write",
    #              frames=[{"time": 2400, "data": {"body.torso.roll": -0.0}},
    #                      {"time": 3600, "data": {"body.torso.roll": -0.8}},
    #                      {"time": 4800, "data": {"body.torso.roll": 0.8}}],
    #              force=True
    #              )
    # session.call("rom.actuator.motor.write",
    #              frames=[{"time": 1200, "data": {"body.head.pitch": 0.17}}],
    #              force=True
    #              )
    # # after
    # session.call("rom.actuator.motor.write",
    #              frames=[{"time": 2400, "data": {"body.head.pitch": 0.17}},
    #                      {"time": 3600, "data": {"body.head.pitch": 0.0}}],
    #              force=True
    #              )
    session.leave()  # Close the connection with the robot


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65e5b9c7d9eb6cfb396e4516",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
