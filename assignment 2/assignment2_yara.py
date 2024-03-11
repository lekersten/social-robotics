from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

head_patted = False


def touched(frame):
    global head_patted
    if (("body.head.front" in frame["data"] and frame["data"]["body.head.front"]) or
            ("body.head.middle" in frame["data"] and frame["data"]["body.head.middle"]) or
            ("body.head.rear" in frame["data"] and frame["data"]["body.head.rear"])):
        print("The head was touched!")
        head_patted = True


def say_upset_sentence():
    pass


@inlineCallbacks
def say_big_sentence(session, details):
    # After preparation (have arms close to chest, maybe lower body somehow?)
    session.call("rom.actuator.motor.write",
                 frames=[
                     {"time": 1000, "data": {"body.arms.right.upper.pitch": -1.0, "body.arms.left.upper.pitch": -1.0,
                                             "body.arms.right.lower.roll": -1.7, "body.arms.left.lower.roll": -1.7}}],
                 force=True
                 )
    # During stroke (move arms away from body slightly and up, then move arms outward)
    yield session.call("rom.actuator.motor.write",
                       frames=[
                           {"time": 1000,
                            "data": {"body.arms.right.upper.pitch": -1.5, "body.arms.left.upper.pitch": -1.5,
                                     "body.arms.right.lower.roll": -1.0, "body.arms.left.lower.roll": -1.0}},
                           {"time": 2000,
                            "data": {"body.arms.right.upper.pitch": -2.5, "body.arms.left.upper.pitch": -2.5,
                                     "body.arms.right.lower.roll": 2.0, "body.arms.left.lower.roll": 3.0}}
                       ],
                       force=True
                       )
    # After stroke (lower arms down and move back to robot's sides)
    yield session.call("rom.actuator.motor.write",
                       frames=[
                           {"time": 1000, "data": {"body.arms.right.upper.pitch": 0, "body.arms.left.upper.pitch": 0,
                                                   "body.arms.right.lower.roll": 0, "body.arms.left.lower.roll": 0}}],
                       force=True
                       )


@inlineCallbacks
def main(session, details):
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    yield session.call("rie.dialogue.config.language", lang="en")

    yield say_big_sentence(session, details)

    session.leave()

    # # Sad gesture
    # yield sleep(5)

    # 'body.arms.right.upper.pitch': {'max': 1.5943951023931953, 'min': -2.5943951023931953, 'type': 'joint'},
    # 'body.arms.right.lower.roll': {'max': 6.46259971647245e-05, 'min': -1.745264625997165, 'type': 'joint'},
    # 'body.torso.yaw': {'max': 0.8726646259971648, 'min': -0.8726646259971648, 'type': 'joint'},

    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    t_0 = 1000  # start preparation
    t_1 = 1500 / 4  # preparation duration
    t_2 = 2000 / 5  # stroke duration
    t_3 = 1000  # retraction duration

    session.call("rie.dialogue.say", text="It makes me very sad/upset that you don't want to hear my story.")

    session.call("rom.actuator.motor.write",
                 frames=[{"time": t_0, "data": {"body.torso.yaw": 0}}],
                 force=True
                 )

    # preparation
    session.call("rom.actuator.motor.write",
                 frames=[
                     {"time": t_1 * 4, "data": {"body.arms.right.upper.pitch": -1.5, "body.arms.left.upper.pitch": -1.5,
                                                "body.arms.right.lower.roll": -1.5, "body.arms.left.lower.roll": -1.5,
                                                "body.legs.right.upper.pitch": -0.5,
                                                "body.legs.left.upper.pitch": -0.5}}],
                 force=True
                 )
    # session.call("rom.actuator.motor.write",
    #              frames=[{"time": t_1, "data": {"body.arms.right.upper.pitch": -1.5, "body.arms.left.upper.pitch": -1.5}}],
    #              force=True
    #              )
    # session.call("rom.actuator.motor.write",
    #              frames=[{"time": t_1, "data": {"body.arms.right.lower.roll": -1.5, "body.arms.left.lower.roll": -1.5}}],
    #              force=True
    #              )
    # session.call("rom.actuator.motor.write",
    #              frames=[{"time": t_1*3,
    #                       "data": {"body.legs.right.upper.pitch": -0.5, "body.legs.left.upper.pitch": -0.5}}],
    #              force=True
    #              )

    # during stroke
    session.call("rom.actuator.motor.write",
                 frames=[{"time": t_2, "data": {"body.head.pitch": 0.17}}],
                 force=True
                 )

    session.call("rom.actuator.motor.write",
                 frames=[{"time": t_2, "data": {"body.head.yaw": 0.5}},
                         {"time": t_2 * 2, "data": {"body.head.yaw": -0.5}},
                         {"time": t_2 * 3, "data": {"body.head.yaw": 0.5}},
                         {"time": t_2 * 4, "data": {"body.head.yaw": -0.5}},
                         {"time": t_2 * 5, "data": {"body.head.yaw": 0}}],
                 force=True
                 )

    # First wait for user to touch its head
    yield session.subscribe(touched, "rom.sensor.touch.stream")
    yield session.call("rom.sensor.touch.stream")

    while not head_patted:
        yield sleep(0.5)

    # retraction
    session.call("rom.actuator.motor.write",
                 frames=[{"time": t_3,
                          "data": {"body.legs.right.upper.pitch": 0, "body.legs.left.upper.pitch": 0,
                                   "body.arms.right.lower.roll": 0, "body.arms.left.lower.roll": 0,
                                   "body.arms.right.upper.pitch": 0, "body.arms.left.upper.pitch": 0}}],
                 force=True
                 )

    # session.call("rom.actuator.motor.write",
    #              frames=[{"time": t_3,
    #                       "data": {"body.legs.right.upper.pitch": 0, "body.legs.left.upper.pitch": 0}}],
    #              force=True
    #              )
    # session.call("rom.actuator.motor.write",
    #              frames=[{"time": t_3,
    #                       "data": {"body.arms.right.lower.roll": 0, "body.arms.left.lower.roll": 0}}],
    #              force=True
    #              )
    # session.call("rom.actuator.motor.write",
    #              frames=[{"time": t_3,
    #                       "data": {"body.arms.right.upper.pitch": 0, "body.arms.left.upper.pitch": 0}}],
    #              force=True
    #              )

    yield session.call("rie.dialogue.say", text="Thank you!")

    yield session.call("rom.optional.behavior.play", name="BlocklyStand")

    session.leave()  # Close the connection with the robot


wamp = Component(
    transports=[{
        "url": "ws://wamp.robotsindeklas.nl",
        "serializers": ["msgpack"],
        "max_retries": 0
    }],
    realm="rie.65eedca6d9eb6cfb396e7492",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])
